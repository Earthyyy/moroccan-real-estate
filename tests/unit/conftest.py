import os
import sys

import pytest
import requests
from scrapy.http import HtmlResponse

# add the project's root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.scraping.spiders.avito import AvitoSpider
from src.scraping.spiders.yakeey import YakeeySpider

# a user agent is needed to make requests to the website.

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


# define fixtures and utility functions


def make_response(url: str) -> HtmlResponse:
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    body = response.content
    return HtmlResponse(url=url, body=body)


@pytest.fixture
def avito_spider():
    return AvitoSpider()


@pytest.fixture
def yakeey_spider():
    return YakeeySpider()
