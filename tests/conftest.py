import pytest
from scrapy.http import HtmlResponse
from scrapy.selector.unified import Selector
import requests

import sys
import os

# Add the project's root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraping.spiders.avito import AvitoSpider

# A user agent is needed to make requests to the website.

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Avito

# Requests to the following URLs are cached in tests/scraping/cassettes, if these caches are deleted, links might not work as the information is constantly changing.
# for example, the last page of the announcements is 1359, but it might change in the future, as well as announcements within the pages, or information in an announcement.

AVITO_PAGE_1 = "https://www.avito.ma/fr/maroc/appartements-à_vendre"
AVITO_PAGE_2 = "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=2"
AVITO_PAGE_3 = "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=3"
AVITO_PAGE_500 = "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=500"
AVITO_PAGE_501 = "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=501"
AVITO_PAGE_1000 = "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=1000"
AVITO_PAGE_1001 = "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=1001"
AVITO_PAGE_BEFORE_LAST =  "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=1359"
AVITO_PAGE_LAST = "https://www.avito.ma/fr/maroc/appartements-à_vendre?o=1360"
AVITO_ANNOUNCEMENT = ""

# Defining fixtures and utility functions

def make_response(url: str) -> HtmlResponse:
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    body = response.content
    return HtmlResponse(url=url, body=body)

@pytest.fixture
def avito_spider():
    return AvitoSpider()

@pytest.fixture
def get_announcements_a() -> Selector:
    response = make_response(AVITO_PAGE_1)
    return response.css("div.sc-1nre5ec-1 a")

# Yakeey
