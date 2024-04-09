import pytest

from google_books.hathi_processor import (
    find_bibno,
    find_cid,
    find_err_msg,
    google_reconciliation_to_barcodes_lst,
)


@pytest.mark.parametrize(
    "arg",
    [
        "WARNING: .b12274570x (7472): no OCLC number in record",
        "ERROR 47: .b12274570x (7471): invalid recTyp: b, leader = '01249nbcaa2200349   4500'",
    ],
)
def test_find_bibno(arg):
    assert find_bibno(arg) == ".b12274570x"


def test_find_bibno_exception():
    with pytest.raises(ValueError) as exc:
        find_bibno("foo bar")

    assert "Invalid Sierra bib # encountered. Line: foo bar" in str(exc.value)


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
    sample_report = "tests/google-reconciliation-FO-report-sample.txt"
    assert google_reconciliation_to_barcodes_lst(sample_report) == [
        "33433004338053",
        "33433004727081",
    ]
