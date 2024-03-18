from google_books.hathi_processor import google_reconciliation_to_barcodes_lst


def test_google_reconciliation_to_barcodes_lst():
    sample_report = "tests/google-reconciliation-FO-report-sample.txt"
    assert google_reconciliation_to_barcodes_lst(sample_report) == [
        "33433004338053",
        "33433004727081",
    ]
