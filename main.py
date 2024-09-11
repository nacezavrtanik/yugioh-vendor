import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from firefox import firefox_instance

RABBIT = (
    "https://www.cardmarket.com/en/YuGiOh/Products/Singles/"
    "The-Infinite-Forbidden/"
    "Silhouhatte-Rabbit-V1-Secret-Rare"
)
VAMPIRE_LORD = (
    "https://www.cardmarket.com/en/YuGiOh/Products/Singles/"
    "Dark-Crisis/"
    "Vampire-Lord-V2-Secret-Rare"
)
BREAKER = (
    "https://www.cardmarket.com/en/YuGiOh/Products/Singles/"
    "Magicians-Force/"
    "Breaker-the-Magical-Warrior"
)

CARD = BREAKER

entry_xpath = "//div[@class='row g-0 article-row']"
with firefox_instance() as firefox:
    firefox.get(CARD)
    elements = firefox.find_elements(By.XPATH, entry_xpath)
    for element in elements:
        seller_xpath = ".//span[@class='seller-name d-flex']/span[3]"
        seller = element.find_element(By.XPATH, seller_xpath).text

        condition_xpath = ".//span[@class='badge ']"
        condition = element.find_element(By.XPATH, condition_xpath).text

        language_xpath = ".//div[@class='product-attributes col']/span"
        language_element = element.find_element(By.XPATH, language_xpath)
        language = language_element.get_attribute("aria-label")

        price_xpath = ".//div[@class='col-offer col-auto']//span"
        price = element.find_element(By.XPATH, price_xpath).text

        comment_xpath = ".//div[@class='product-comments me-1 col']"
        try:
            comment = element.find_element(By.XPATH, comment_xpath).text
        except NoSuchElementException:
            comment = ""

        attrs = seller, condition, language, price, comment
        print(attrs)
