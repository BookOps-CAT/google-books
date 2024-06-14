"""
A module with methods to unpack Google Candidate List and create
NYPL pick list.
"""

import csv
import glob
import tarfile
from itertools import islice

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
    out = f"files/picklist/nypl-{date}-candidate-items.csv"

    extract_candidate_list(tar_file)

    # read each extracted .txt file, find item #, and write it to a new file
    files = glob.glob("files/picklist/*_combined-*.txt")
    n = 0
    f = 0
    for f in files:
        reader = csv.reader(open(f, "r", encoding="utf-8"), delimiter="\t")
        for row in reader:
            n = +1
            if n > list_size:
                n = 0
                f += 1
                print(f"Outputting to file -{str(f).zfill(1)}...")
            item = row[1][1:]
            out = f"files/picklist/nypl-{date}-candidate-items-{str(f).zfill(1)}.csv"
            save2csv(out, ",", [item])


def prep_sierra_export_for_dataframe(fh):
    with open(fh, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            try:
                assert len(row[14:]) % 7 == 0
            except AssertionError:
                print(row[0], len(row), len(row[14:]))
            linked_bibs_no = int(len(row[14:]) / 7)
            clean_bib_codes = [i for i in islice(row[14:], 0, None, linked_bibs_no)]
            new_row = row[:14] + clean_bib_codes
            save2csv("files/picklist/google-candidates-clean.txt", "\t", new_row)


if __name__ == "__main__":
    prep_sierra_export_for_dataframe("files/picklist/google-candidates.txt")
