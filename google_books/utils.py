import csv
from datetime import datetime
from pathlib import Path
import re
from typing import Optional
import warnings


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


def create_directory(dir_parent: Path, dir_name: str) -> None:
    dir_path = Path(dir_parent).joinpath(dir_name)
    dir_path.mkdir()


def fh_date(fh: str) -> Optional[str]:
    """
    Determines date element in the given file name

    Args:
        fh: str, file handle
    """
    fh_name = Path(fh).stem
    pattern = re.compile(r"(\D)(\d{8})(\D|$)")
    match = re.search(pattern, fh_name)
    if match:
        return match.group(2)
    else:
        return None
