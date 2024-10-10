
from itertools import count
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from marketwatch.binder import Binder
from marketwatch.exceptions import ArticleNotFoundError


class PriceBot:
    SEARCH_URL_TEMPLATE = (
        "https://www.cardmarket.com/en/YuGiOh/Products/Search"
        "?searchString={search_term}"
        "&site={site_number}"
    )

    def __init__(
        self,
        driver_context_manager,
        ignore_bad_sellers=True,
        manual_lookup_threshold=None,
    ):
        self.driver_context_manager = driver_context_manager
        self.ignore_bad_sellers = ignore_bad_sellers
        self.manual_lookup_threshold = manual_lookup_threshold

    def evaluate_single(self, single):
        """Return lowest price as floating point number."""

    def evaluate_binder(self, binder):
        """Return lowest price total as floating point number."""

    def update_single_with_offers(self, single, n_offers=3):
        """Add n lowest offers to single."""

    def update_binder_with_offers(self, binder, n_offers=3):
        """Add n lowest offers to each single in binder."""
        with self.driver_context_manager() as driver:
            for single in binder:
                self._set_article_attribute_for_single(driver, single)
                prices = self.get_prices_for_single(driver, single)

    def _get_search_url_for_single(self, single, site_number=1):
        return self.SEARCH_URL_TEMPLATE.format(
            search_term=single.name.replace(" ", "+"),
            site_number=site_number,
        )

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
                    if name == single.name:
                        print("!!!", set_, single.name)
                        print("FOUND", name_element.get_attribute("href"))
                        single.article = name_element.get_attribute("href")
                        return
                    else:
                        print(" * ", set_, name)
            else:
                if is_last_page:
                    raise ArticleNotFoundError("last results page reached")

    def get_prices_for_single(self, driver, single):
        offers = []

        offer_xpath = "//div[@class='row g-0 article-row']"
        elements = driver.find_elements(By.XPATH, offer_xpath)

        for element in elements:
            seller_xpath = ".//span[@class='seller-name d-flex']/span[3]"
            seller = element.find_element(By.XPATH, seller_xpath).text

            condition_xpath = ".//span[@class='badge ']"
            condition = element.find_element(By.XPATH, condition_xpath).text

            language_xpath = ".//div[@class='product-attributes col']/span"
            language_element = element.find_element(By.XPATH, language_xpath)
            language = language_element.get_attribute("aria-label")

            edition_xpath = ".//div[@class='product-attributes col']/span[@class='icon st_SpecialIcon mr-1']"
            try:
                element.find_element(By.XPATH, edition_xpath)
            except NoSuchElementException:
                edition = "Unlimited"
            else:
                edition = "1st Edition"

            price_xpath = ".//div[@class='col-offer col-auto']//span"
            price = element.find_element(By.XPATH, price_xpath).text

            comment_xpath = ".//div[@class='product-comments me-1 col']"
            try:
                comment = element.find_element(By.XPATH, comment_xpath).text
            except NoSuchElementException:
                comment = ""

            attrs = seller, condition, language, edition, price, comment
            offers.append(attrs)
            print(attrs)
            return offers
