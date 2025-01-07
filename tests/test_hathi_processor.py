from pathlib import Path
from datetime import date

import pytest

from google_books.hathi_processor import (
    find_bibno,
    find_cid,
    find_err_msg,
    google_reconciliation_to_barcodes_lst,
    get_hathi_meta_destination,
)


@pytest.mark.parametrize(
    "arg",
    [
        "WARNING: .b12274570x (7472): no OCLC number in record",
        "ERROR 47: .b12274570x (7471): invalid recTyp: b, leader = '01249nbcaa2200349   4500'",  # noqa: E501
    ],
)
def test_find_bibno(arg):
    assert find_bibno(arg) == "b12274570x"


def test_find_bibno_exception():
    with pytest.raises(ValueError) as exc:
        find_bibno("foo bar")

    assert "Invalid Sierra bib # encountered. Line: foo bar" in str(exc.value)


def test_find_cid():
    line = "INFO: 1: new cid = 103134087"
    assert find_cid(line) == "103134087"


def test_find_cid_value_error():
    with pytest.raises(ValueError) as exc:
        find_cid("INFO: 1: new cid = 10313408x")
    assert "Invalid Hathi CID encountered." in str(exc.value)


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("ERROR 47: .b103905054 (7249): err msg here\n", "err msg here"),
        ("WARNING: .b100146703 (5999): no OCLC number in record\n", ""),
    ],
)
def test_find_err_msg(arg, expectation):
    assert find_err_msg(arg) == expectation


def test_google_reconciliation_to_barcodes_lst():
    sample_report = Path("tests/_grin_query_sample.txt")
    assert google_reconciliation_to_barcodes_lst(sample_report) == sorted(
        ["33433124886338", "33433119947368", "33433116658661"]
    )


def test_get_hathi_meta_destination():
    ship_date = date(2024, 12, 31)
    assert get_hathi_meta_destination(ship_date) == Path(
        "files/shipments/2024-12-31/nyp_20241231_google.xml"
    )
