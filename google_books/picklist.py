"""
A module with methods to unpack Google Candidate List and create
NYPL pick list.
"""

import csv
import glob
import tarfile

from google_books.utils import fh_date, save2csv


def extract_candidate_list(tar_file: str) -> None:
    """
    Extracts the candidate list from the tar file.

    Args:
        tar_file (str): The tar file containing the candidate list.
    """
    with tarfile.open(tar_file, "r") as tar:
        tar.extractall("files/picklist")


def prep_item_list_for_sierra(tar_file: str) -> None:
    """
    Prepares the item list for Sierra based on Google Candidate list _combined tar file.
    Creates `nypl-YYYY-MM-DD-candidate-items.csv` file with item numbers in the
    `picklist` folder.

    Args:
        tar_file (str): The tar file containing the candidate list.
    """
    date = fh_date(tar_file)
    out = f"files/picklist/nypl-{date}-candidate-items.csv"

    extract_candidate_list(tar_file)

    # read each extracted .txt file, find item #, and write it to a new file
    files = glob.glob("files/picklist/*_combined-*.txt")
    for f in files:
        reader = csv.reader(open(f, "r", encoding="utf-8"), delimiter="\t")
        for row in reader:
            item = row[1][1:]
            save2csv(out, ",", [item])


if __name__ == "__main__":
    prep_item_list_for_sierra("files/picklist/nypl-2024-05-15_combined.tar.gz")
