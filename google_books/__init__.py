import click

from google_books.hathi_processor import (
    parse_hathi_processing_report,
    clean_metadata_for_hathi_submission,
)
from google_books.marc_manipulator import manipulate_records as fix_oclc_data
from google_books.recap_manifest import prep_recap_manifest_for_sierra_list


__version__ = "0.1.0"


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
def hathi_report(filename: str) -> None:
    """
    Run analysis of the HathiTrust/Zephir reports and create actionable data.
    Outputs reports to files/out/ directory.
    """
    parse_hathi_processing_report(filename)


@cli.command()
@click.argument("marcxml", type=click.Path(exists=True))
@click.argument("google_report", type=click.Path(exists=True))
@click.argument("out", type=click.Path())
def hathi_metadata_prep(marcxml: str, google_report: str, out: str):
    """
    Preps HathiTrust MARCXML file using Google FO reconciliation report by removing from
    it records/items that have not been digitized.

    Args:
        marcxml:                MARCXML file used for Google submission
        google_report:          Google FO reconciliation report
        out:                    path to output MARCXML file
    """
    clean_metadata_for_hathi_submission(marcxml, google_report, out)


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
def oclc(filename: str) -> None:
    """
    Replaces 001/003 with OCLC info found in 035 or 991. Deletes 991.
    Outputs manipulated file to files/out/ directory
    """
    fix_oclc_data(filename)


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
def recap_manifest(filename: str) -> None:
    """
    Preps ReCAP manifest for Sierra list creation
    """
    out = prep_recap_manifest_for_sierra_list(filename)
    click.echo(f"Cleaned up manifest was saved to {out.resolve()}")


def main() -> None:
    cli()
