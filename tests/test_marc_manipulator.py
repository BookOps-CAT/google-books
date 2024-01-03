import pytest

from pymarc import Field, Subfield

from google_books.marc_manipulator import find_oclcno


@pytest.mark.parametrize("arg,expectation", [("(OCoLC)1234", "1234"), ("1234", None)])
def test_find_oclcno_in_035(arg, expectation, stub_bib):
    stub_bib.add_field(
        Field(tag="035", indicators=[" ", " "], subfields=[Subfield("a", arg)])
    )
    assert find_oclcno(stub_bib) == expectation


@pytest.mark.parametrize("arg,expectation", [("1234", "1234"), (" 1234 ", "1234")])
def test_find_oclcno_in_991(arg, expectation, stub_bib):
    stub_bib.add_field(
        Field(tag="991", indicators=[" ", " "], subfields=[Subfield("y", arg)])
    )
    assert find_oclcno(stub_bib) == expectation


def test_find_oclcno_not_present(stub_bib):
    assert find_oclcno(stub_bib) is None


def test_find_oclcno_in_invalid_subfield_of_991(stub_bib):
    stub_bib.add_field(
        Field(tag="991", indicators=[" ", " "], subfields=[Subfield("a", "1234")])
    )
    assert find_oclcno(stub_bib) is None


def test_find_oclcno_invlid_oclcno_in_035(stub_bib):
    stub_bib.add_field(
        Field(
            tag="035",
            indicators=[" ", " "],
            subfields=[Subfield("a", "(OCoLC)nyp1234")],
        )
    )
    with pytest.warns(UserWarning) as wrn:
        find_oclcno(stub_bib)
    assert "Encountered invalid OCLC #: nyp1234." in str(wrn[-1].message)


def test_find_oclcno_invlid_oclcno_in_991(stub_bib):
    stub_bib.add_field(
        Field(
            tag="991",
            indicators=[" ", " "],
            subfields=[Subfield("y", "a1234")],
        )
    )
    with pytest.warns(UserWarning) as wrn:
        find_oclcno(stub_bib)
    assert "Encountered invalid OCLC #: a1234." in str(wrn[-1].message)
