from collections.abc import Callable

import click

from google_books.hathi_processor import (
    parse_hathi_processing_report,
    clean_metadata_for_hathi_submission,
)
from google_books.marc_manipulator import manipulate_records as fix_oclc_data
from google_books.recap_manifest import prep_recap_manifest_for_sierra_list


@click.group()
def cli() -> None:
    pass


def io_params(f: Callable) -> Callable:
    f = click.argument("source_fh", type=str)(f)
    return f


@cli.command()
@io_params
def hathi_report(source_fh: str) -> None:
    """
    Run analysis of the HathiTrust/Zephir reports and create actionable data.
    Outputs reports to files/out/ directory.
    """
    parse_hathi_processing_report(source_fh)


@cli.command()
@io_params
def hathi_metadata_prep(src_metadata: str, google_report: str, out: str):
    """
    Preps HathiTrust MARCXML file using Google FO reconciliation report by removing from
    it records/items that have not been digitized.

    Args:
        src_metadata:           MARCXML file used for Google submission
        google_report:          Google FO reconciliation report
        out:                    path to output MARXML file
    """
    clean_metadata_for_hathi_submission(src_metadata, google_report, out)


@cli.command()
@io_params
def oclc(source_fh: str) -> None:
    """
    Replaces 001/003 with OCLC info found in 035 or 991. Deletes 991.
    Outputs manipulated file to files/out/ directory
    """
    fix_oclc_data(source_fh)


@cli.command()
@io_params
def recap_manifest(source_fh: str) -> None:
    """
    Preps ReCAP manifest for Sierra list creation
    """
    out = prep_recap_manifest_for_sierra_list(source_fh)
    click.echo(f"Cleaned up manifest was saved to {out.resolve()}")


def main() -> None:
    cli()
