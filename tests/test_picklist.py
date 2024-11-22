import pytest

from google_books.picklist import (
    is_oversized,
    too_tall,
    too_wide,
    too_thick,
    get_number_of_linked_bibs,
    get_clean_bib_values,
)


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("", False),  # when no data let pickers decide
        ("8vo.", False),
        ("4̊ .", False),
        ("24 cm.", False),
        ("24cm.", False),
        ("32 cm.", True),
        ("33 x 34 cm.", True),
        ("42x54 cm.", True),
        ("22 x 32 cm.", False),
        ("22 x 33-35 x 15 cm", False),
        ("27-36 cm.", False),
        ("34-12 cm.", True),
    ],
)
def test_too_tall(arg, expectation):
    assert too_tall(arg) == expectation


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("", False),
        ("24 cm.", False),
        ("32 cm.", False),
        ("48 cm.", False),
        ("24 x 32 cm.", False),
        ("24 x 46 cm.", True),
        ("24 x 47 cm.", True),
        ("24x46 cm.", True),
        ("21-23cm.", False),  # range of sizes in multi-volume sets
        (
            "24-46 cm.",
            False,
        ),  # some vols. eligible for scanning; pickers will decide
    ],
)
def test_too_wide(arg, expectation):
    assert too_wide(arg) == expectation


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("", False),
        ("24 cm.", False),
        ("32 cm.", False),
        ("33 x 47 x 10 cm.", False),
        ("10 x 15 x 13 cm.", True),
        ("22 x 28-33 x 25 cm", True),
    ],
)
def test_too_thick(arg, expectation):
    assert too_thick(arg) == expectation


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("", False),  # when no data let pickers decide
        ("24 cm.", False),
        ("32 cm.", True),
        ("31 x 35 cm", False),
        ("33 x 14 cm.", True),
        ("22 x 46 cm.", True),
        ("10 x 15 x 11 cm.", False),
        ("10 x 15 x 13 cm.", True),
    ],
)
def test_is_oversized(arg, expectation):
    assert is_oversized(arg) == expectation


@pytest.mark.parametrize(
    "arg,expectation",
    [(["foo"] * 14, 0), (["foo"] * 23, 1), (["foo"] * 31, 2), (["foo"] * 39, 3)],
)
def test_get_number_of_linked_bibs(arg, expectation):
    assert get_number_of_linked_bibs(arg) == expectation


def test_get_number_of_linked_bibs_real_data_single_bib(stub_row_one_bib):
    assert get_number_of_linked_bibs(stub_row_one_bib) == 1


def test_get_number_of_linked_bibs_real_data_linked_bibs(stub_row_linked_bibs):
    assert get_number_of_linked_bibs(stub_row_linked_bibs) == 2


def test_get_clean_bib_values_single_bib(stub_row_one_bib):
    assert get_clean_bib_values(stub_row_one_bib, 1) == [
        "u",
        "1888",
        "9999",
        "25 cm.",
        "Report of meeting.",
        "Sydney : [The Association], 1888-",
        "*EC.A939",
        "*EC.A939",
    ]


def test_get_clean_bib_values_linked_bibs(stub_row_linked_bibs):
    assert get_clean_bib_values(stub_row_linked_bibs, 2) == [
        "c",
        "1965",
        "19uu",
        "",
        "Supplementary volume.",
        "Cambridge, Eng.: Trinity College.",
        "L-10 9215 Library has: 1-24 (Incomplete). Some vols. classed separately.",
        "L-10 9215 Library has: 1-24 (Incomplete). Some vols. classed separately.",
    ]
