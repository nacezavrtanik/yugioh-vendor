
from itertools import count
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from marketwatch.offer import Offer
from marketwatch.binder import Binder
from marketwatch.exceptions import ArticleNotFoundError


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


    def _set_article_attribute_for_single(self, driver, single):
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
                        single.article = name_element.get_attribute("href")
                        return
                    else:
                        print(" * ", set_, name)
            else:
                if is_last_page:
                    raise ArticleNotFoundError("last results page reached")

    def _set_offers_attribute_for_single(self, driver, single, n_offers=3):
        """Add n lowest offers to single."""
        driver.get(single.article)

        offers = []
        offer_xpath = "//div[@class='row g-0 article-row']"
        elements = driver.find_elements(By.XPATH, offer_xpath)

        for element in elements:
            location_xpath = ".//span[@class='icon d-flex has-content-centered me-1']"
            location_element = element.find_element(By.XPATH, location_xpath)
            location = location_element.get_attribute("aria-label")

            seller_xpath = ".//span[@class='seller-name d-flex']/span[3]"
            seller = element.find_element(By.XPATH, seller_xpath).text

            comment_xpath = ".//div[@class='product-comments me-1 col']"
            try:
                comment = element.find_element(By.XPATH, comment_xpath).text
            except NoSuchElementException:
                comment = ""

            price_xpath = ".//div[@class='col-offer col-auto']//span"
            price = element.find_element(By.XPATH, price_xpath).text

            n_available_xpath = "./div[3]/div[2]"
            n_available = element.find_element(By.XPATH, n_available_xpath).text

            offer = Offer(location, seller, comment, price, n_available)
            offers.append(offer)
        single.offers = offers

    def update_binder_with_offers(self, binder, n_offers=3):
        """Add n lowest offers to each single in binder."""
        with self.driver_context_manager() as driver:
            for single in binder:
                self._set_article_attribute_for_single(driver, single)
                self._set_offers_attribute_for_single(driver, single, n_offers)

    def get_prices_for_single(self, driver, single):
        pass
