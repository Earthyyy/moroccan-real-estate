import sys

sys.path.insert(
    0,
    "./src",
)

from src.example_1 import sub_version, sum_version


def test_sum_version():
    a = 1
    b = 2
    result = 3

    assert sum_version(a, b) == result


def test_sub_version():
    a = 3
    b = 1
    result = 2

    assert sub_version(a, b) == result
