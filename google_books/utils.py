import csv
import datetime
from pathlib import Path
import re
from typing import Optional, Union
import warnings

from .errors import FileNameError


def save2csv(dst_fh, delimiter, row):
    """
    Appends a list with data to a dst_fh csv
    args:
        dst_fh: str, output file
        row: list, list of values to write in a row
    """

    with open(dst_fh, "a", encoding="utf-8") as csvfile:
        out = csv.writer(
            csvfile,
            delimiter=delimiter,
            lineterminator="\n",
            quotechar="@",
            quoting=csv.QUOTE_MINIMAL,
        )
        try:
            out.writerow(row)
        except UnicodeEncodeError:
            warnings.warn(f"Could not write {row[0]} to {dst_fh}")


def create_directory(dir_parent: Union[str, Path], dir_name: str) -> Path:
    dir_path = Path(dir_parent).joinpath(dir_name)
    try:
        dir_path.mkdir()
    except FileExistsError:
        pass
    return dir_path


def create_shipment_directory(
    shipment_date: str, parent_dir: str = "files/shipments"
) -> Path:
    date = shipment_date_obj(shipment_date)
    ship_dir = create_directory(Path(parent_dir), f"{date:%Y-%m-%d}")
    return ship_dir


def fh_date(fh: Union[str, Path]) -> Optional[str]:
    """
    Determines date element in the given file name

    Args:
        fh: str, file handle
    """
    if isinstance(fh, str):
        fh_path = Path(fh)
    fh_name = fh_path.stem
    pattern = re.compile(r"(\D)(\d{8})(\D|$)")
    match = re.search(pattern, fh_name)
    if match:
        return match.group(2)
    else:
        return None


def shipment_date_obj(shipment_date: str) -> datetime.date:
    """
    Converts date element of the file name into a `datetime.date` instance

    Args:
        date_str: shipments date as a str in 'YYYYMMDD' format

    Returns:
        `datetime.date` instance
    """
    try:
        if len(shipment_date) == 8:
            return datetime.datetime.strptime(shipment_date, "%Y%m%d").date()
        elif len(shipment_date) == 6:
            return datetime.datetime.strptime(shipment_date, "%y%m%d").date()
        else:
            raise ValueError
    except (TypeError, ValueError):
        raise FileNameError(
            "Given file handle has incorrectly coded date. Format should be: "
            "YYYYMMDD."
        )
