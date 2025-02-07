"""
Onsite & ReCAP manifest manipulation scripts
"""

import csv
from pathlib import Path

from google_books.utils import (
    save2csv,
    get_directory,
    shipment_date_obj,
)


def prep_onsite_manifest_for_google(shipment_date: str) -> Path:
    """
    Manipulates cart numbering in the manifest and creates a ready
    for submission to Google copy of carts and barcodes.

    Args:
        shipment_date:  YYYYMMDD of the shipment
    """
    date = shipment_date_obj(shipment_date)
    shipment_directory = get_directory("files/shipments", f"{date:%Y-%m-%d}")
    source_path = shipment_directory / f"SierraExportManifest_{date:%Y%m%d.txt}"
    out_path = shipment_directory / f"NYPL_{date:%Y%m%d}.txt"

    with source_path.open("r") as csvfile:
        data = csv.reader(csvfile, delimiter="\t")
        next(data)  # skip the header
        for row in data:
            cart = row[0].split(" ")[-1]
            barcode = row[1]
            save2csv(out_path, "\t", [cart, barcode])
    return out_path


def prep_recap_manifest_for_sierra_list(shipment_date: str) -> Path:
    """
    Removes cart numbering from the manifest and creates a clean copy
    of barcodes to be used to create a list in Sierra

    Args:
        shipment_date:  date in the format YYYYMMDD

    Returns:
        `Path` instance to output file
    """
    date = shipment_date_obj(shipment_date)
    shipment_directory = get_directory("files/shipments", f"{date:%Y-%m-%d}")
    source_fh = Path(shipment_directory).joinpath(f"NYPL_{date:%Y%m%d}-ReCAP.txt")
    out_path = Path(shipment_directory).joinpath(
        f"google-recap-barcodes-{date:%Y%m%d}.csv"
    )
    with source_fh.open("r") as csvfile:
        manifest = csv.reader(csvfile, delimiter="\t")
        for row in manifest:
            barcode = row[1]
            save2csv(out_path, ",", [barcode])
    return out_path
