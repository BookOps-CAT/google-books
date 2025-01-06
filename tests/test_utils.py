from contextlib import nullcontext as does_not_raise
from datetime import date

import pytest


from google_books.utils import create_directory, fh_date, shipment_date_obj
from google_books.errors import FileNameError


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("files/shipments/2024-12-08/nyp_20231208_google.txt", "20231208"),
        ("files/shipments/20241208/nyp_20231208_google.txt", "20231208"),
        ("nyp_20240101_google_recap.txt", "20240101"),
        ("C:/Users/foobar/documents/SierraExportManifest_20241231", "20241231"),
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


@pytest.mark.parametrize(
    "arg,expectation",
    [
        ("20241201", date(2024, 12, 1)),
    ],
)
def test_shipment_date_obj_success(arg, expectation):
    assert shipment_date_obj(arg) == expectation


@pytest.mark.parametrize(
    "arg", [None, {}, "241231", "NYPL_240816.xml", "nypl_2024-08-12.xml", "foo.xml"]
)
def test_shipment_date_obj_type_error(arg):
    with pytest.raises(FileNameError):
        shipment_date_obj(arg)
