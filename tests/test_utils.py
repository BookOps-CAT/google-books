from contextlib import nullcontext as does_not_raise
import csv
from datetime import date
import warnings

import pytest


from google_books.utils import (
    get_directory,
    fh_date,
    save2csv,
    shipment_date_obj,
    timestamp_str2date,
)
from google_books.errors import FileNameError, GoogleBooksToolError


def test_save2csv(tmp_path):
    row = ["foo", "bar"]
    fh = tmp_path / "save2cvs-test.csv"
    with does_not_raise():
        save2csv(fh, delimiter=",", row=row)
    assert fh.exists()
    with open(fh, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = []
        for row in reader:
            rows.append(row)
    assert len(rows) == 1
    assert rows[0] == ["foo", "bar"]


def test_save2csv_unicode_encode_error(tmp_path):
    row = ["foo", "\ud83d\udca9"]
    fh = tmp_path / "save2csv-test.csv"

    with pytest.warns(UserWarning) as wrn:
        save2csv(fh, ",", row)

    assert wrn[0].message.args[0] == f"Could not write `foo` to {fh}"


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
    output = get_directory(tmp_path, "foo")
    assert output == tmp_path / "foo"


def test_create_dir_with_str(tmp_path):
    parent_str = str(tmp_path)
    assert isinstance(parent_str, str)
    output = get_directory(parent_str, "foo")
    assert output == tmp_path / "foo"


def test_create_dir_exists(tmp_path):
    d = tmp_path / "foo"
    d.mkdir()
    assert d.exists()
    with does_not_raise():
        output = get_directory(tmp_path, "foo")
    assert output == d


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


def test_timestamp_str2date_success():
    assert timestamp_str2date("2024/10/17 23:39") == date(2024, 10, 17)


@pytest.mark.parametrize("arg", [None, 123, "1969-07-21 T 02:56"])
def test_timestamp_str2date_exceptions(arg):
    with pytest.raises(GoogleBooksToolError) as exc:
        timestamp_str2date(arg)
    assert f"Error. Encountered invalid timestamp: `{arg}`." in str(exc.value)
