import os
import sys
from datetime import datetime, timedelta

import pytest

from src.scraping.pipelines import AvitoTimePipeline
from tests.unit.conftest import make_response

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import var_avito as va

# Tests based on spider attributes


def test_set_recent_date(avito_spider):
    glob_path = "./tests/unit/data/raw/avito/*.json"
    assert avito_spider.set_recent_date(glob_path) == datetime(2024, 11, 30, 14, 44, 37)


# Tests based on the announcements listing page


@pytest.fixture(scope="module")
def vcr_cassette_dir():
    return os.path.join("tests", "unit", "scraping", "cassettes", "avito")


@pytest.mark.vcr
def test_is_announcement_valid(avito_spider):
    response = make_response(va.AVITO_PAGES[1])
    announcements_a = response.css("div.sc-1nre5ec-1 a")
    for test in [*va.AVITO_ANNOUNCEMENTS[:-1], va.AVITO_ANNOUNCEMENT_IMMONEUF]:
        assert (
            avito_spider.is_announcement_valid(announcements_a[test["position"]])
            == test["is_valid"]
        )


@pytest.mark.vcr
def test_get_info_from_announcement_a(avito_spider):
    response = make_response(va.AVITO_PAGES[1])
    announcements_a = response.css("div.sc-1nre5ec-1 a")
    for test in va.AVITO_ANNOUNCEMENTS[:-1]:
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


# Tests for the item pipeline


@pytest.mark.parametrize(
    ("time", "delta"),
    [
        ("il y a 1 minute", timedelta(minutes=1)),
        ("il y a 10 minutes", timedelta(minutes=10)),
        ("il y a 1 heure", timedelta(hours=1)),
        ("il y a 10 heures", timedelta(hours=10)),
        ("il y a 1 jour", timedelta(days=1)),
        ("il y a 10 jours", timedelta(days=10)),
        ("il y a 1 mois", timedelta(days=31)),
        ("il y a 10 mois", timedelta(days=10 * 31)),
        ("il y a 1 an", timedelta(days=365)),
        ("il y a 5 ans", timedelta(days=365 * 5)),
    ],
)
def test_get_absolute_time(time: str, delta: timedelta):
    expected_date = datetime.now() - delta
    assert AvitoTimePipeline.get_absolute_time(time) == (
        expected_date.strftime("%Y-%m-%d %H:%M"),
        expected_date.year,
        expected_date.month,
    )
