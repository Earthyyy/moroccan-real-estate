from typing import Dict, List, Tuple

import pytest

from tests.unit import conftest

# Tests based on the announcements listing page


@pytest.mark.vcr
def test_is_announcement_valid(avito_spider, get_announcements_a):
    announcements_a = get_announcements_a
    for test in [*conftest.AVITO_ANNOUNCEMENTS, conftest.AVITO_ANNOUNCEMENT_IMMONEUF]:
        assert (
            avito_spider.is_announcement_valid(announcements_a[test["index"]])
            == test["is_valid"]
        )


@pytest.mark.vcr
def test_get_info_from_announcement_a(avito_spider, get_announcements_a):
    announcements_a = get_announcements_a
    for test in conftest.AVITO_ANNOUNCEMENTS:
        assert (
            avito_spider.get_info_from_announcement_a(announcements_a[test["index"]])
            == test["info"]
        )


@pytest.mark.vcr
@pytest.mark.parametrize(
    ("url", "expected_url"),
    [
        (conftest.AVITO_PAGE_1, conftest.AVITO_PAGE_2),
        (conftest.AVITO_PAGE_2, conftest.AVITO_PAGE_3),
        (conftest.AVITO_PAGE_500, conftest.AVITO_PAGE_501),
        (conftest.AVITO_PAGE_1000, conftest.AVITO_PAGE_1001),
        (conftest.AVITO_PAGE_BEFORE_LAST, conftest.AVITO_PAGE_LAST),
        (conftest.AVITO_PAGE_LAST, None),
    ],
)
def test_get_next_page_url(avito_spider, url: str, expected_url: str):
    response = conftest.make_response(url)
    assert avito_spider.get_next_page_url(response) == expected_url


# Tests based on the announcement's page


@pytest.mark.vcr
@pytest.mark.parametrize(
    ("url", "expected"),
    [(test["url"], test["header"]) for test in conftest.AVITO_ANNOUNCEMENTS],
)
def test_get_header(avito_spider, url: str, expected: Tuple[str, str, str, str, str]):
    response = conftest.make_response(url)
    assert avito_spider.get_header(response) == expected


@pytest.mark.vcr
@pytest.mark.parametrize(
    ("url", "expected"),
    [(test["url"], test["attributes"]) for test in conftest.AVITO_ANNOUNCEMENTS],
)
def test_get_attributes(avito_spider, url: str, expected: Dict[str, str]):
    response = conftest.make_response(url)
    assert avito_spider.get_attributes(response) == expected


@pytest.mark.vcr
@pytest.mark.parametrize(
    ("url", "expected"),
    [(test["url"], test["equipments"]) for test in conftest.AVITO_ANNOUNCEMENTS],
)
def test_get_equipments(avito_spider, url: str, expected: List[str]):
    response = conftest.make_response(url)
    assert avito_spider.get_equipments(response) == expected
