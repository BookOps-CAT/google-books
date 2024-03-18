import pytest


from google_books.utils import fh_date


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("nyp_20231208_google.txt", "20231208"),
        ("nyp_20240101_google_recap.txt", "20240101"),
    ],
)
def test_report_name_base_valid(arg, expectation):
    assert fh_date(arg) == expectation


@pytest.mark.parametrize(
    "arg",
    ["foo", "20231208_google.txt", "nyp_foo_google.txt", "nyp-20231208-google.txt"],
)
def test_report_name_base_invalid(arg):
    with pytest.raises(ValueError):
        fh_date(arg)
