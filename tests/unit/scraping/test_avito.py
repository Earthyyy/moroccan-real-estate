import pytest
import requests
from scrapy.http import HtmlResponse

from scraping.spiders.avito import AvitoSpider

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

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

@pytest.fixture
def avito_spider():
    return AvitoSpider()

def make_response(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    body = response.content
    return HtmlResponse(url=url, body=body)

def test_parse_announcement():
    pass

def test_is_announcement_valid():
    pass

def test_get_info_from_announcement_a():
    pass

@pytest.mark.vcr()
@pytest.mark.parametrize("url, expected_url", [
    (AVITO_PAGE_1, AVITO_PAGE_2),
    (AVITO_PAGE_2, AVITO_PAGE_3),
    (AVITO_PAGE_500, AVITO_PAGE_501),
    (AVITO_PAGE_1000, AVITO_PAGE_1001),
    (AVITO_PAGE_BEFORE_LAST, AVITO_PAGE_LAST),
    (AVITO_PAGE_LAST, None)
])
def test_get_next_page_url(avito_spider, url, expected_url):
    response = make_response(url)
    assert avito_spider.get_next_page_url(response) == expected_url

def test_get_header():
    pass

def test_get_attributes():
    pass

def test_get_equipments():
    pass
