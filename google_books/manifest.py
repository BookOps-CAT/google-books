"""
Onsite & ReCAP manifest manipulation scripts
"""

import csv
from pathlib import Path

from google_books.errors import FileNameError
from google_books.utils import save2csv, create_directory, fh_date


def prep_onsite_manifest_for_google(fh: str, parent_fh: str = None) -> Path:
    """
    Manipulates cart numbering in the manifest and creates a ready
    for submission to Google copy of carts and barcodes.

    Args:
        fh:         path to the Sierra Export with data for the manifest file
    """
    shipment_date = fh_date(fh)
    if not parent_fh:
        dir_parent = Path("files/shipments")

    if shipment_date:
        source_path = Path(fh)
        dir_path = create_directory(dir_parent, shipment_date)
        out_path = Path(dir_path).joinpath(f"NYPL_{shipment_date}.txt")

        with source_path.open("r") as csvfile:
            data = csv.reader(csvfile, delimiter="\t")
            next(data)  # skip the header
            for row in data:
                cart = row[0].split(" ")[-1]
                barcode = row[1]
                save2csv(out_path, "\t", [cart, barcode])
        return out_path
    else:
        raise FileNameError(
            "File name of the Sierra export must have YYYYMMDD of the shipment. "
            "Example, Google_Export_20241206.txt"
        )


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
