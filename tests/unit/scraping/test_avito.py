import pytest
from tests.unit.scraping.conftest_scraping import *
from typing import Dict, List, Tuple 

# Tests based on the announcements listing page

@pytest.mark.vcr()
def test_is_announcement_valid(avito_spider, get_announcements_a,):
    announcements_a = get_announcements_a
    for test in AVITO_ANNOUNCEMENTS + [AVITO_ANNOUNCEMENT_IMMONEUF]:
        assert avito_spider.is_announcement_valid(announcements_a[test["index"]]) == test["is_valid"]

@pytest.mark.vcr()
def test_get_info_from_announcement_a(avito_spider, get_announcements_a):
    announcements_a = get_announcements_a
    for test in AVITO_ANNOUNCEMENTS:
        assert avito_spider.get_info_from_announcement_a(announcements_a[test["index"]]) == test["info"]

@pytest.mark.vcr()
@pytest.mark.parametrize("url, expected_url", [
    (AVITO_PAGE_1, AVITO_PAGE_2),
    (AVITO_PAGE_2, AVITO_PAGE_3),
    (AVITO_PAGE_500, AVITO_PAGE_501),
    (AVITO_PAGE_1000, AVITO_PAGE_1001),
    (AVITO_PAGE_BEFORE_LAST, AVITO_PAGE_LAST),
    (AVITO_PAGE_LAST, None)
])
def test_get_next_page_url(avito_spider, url: str, expected_url: str):
    response = make_response(url)
    assert avito_spider.get_next_page_url(response) == expected_url

# Tests based on the announcement's page

@pytest.mark.vcr()
@pytest.mark.parametrize("url, expected", [(test["url"], test["header"]) for test in AVITO_ANNOUNCEMENTS])
def test_get_header(avito_spider, url: str, expected: Tuple[str, str, str, str, str]):
    response = make_response(url)
    assert avito_spider.get_header(response) == expected

@pytest.mark.vcr()
@pytest.mark.parametrize("url, expected", [(test["url"], test["attributes"]) for test in AVITO_ANNOUNCEMENTS])
def test_get_attributes(avito_spider, url: str, expected: Dict[str, str]):
    response = make_response(url)
    assert avito_spider.get_attributes(response) == expected

@pytest.mark.vcr()
@pytest.mark.parametrize("url, expected", [(test["url"], test["equipments"]) for test in AVITO_ANNOUNCEMENTS])
def test_get_equipments(avito_spider, url: str, expected: List[str]):
    response = make_response(url)
    assert avito_spider.get_equipments(response) == expected
