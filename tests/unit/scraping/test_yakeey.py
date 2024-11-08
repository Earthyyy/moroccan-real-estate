import os
import sys

import pytest

from tests.unit.conftest import make_response

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import var_yakeey as vy


@pytest.fixture(scope="module")
def vcr_cassette_dir():
    return os.path.join("tests", "unit", "scraping", "cassettes", "yakeey")


@pytest.mark.vcr
def test_is_announcement_valid(yakeey_spider):
    response = make_response(vy.YAKEEY_PAGES[1])
    announcements_a = response.css("div.mui-4oo2hv a")
    for test in [
        *vy.YAKEEY_ANNOUNCEMENTS[:-1],
        vy.YAKEEY_ANNOUNCEMENT_NEUF_1,
        vy.YAKEEY_ANNOUNCEMENT_NEUF_2,
    ]:
        assert (
            yakeey_spider.is_announcement_valid(announcements_a[test["position"]])
            == test["is_valid"]
        )


@pytest.mark.vcr
def test_get_info_from_announcement_a(yakeey_spider):
    response = make_response(vy.YAKEEY_PAGES[1])
    announcements_a = response.css("div.mui-4oo2hv a")
    for test in vy.YAKEEY_ANNOUNCEMENTS[:-1]:
        assert (
            yakeey_spider.get_info_from_announcement_a(
                announcements_a[test["position"]]
            )
            == test["info"]
        )


@pytest.mark.vcr
@pytest.mark.parametrize(
    ("index", "expected_index"), [(1, 2), (2, 3), (15, 16), (33, 34), (34, 35)]
)
def test_get_next_page_url(yakeey_spider, index: int, expected_index: int):
    response = make_response(vy.YAKEEY_PAGES[index])
    assert yakeey_spider.get_next_page_url(response) == (
        vy.YAKEEY_PAGES.get(expected_index, None)
    )


# Tests based on the announcement's page


@pytest.mark.vcr
@pytest.mark.parametrize(
    "index",
    range(len(vy.YAKEEY_ANNOUNCEMENTS)),
)
def test_get_header(yakeey_spider, index: int):
    response = make_response(vy.YAKEEY_ANNOUNCEMENTS[index]["url"])
    assert yakeey_spider.get_header(response) == (
        vy.YAKEEY_ANNOUNCEMENTS[index]["header"]
    )


@pytest.mark.vcr
@pytest.mark.parametrize(
    "index",
    range(len(vy.YAKEEY_ANNOUNCEMENTS)),
)
def test_get_attributes(yakeey_spider, index: int):
    response = make_response(vy.YAKEEY_ANNOUNCEMENTS[index]["url"])
    assert yakeey_spider.get_attributes(response) == (
        vy.YAKEEY_ANNOUNCEMENTS[index]["attributes"]
    )


@pytest.mark.vcr
@pytest.mark.parametrize(
    "index",
    range(len(vy.YAKEEY_ANNOUNCEMENTS)),
)
def test_get_equipments(yakeey_spider, index: int):
    response = make_response(vy.YAKEEY_ANNOUNCEMENTS[index]["url"])
    assert yakeey_spider.get_equipments(response) == (
        vy.YAKEEY_ANNOUNCEMENTS[index]["equipments"]
    )
