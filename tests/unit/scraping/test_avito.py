import os
import sys
from typing import Dict, List

import pytest

from tests.unit.conftest import make_response

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import var_avito as va

# Tests based on the announcements listing page


@pytest.fixture(scope="module")
def vcr_cassette_dir():
    return os.path.join("tests", "unit", "scraping", "cassettes", "avito")


@pytest.mark.vcr
def test_is_announcement_valid(avito_spider):
    response = make_response(va.AVITO_PAGES[1])
    announcements_a = response.css("div.sc-1nre5ec-1 a")
    for test in [*va.AVITO_ANNOUNCEMENTS, va.AVITO_ANNOUNCEMENT_IMMONEUF]:
        assert (
            avito_spider.is_announcement_valid(announcements_a[test["position"]])
            == test["is_valid"]
        )


@pytest.mark.vcr
def test_get_info_from_announcement_a(avito_spider):
    response = make_response(va.AVITO_PAGES[1])
    announcements_a = response.css("div.sc-1nre5ec-1 a")
    for test in va.AVITO_ANNOUNCEMENTS:
        assert (
            avito_spider.get_info_from_announcement_a(announcements_a[test["position"]])
            == test["info"]
        )


@pytest.mark.vcr
@pytest.mark.parametrize(
    ("index", "expected_index"),
    [(1, 2), (2, 3), (500, 501), (1000, 1001), (1359, 1360), (1360, 1361)],
)
def test_get_next_page_url(avito_spider, index: int, expected_index: int):
    response = make_response(va.AVITO_PAGES[index])
    assert avito_spider.get_next_page_url(response) == (
        va.AVITO_PAGES.get(expected_index, None)
    )


# Tests based on the announcement's page


@pytest.mark.vcr
@pytest.mark.parametrize(
    "index",
    range(len(va.AVITO_ANNOUNCEMENTS)),
)
def test_get_header(avito_spider, index: int):
    response = make_response(va.AVITO_ANNOUNCEMENTS[index]["url"])
    assert avito_spider.get_header(response) == (
        va.AVITO_ANNOUNCEMENTS[index]["header"]
    )


@pytest.mark.vcr
@pytest.mark.parametrize(
    "index",
    range(len(va.AVITO_ANNOUNCEMENTS)),
)
def test_get_attributes(avito_spider, index: int):
    response = make_response(va.AVITO_ANNOUNCEMENTS[index]["url"])
    assert avito_spider.get_attributes(response) == (
        va.AVITO_ANNOUNCEMENTS[index]["attributes"]
    )


@pytest.mark.vcr
@pytest.mark.parametrize(
    "index",
    range(len(va.AVITO_ANNOUNCEMENTS)),
)
def test_get_equipments(avito_spider, index: int):
    response = make_response(va.AVITO_ANNOUNCEMENTS[index]["url"])
    assert avito_spider.get_equipments(response) == (
        va.AVITO_ANNOUNCEMENTS[index]["equipments"]
    )
