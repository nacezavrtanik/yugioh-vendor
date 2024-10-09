
from itertools import count
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from binder import Binder


class CardmarketBot:
    def __init__(
        self,
        driver_context_manager,
        ignore_signed_cards=True,
        ignore_altered_cards=True,
        ignore_bad_sellers=True,
        manual_lookup_threshold=None,
    ):
        self.driver_context_manager = driver_context_manager
        self.ignore_signed_cards = ignore_signed_cards
        self.ignore_altered_cards = ignore_altered_cards
        self.ignore_bad_sellers = ignore_bad_sellers
        self.manual_lookup_threshold = manual_lookup_threshold

    def evaluate_card(self, card):
        """Return lowest price as floating point number."""

    def evaluate_binder(self, binder):
        """Return lowest price total as floating point number."""

    def update_card_with_offers(self, card, n_offers=3):
        """Add n lowest offers to card."""

    def update_binder_with_offers(self, binder, n_offers=3):
        """Add n lowest offers to each card in binder."""
        with self.driver_context_manager() as driver:
            for card in binder:
                self.open_article_website_for_card(driver, card)
                prices = self.get_prices_for_card(driver, card)

    def open_article_website_for_card(self, driver, card):
        page_count = count(1)
        versions_xpath = "//div[@class='table-body']/div"
        set_xpath = "./div[3]"
        name_xpath = "./div[4]//a[1]"

        while True:
            driver.get(card.get_search_url(next(page_count)))
            versions = driver.find_elements(By.XPATH, versions_xpath)
            is_last_page = len(versions) < 30

            for version in versions:
                set_ = version.find_element(By.XPATH, set_xpath).text
                if set_ == card.set_:
                    name_element = version.find_element(By.XPATH, name_xpath)
                    name = name_element.text
                    if name == card.name:
                        print("!!!", set_, card.name)
                        print("FOUND")
                        print(name_element.get_attribute("href"))
                        return
                    print(" * ", set_, name)

            if is_last_page:
                print("NOT FOUND")
                break

    def get_prices_for_card(self, driver, card):
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


if __name__ == "__main__":

    from firefox import firefox_instance
    import config

    binder = Binder.from_excel(config.EXCEL)
    cardmarket_bot = CardmarketBot(firefox_instance)
    cardmarket_bot.update_binder_with_offers(binder)

