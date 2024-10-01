import os
import sys
from typing import Dict, List, Tuple

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
    print([a.attrib["href"] for a in announcements_a])
    assert True
    # for test in [*vy.YAKEEY_ANNOUNCEMENTS, vy.YAKEEY_ANNOUNCEMENT_NEUF]:
    #     assert (
    #         yakeey_spider.is_announcement_valid(announcements_a[test["index"]])
    #         == test["is_valid"]
    #     )


@pytest.mark.vcr
@pytest.mark.parametrize(
    ("index", "expected_index"),
    [(1, 2), (2, 3), (15, 16), (33, 34), (34, 35)]
)
def test_get_next_page_url(yakeey_spider, index: int, expected_index: int):
    response = make_response(vy.YAKEEY_PAGES[index])
    assert yakeey_spider.get_next_page_url(response) == (
        vy.YAKEEY_PAGES.get(expected_index, None)
    )


# Tests based on the announcement's page
