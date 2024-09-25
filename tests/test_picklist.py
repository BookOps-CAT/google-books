import pytest

from google_books.picklist import is_oversized


@pytest.mark.parametrize("arg,expectation", [("24 cm.", False), ("32 cm.", True)])
def test_is_oversized(arg, expectation):
    assert is_oversized(arg) == expectation
