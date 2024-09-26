import pytest

from google_books.picklist import is_oversized


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("", False),  # when no data let pickers decide
        ("24 cm.", False),
        ("32 cm.", True),
        ("33 x 34 cm.", True),
        ("22 x 32 cm.", False),
        ("22 x 28-33 x 25 cm", True),
    ],
)
def test_is_oversized(arg, expectation):
    assert is_oversized(arg) == expectation
