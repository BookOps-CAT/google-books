import pytest

from pymarc import Record, Field, Subfield

from google_books.marc_manipulator import (
    find_oclcno,
    fix_oclc_info,
    get_bibs,
    is_item_field,
    marcxml_reader,
)


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


def test_fix_oclc_info_warning_no_oclcno_found(stub_bib):
    with pytest.warns(UserWarning) as wrn:
        fix_oclc_info(stub_bib)

    assert (
        "Unable to manipulate bib (.b00000001). No suitable OCLC # was found in bib."
        in str(wrn[-1].message)
    )


def test_fix_oclc_info_success(stub_bib):
    stub_bib.add_field(
        Field(
            tag="035", indicators=[" ", " "], subfields=[Subfield("a", "(OCoLC)1234")]
        )
    )
    stub_bib.add_field(
        Field(tag="991", indicators=[" ", " "], subfields=[Subfield("y", "1234")])
    )
    stub_bib.add_field(
        Field(tag="997", indicators=[" ", " "], subfields=[Subfield("a", "foo")])
    )
    stub_bib.add_field(
        Field(tag="959", indicators=[" ", " "], subfields=[Subfield("a", "bar")])
    )
    stub_bib.add_field(
        Field(tag="910", indicators=[" ", " "], subfields=[Subfield("a", "RL")])
    )
    fix_oclc_info(stub_bib)

    assert str(stub_bib["001"]) == "=001  1234"
    assert str(stub_bib["003"]) == "=003  OCoLC"
    assert str(stub_bib["945"]) == "=945  \\\\$a.b00000001"
    assert str(stub_bib["949"]) == "=949  \\\\$a*bn=xxx;"
    assert "991" not in stub_bib
    assert "997" not in stub_bib
    assert "959" not in stub_bib
    assert "910" not in stub_bib


def test_get_bibs_yield_record_sequence_in_file():
    reader = get_bibs("tests/sample-rlin-bibs.mrc")
    n, bib = next(reader)
    assert n == 1
    assert isinstance(bib, Record)


@pytest.mark.parametrize(
    "tag,subfields,expectation",
    [
        ("900", [Subfield("a", "foo"), Subfield("y", "bar")], False),
        ("945", [Subfield("a", "foo")], False),
        ("945", [Subfield("a", "foo"), Subfield("y", "bar")], True),
    ],
)
def test_is_item_field(tag, subfields, expectation):
    field = Field(tag=tag, indicators=[" ", " "], subfields=subfields)
    assert is_item_field(field) == expectation


def test_marcxml_reader():
    test_file = "tests/marcxml-sample.xml"
    bibs = marcxml_reader(test_file)
    for n, bib in enumerate(bibs):  # n starts with 0!
        assert isinstance(bib, Record)
    assert n == 1
