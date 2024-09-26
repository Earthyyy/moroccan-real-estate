import pytest
from scrapy.http import HtmlResponse
from scrapy.selector.unified import Selector
import requests

import sys
import os

# Add the project's root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from scraping.spiders.avito import AvitoSpider

# A user agent is needed to make requests to the website.

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Avito

# Defining fixtures and utility functions

def make_response(url: str) -> HtmlResponse:
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    body = response.content
    return HtmlResponse(url=url, body=body)

@pytest.fixture
def avito_spider():
    return AvitoSpider

@pytest.fixture
def get_announcements_a() -> Selector:
    response = make_response(AVITO_PAGE_1)
    return response.css("div.sc-1nre5ec-1 a")

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

AVITO_ANNOUNCEMENT = {
    "index": 0,
    "url": "https://www.avito.ma/fr/autre_secteur/appartements/شقة_بواجهتين_بالقرب_من_ديكاتلون_فمنزل_R2__55576138.htm",
    "is_valid": True,
    "info": ("3", "3", "140 m²"),
    "header": (),
    "attributes": {},
    "equipments": []
}
AVITO_ANNOUNCEMENT_NO_EQUIPMENTS = {
    "index": 2,
    "url": "https://www.avito.ma/fr/oulfa/appartements/appartement_sourour_farah_salam__55440383.htm",
    "is_valid": True,
    "info": ("2", "1", "50 m²"),
    "header": (),
    "attributes": {},
    "equipments": []
}
AVITO_ANNOUNCEMENT_IMMONEUF = {
    "index": 4,
    "url": "https://immoneuf.avito.ma/fr/unite/jfU?utm_source=avito_integration&utm_medium=listing_integration",
    "is_valid": False,
    "info": None,
    "header": (),
    "attributes": {},
    "equipments": []
}
AVITO_ANNOUNCEMENT_NO_PRICE = {
    "index": 5,
    "url": "https://www.avito.ma/fr/sakar/appartements/appartement_avec_jardin__55576063.htm",
    "is_valid": True,
    "info": ("3", "2", "281 m²"),
    "header": (),
    "attributes": {},
    "equipments": []
}
AVITO_ANNOUNCEMENT_REQUIRED_ONLY = {
    "index": 11,
    "url": "https://www.avito.ma/fr/khemisset/appartements/Appartement_à_vendre_1_m²_à_Khemisset_55576049.htm",
    "is_valid": True,
    "info": ("1", None, None),
    "header": (),
    "attributes": {},
    "equipments": []
}
AVITO_ANNOUNCEMENT_OPTIONAL_ALL = {
    "index": 21,
    "url": "https://www.avito.ma/fr/saidia/appartements/Apparemment__saidia_ap2_al_waha_55208892.htm",
    "is_valid": True,
    "info": ("2", "2", "117 m²"),
    "header": (),
    "attributes": {},
    "equipments": []
}
AVITO_ANNOUNCEMENT_VERIFIED = {
    "index": 23,
    "url": "https://www.avito.ma/fr/2_mars/appartements/Appartement_Spacieux_à_vendre_147_m²_à_Casablanca__55393976.htm",
    "is_valid": True,
    "info": ("3", "2", "147 m²"),
    "header": (),
    "attributes": {},
    "equipments": []
}
AVITO_ANNOUNCEMENT_STAR = {
    "index": 27,
    "url": "https://www.avito.ma/fr/skikina/appartements/Appartement_à_vendre_105_m²_à_Temara_55562047.htm",
    "is_valid": True,
    "info": ("3", "2", "105 m²"),
    "header": (),
    "attributes": {},
    "equipments": []
}

AVITO_ANNOUNCEMENTS = [
    AVITO_ANNOUNCEMENT,
    AVITO_ANNOUNCEMENT_STAR,
    AVITO_ANNOUNCEMENT_VERIFIED,
    AVITO_ANNOUNCEMENT_REQUIRED_ONLY,
    AVITO_ANNOUNCEMENT_OPTIONAL_ALL,
    AVITO_ANNOUNCEMENT_NO_PRICE,
    AVITO_ANNOUNCEMENT_NO_EQUIPMENTS
]
