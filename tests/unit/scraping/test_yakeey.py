import os
import sys
from typing import Dict, List, Tuple

import pytest

from tests.unit.conftest import make_response

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import var_yakeey as vy

# Tests based on the announcements listing page

@pytest.mark.skip
@pytest.mark.vcr
def test_is_announcement_valid(avito_spider): # TODO: fix this test
    response = make_response(vy.AVITO_PAGE_1)
    announcements_a = response.css("div.sc-1nre5ec-1 a")
    assert True

@pytest.mark.vcr
@pytest.mark.parametrize(
    ("url", "expected_url"),
    [
        (vy.YAKEEY_PAGE_1, vy.YAKEEY_PAGE_2),
        (vy.YAKEEY_PAGE_2, vy.YAKEEY_PAGE_3),
        (vy.YAKEEY_PAGE_15, vy.YAKEEY_PAGE_16),
        (vy.YAKEEY_PAGE_BEFORE_LAST, vy.YAKEEY_PAGE_LAST),
        (vy.YAKEEY_PAGE_LAST, None),
    ],
)
def test_get_next_page_url(yakeey_spider, url: str, expected_url: str):
    response = make_response(url)
    assert yakeey_spider.get_next_page_url(response) == expected_url


# Tests based on the announcement's page
