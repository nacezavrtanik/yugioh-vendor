from itertools import count
import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from firefox import firefox_instance
from card import Card
from binder import Binder
import config


def open_article_website_for_card(driver, card):
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


def get_prices_for_card(driver, card):
    offers = []

    offer_xpath = "//div[@class='row g-0 article-row']"
    elements = firefox.find_elements(By.XPATH, offer_xpath)

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
    with firefox_instance() as firefox:
        for card in Binder.from_excel(config.EXCEL):
            open_article_website_for_card(firefox, card)
            prices = get_prices_for_card(firefox, card)
