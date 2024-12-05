from contextlib import nullcontext as does_not_raise
from pathlib import Path
import pytest


from google_books.utils import create_directory, fh_date


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("files/shipments/2024-12-08/nyp_20231208_google.txt", "20231208"),
        ("files/shipments/20241208/nyp_20231208_google.txt", "20231208"),
        ("nyp_20240101_google_recap.txt", "20240101"),
        ("NYPL_20240131Recap.txt", "20240131"),
        ("NYPL_20240131-Recap.txt", "20240131"),
        ("SierraExport4Google_20240131.mrc", "20240131"),
        ("SierraExport4Google_202401316.mrc", None),
        ("files/shipments/20241208/google_export.txt", None),
    ],
)
def test_fh_date(arg, expectation):
    assert fh_date(arg) == expectation


def test_create_dir(tmp_path):
    with does_not_raise():
        create_directory(tmp_path, "foo")
