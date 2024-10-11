
from itertools import count
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from marketwatch.article import Article
from marketwatch.price import Price
from marketwatch.binder import Binder
from marketwatch.exceptions import ProductPageNotFoundError


class PriceBot:
    SEARCH_URL_TEMPLATE = (
        "https://www.cardmarket.com/en/YuGiOh/Products/Search"
        "?searchString={search_term}"
        "&site={site_number}"
    )
    DUELIST_LEAGUE_VERSION_MAPPING = {
        "blue": 1,
        "green": 2,
        "gold": 3,
        "silver": 4,
    }

    def __init__(
        self,
        driver_context_manager,
        ignore_bad_sellers=True,
        manual_lookup_threshold=None,
    ):
        self.driver_context_manager = driver_context_manager
        self.ignore_bad_sellers = ignore_bad_sellers
        self.manual_lookup_threshold = manual_lookup_threshold

    def _get_search_url_for_single(self, single, site_number=1):
        return self.SEARCH_URL_TEMPLATE.format(
            search_term=single.name.replace(" ", "+"),
            site_number=site_number,
        )

    def _get_single_name_for_version(self, single):
        if single.set_is_duelist_league:
            number = self.DUELIST_LEAGUE_VERSION_MAPPING.get(single.version)
            assert number
            suffix = f" (V.{number} - Rare)"
            name = single.name + suffix
        elif single.set_requires_language_code:
            assert single.version
        else:
            name = single.name
        return name


    def _set_url_attribute_for_single(self, driver, single):
        page_count = count(1)
        results_xpath = "//div[@class='table-body']/div"
        set_xpath = "./div[3]"
        name_xpath = "./div[4]//a[1]"
        results_per_full_search_page = 30

        while True:
            driver.get(self._get_search_url_for_single(single, next(page_count)))
            results = driver.find_elements(By.XPATH, results_xpath)
            is_last_page = len(results) < results_per_full_search_page

            for result in results:
                set_ = result.find_element(By.XPATH, set_xpath).text
                if set_ == single.set:
                    name_element = result.find_element(By.XPATH, name_xpath)
                    name = name_element.text
                    name_for_version = self._get_single_name_for_version(single)
                    if name == name_for_version:
                        print("!!!", set_, name)
                        print("FOUND", name_element.get_attribute("href"))
                        single.url = name_element.get_attribute("href")
                        return
                    else:
                        print(" * ", set_, name)
            else:
                if is_last_page:
                    raise ProductPageNotFoundError("last results page reached")

    def _set_articles_attribute_for_single(self, driver, single, n_articles=3):
        """Add n lowest articles to single."""
        driver.get(single.filtered_url)

        articles = []
        article_xpath = "//div[@class='row g-0 article-row']"
        elements = driver.find_elements(By.XPATH, article_xpath)

        for element in elements:
            location_xpath = ".//span[@class='icon d-flex has-content-centered me-1']"
            location_element = element.find_element(By.XPATH, location_xpath)
            location = location_element.get_attribute("aria-label")
            location = location.removeprefix("Item location: ")

            seller_xpath = ".//span[@class='seller-name d-flex']/span[3]"
            seller = element.find_element(By.XPATH, seller_xpath).text

            comment_xpath = ".//div[@class='product-comments me-1 col']"
            try:
                comment = element.find_element(By.XPATH, comment_xpath).text
            except NoSuchElementException:
                comment = ""

            price_xpath = ".//div[@class='col-offer col-auto']//span"
            price_element = element.find_element(By.XPATH, price_xpath)
            price_string = price_element.text.removesuffix(" €").replace(",", ".")
            price_float = float(price_string)
            price = Price(value=price_float, unit="EUR")

            quantity_xpath = "./div[3]/div[2]"
            quantity_element = element.find_element(By.XPATH, quantity_xpath)
            quantity = int(quantity_element.text)

            article = Article(location, seller, comment, price, quantity)
            articles.append(article)
            print(article)
        single.articles = articles

    def update_binder_with_articles(self, binder, n_articles=3):
        """Add n lowest articles to each single in binder."""
        with self.driver_context_manager() as driver:
            for single in binder:
                self._set_url_attribute_for_single(driver, single)
                self._set_articles_attribute_for_single(driver, single, n_articles)

    def get_prices_for_single(self, driver, single):
        pass
