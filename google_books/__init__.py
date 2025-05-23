from pathlib import Path
import click

from google_books.errors import FileNameError
from google_books.hathi_processor import (
    parse_hathi_processing_report,
    clean_metadata_for_hathi_submission,
)
from google_books.marc_manipulator import manipulate_records as fix_oclc_data
from google_books.marc_manipulator import create_stub_hathi_records
from google_books.manifest import (
    prep_onsite_manifest_for_google,
    prep_recap_manifest_for_sierra_list,
)
from google_books.picklist import (
    prep_item_list_for_sierra,
    prep_sierra_export_for_dataframe,
)
from google_books.utils import get_directory, shipment_date_obj


__version__ = "0.1.0"


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("shipment_date")
@click.argument("parent_dir", type=click.Path(), default="files/shipments")
def hathi_report(shipment_date: str, parent_dir: str) -> None:
    """
    Run analysis of the HathiTrust/Zephir reports and create actionable data.
    Outputs reports to files/out/ directory.
    """
    date = shipment_date_obj(shipment_date)
    shipment_dir = Path(f"{parent_dir}/{date:%Y-%m-%d}")
    source_fh = shipment_dir / f"nyp_{date:%Y%m%d}_google.txt"
    success_fh = shipment_dir / f"hathi-{date:%Y%m%d}-success.csv"
    invalid_oclc_fh = shipment_dir / f"hathi-{date:%Y%m%d}-unspecified-oclc.csv"
    missing_oclc_fh = shipment_dir / f"hathi-{date:%Y%m%d}-missing-oclc.csv"
    error_fh = shipment_dir / f"hathi-{date:%Y%m%d}-errors.csv"

    suc, inv, mis, err = parse_hathi_processing_report(
        date, source_fh, success_fh, invalid_oclc_fh, missing_oclc_fh, error_fh
    )

    click.echo("Report:")
    click.echo(f"Successfully processed {suc}. See {success_fh}")
    click.echo(f"OCLC in 035 only: {inv}. See {invalid_oclc_fh}")
    click.echo(f"Missing OCLC #: {mis}. See {missing_oclc_fh}")
    click.echo(f"Rejected {err}. See {error_fh}")


@cli.command()
@click.argument("shipment_date")
def hathi_metadata_prep(shipment_date: str):
    """
    Preps HathiTrust MARCXML file using GRIN's Advanced Search report by
    removing from it records/items that have not been digitized.

    Args:
        shipment_date:  date in the format YYYYMMDD
    """
    saved_bibs, rejected_bibs, file_size = clean_metadata_for_hathi_submission(
        shipment_date
    )
    click.echo(
        f"Scanned items: {saved_bibs}\nRejected items: {rejected_bibs}\n"
        f"File size: {file_size} (bytes)"
    )


@cli.command()
@click.argument("shipment_date")
@click.argument("parent_dir", type=click.Path(), default="files/shipments")
def new_shipment(shipment_date: str, parent_dir: str):
    """
    Creates a new folder for shipment files.

    Args:
        shipment_date:  date in the format YYYYMMDD
    """

    date = shipment_date_obj(shipment_date)
    folder = f"{date:%Y-%m-%d}"
    shipment_directory = get_directory(parent_dir, folder)
    click.echo(f"New shipment directory created at {shipment_directory}")


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
def oclc(filename: str) -> None:
    """
    Replaces 001/003 with OCLC info found in 035 or 991. Deletes 991.
    Outputs manipulated file to files/out/ directory
    """
    fix_oclc_data(filename)


@cli.command()
@click.argument(
    "shipment_date",
)
def recap_manifest(shipment_date: str) -> None:
    """
    Preps ReCAP manifest for Sierra list creation.
    Args:
        shipment_date:  date in the format YYYYMMDD
    """
    try:
        out = prep_recap_manifest_for_sierra_list(shipment_date)
        click.echo(f"Cleaned up manifest was saved to {out.resolve()}")
    except FileNotFoundError:
        click.echo(
            "Error. ReCAP manifest file not found. Make sure the shipment folder "
            "exists and manifest txt file has correct name "
            "(NYPL_YYYYMMDD-ReCAP.txt)."
        )


@cli.command()
@click.argument("shipment_date")
def onsite_manifest(shipment_date: str) -> None:
    """
    Preps Sierra item export for submission to Google
    """
    try:
        out = prep_onsite_manifest_for_google(shipment_date)
        click.echo(f"Prepped manifest was saved to {out.resolve()}")
    except FileNameError:
        raise


@cli.command()
@click.argument("tar_file", type=click.Path(exists=True))
@click.argument("list_size", type=int, default=200000)
def unpack_candidate_items(tar_file: str, list_size: int) -> None:
    """
    Prepares the item list for Sierra based on Google Candidate list _combined
    tar file. Creates `nypl-YYYY-MM-DD-candidate-items.csv` file with item numbers
    in the `picklist` folder.
    Args:
        tar_file (str): The tar file containing the candidate list.
    """
    prep_item_list_for_sierra(tar_file, list_size)
    click.echo("Candidate items have been saved to files/picklist/ directory.")


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
@click.argument("date", type=str)
def clean_candidates_sierra_export(filename: str, date: str) -> None:
    """
    Transforms a given Sierra export file to a format that can be used to create
    `pandas.DataFrame` object. Will append data to the out file if already exists.
    Args:
        filename (str): The path to the Sierra export file
        date (str): The date of the export for the output file name
    """
    click.echo("Cleaning up Sierra export. This may take several minutes...")
    prep_sierra_export_for_dataframe(filename, date)
    click.echo("Cleaned Sierra export was saved to files/picklist/ directory.")


@cli.command()
@click.argument("shipment_date")
def hathi_urls(shipment_date: str, parent_dir: str = "files/shipments") -> None:
    """
    Creates stub MARC21 records with generated 856 for HathiTrust URLs based
    on files in the shipment folder.

    Args:
        shipment_date:      shipment_date:  date in the format YYYYMMDD

    """
    date = shipment_date_obj(shipment_date)
    shipment_dir = Path(f"{parent_dir}/{date:%Y-%m-%d}")
    submitted_fh = shipment_dir / f"nyp_{date:%Y%m%d}_google.xml"
    errors_fh = shipment_dir / f"nyp_{date:%Y%m%d}_google_error.xml"
    out_fh = shipment_dir / f"hathi-stub-urls_{date:%Y%m%d}.mrc"

    create_stub_hathi_records(submitted_fh, errors_fh, out_fh)
    click.echo(f"Stub MARC records with Hathi URLs were saved to `{out_fh}`.")


def main() -> None:
    cli()
