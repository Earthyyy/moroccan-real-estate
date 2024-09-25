import pytest
import requests
from scrapy.http import HtmlResponse

from scraping.spiders.avito import AvitoSpider
from conftest import *

@pytest.fixture
def avito_spider():
    return AvitoSpider()

def test_parse_announcement():
    pass

def test_is_announcement_valid():
    pass

def test_get_info_from_announcement_a():
    pass

@pytest.mark.parametrize("url, expected", [
    (AVITO_PAGE_1, AVITO_PAGE_2),
    (AVITO_PAGE_2, AVITO_PAGE_3),
    (AVITO_PAGE_500, AVITO_PAGE_501),
    (AVITO_PAGE_1000, AVITO_PAGE_1001),
    (AVITO_PAGE_BEFORE_LAST, AVITO_PAGE_LAST)
])
def test_get_next_page_url(url, expected):
    pass

def test_get_header():
    pass

def test_get_attributes():
    pass

def test_get_equipments():
    pass
