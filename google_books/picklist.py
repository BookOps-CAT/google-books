"""
A module with methods to unpack Google Candidate List and create
NYPL pick list.
"""

import csv
import glob
import tarfile
from itertools import islice
import re

from google_books.utils import fh_date, save2csv


def extract_candidate_list(tar_file: str) -> None:
    """
    Extracts the candidate list from the tar file.

    Args:
        tar_file (str): The tar file containing the candidate list.
    """
    with tarfile.open(tar_file, "r") as tar:
        tar.extractall("files/picklist")


def prep_item_list_for_sierra(tar_file: str, list_size: int) -> None:
    """
    Prepares the item list for Sierra based on Google Candidate list _combined tar file.
    Creates `nypl-YYYY-MM-DD-candidate-items.csv` file with item numbers in the
    `picklist` folder.

    Args:
        tar_file (str): The tar file containing the candidate list.
        list_size (int): The number of items to include in the list.
    """
    date = fh_date(tar_file)

    extract_candidate_list(tar_file)

    # read each extracted .txt file, find item #, and write it to a new file
    files = glob.glob("files/picklist/*_combined-*.txt")
    n = -1
    s = 1
    print(f"Outputting to file: {str(s).zfill(3)}...")
    for f in files:
        reader = csv.reader(open(f, "r", encoding="utf-8"), delimiter="\t")
        for row in reader:
            n += 1
            if n >= list_size:
                n = 0
                s += 1
                print(f"Outputting to file: {str(s).zfill(3)}...")
            item = row[1][1:]
            out = f"files/picklist/nypl-{date}-candidate-items-{str(s).zfill(3)}.csv"
            save2csv(out, ",", [item])


def too_tall(value: str) -> bool:
    """
    Checks if the height of the item is 32 cm or above per Google guidelines.

    Args:
        value (str): The value of the 300 $c
    """
    pattern = re.compile(r"^(\d{1,2})(.*)")
    if match := pattern.match(value):
        return int(match.group(1)) >= 32
    return False


def too_wide(value: str) -> bool:
    """
    Checks if the width of the item is 24 cm or above per Google guidelines.

    Args:
        value (str): The value of the 300 $c
    """
    pattern = re.compile(r"^(.*x\s?)(\d{1,2})(.*)")
    if match := pattern.match(value):
        return int(match.group(2)) >= 46
    return False


def too_thick(value: str) -> bool:
    """
    Checks if the thickness of the item is 13 cm or above per Google guidelines.

    Args:
        value (str): The value of the 300 $c
    """
    pattern = re.compile(r"^(.*x.*x\s)(\d{1,2})(.*)")
    if match := pattern.match(value):
        return int(match.group(2)) >= 13
    return False


def is_oversized(value: str) -> bool:
    """
    Checks if extend in 300 $c indicates oversized item that Google won't be able
    to scan.
        + length is 46 cm or above
        + thickness is 13 cm or above

    Args:
        value (str): The value of the 300 $c
    """

    results = []
    results.append(too_tall(value))
    results.append(too_wide(value))
    results.append(too_thick(value))

    return any(results)


def prep_sierra_export_for_dataframe(fh: str, date: str) -> None:
    """
    Transforms a given Sierra export file to a format that can be used to create
    `pandas.DataFrame` object. Will append data to the out file if already exists.

    Args:
        fh (str): The path to the Sierra export file
        date (str): The date of the export in the format YYYY-MM-DD
    """
    with open(fh, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
        next(reader)  # skip the header
        for row in reader:
            try:
                assert len(row[14:]) % 8 == 0
            except AssertionError:
                save2csv(
                    f"files/picklist/candidates-siera-export-longrows-{date}.csv",
                    "\t",
                    [row[0], len(row), len(row[14])],
                )
            new_row = row[:14]
            oversized = str(is_oversized(row[19]))
            new_row.append(oversized)
            linked_bibs_no = int(len(row[14:]) / 8)

            # move clean_bib_values to its own function for testing
            try:
                clean_bib_values = [
                    i for i in islice(row[14:], 0, None, linked_bibs_no)
                ]
            except ValueError:
                print(f"Error in {row[0]}. Step: {linked_bibs_no}")
                raise
            new_row.extend(clean_bib_values)
            save2csv(
                f"files/picklist/candidates-sierra-export-clean-{date}.csv",
                "\t",
                new_row,
            )
