import requests
from firefox import firefox_instance

URL = (
    "https://www.cardmarket.com/en/YuGiOh/Products/Singles/"
    "The-Infinite-Forbidden/"
    "Silhouhatte-Rabbit-V1-Secret-Rare"
)

with firefox_instance() as firefox:
    firefox.get(URL)
    input()
