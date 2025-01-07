from contextlib import nullcontext as does_not_raise
from datetime import date

import pytest


from google_books.utils import (
    create_directory,
    create_shipment_directory,
    fh_date,
    shipment_date_obj,
)
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


def test_create_dir_with_path_obj(tmp_path):
    output = create_directory(tmp_path, "foo")
    assert output == tmp_path / "foo"


def test_create_dir_with_str(tmp_path):
    parent_str = str(tmp_path)
    assert isinstance(parent_str, str)
    output = create_directory(parent_str, "foo")
    assert output == tmp_path / "foo"


def test_create_dir_exists(tmp_path):
    d = tmp_path / "foo"
    d.mkdir()
    assert d.exists()
    with does_not_raise():
        output = create_directory(tmp_path, "foo")
    assert output == d


def test_create_shipment_directory(tmp_path):
    d = create_shipment_directory("20241231", tmp_path)
    assert d.exists()
    assert d == tmp_path / "2024-12-31"


@pytest.mark.parametrize(
    "arg,expectation",
    [("20241201", date(2024, 12, 1)), ("241231", date(2024, 12, 31))],
)
def test_shipment_date_obj_success(arg, expectation):
    assert shipment_date_obj(arg) == expectation


@pytest.mark.parametrize(
    "arg", [None, {}, "2412319", "NYPL_240816.xml", "nypl_2024-08-12.xml", "foo.xml"]
)
def test_shipment_date_obj_type_error(arg):
    with pytest.raises(FileNameError):
        shipment_date_obj(arg)
