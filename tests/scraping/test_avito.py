import pytest
import requests
from scrapy.http import HtmlResponse
from scraping.spiders.avito import AvitoSpider

@pytest.fixture
def avito_spider():
    return AvitoSpider()

def make_response(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    body = response.content
    return HtmlResponse(url=url, body=body, encoding='utf-8')

@pytest.mark.vcr()
def test_get_announcement_urls(avito_spider):
    url = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre"
    response = make_response(url)
    urls = avito_spider.get_announcement_urls(response)
    assert len(urls) == 44