"""Global variables and fixtures for the scraping tests."""

import pytest
import requests
from scrapy.http import HtmlResponse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

@pytest.fixture
def make_response(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    body = response.content
    return HtmlResponse(url=url, body=body)


# Avito

AVITO_PAGE_1 = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre"
AVITO_PAGE_2 = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?o=2"
AVITO_PAGE_3 = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?o=3"
AVITO_PAGE_500 = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?o=500"
AVITO_PAGE_501 = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?o=501"
AVITO_PAGE_1000 = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?o=1000"
AVITO_PAGE_1001 = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?o=1001"
AVITO_PAGE_BEFORE_LAST =  "https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?o=1360"
AVITO_PAGE_LAST = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?o=1361"

