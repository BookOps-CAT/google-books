"""
Onsite & ReCAP manifest manipulation scripts
"""

import csv
from pathlib import Path

from google_books.utils import save2csv


def prep_onsite_manifest_for_google(fh: str) -> Path:
    """
    Manipulates cart numbering in the manifest and creates a ready
    for submission to Google copy of carts and barcodes.

    Args:
        fh:         path to the manifest file
    """
    fh_path = Path(fh)
    out_path = Path(f"files/out/{fh_path.stem}.txt")
    with fh_path.open("r") as csvfile:
        manifest = csv.reader(csvfile, delimiter="\t")
        next(manifest)  # skip the header
        for row in manifest:
            cart = row[0].split(" ")[-1]
            barcode = row[1]
            save2csv(out_path, "\t", [cart, barcode])
    return out_path


def prep_recap_manifest_for_sierra_list(fh: str) -> Path:
    """
    Removes cart numbering from the manifest and creates a clean copy
    of barcodes to be used to create a list in Sierra

    Args:
        fh:         path to the manifest file
    """
    fh_path = Path(fh)
    out_path = Path(f"files/out/{fh_path.stem}-barcodes.csv")
    with fh_path.open("r") as csvfile:
        manifest = csv.reader(csvfile, delimiter="\t")
        for row in manifest:
            barcode = row[1]
            save2csv(out_path, ",", [barcode])
    return out_path
