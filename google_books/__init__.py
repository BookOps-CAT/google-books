from collections.abc import Callable

import click

from google_books.hathi_report import parse_report as hathi_report


@click.group()
def cli() -> None:
    pass


def io_params(f: Callable) -> Callable:
    f = click.argument("source_fh", type=str)(f)
    return f


@cli.command()
@io_params
def hathi(source_fh: str) -> None:
    """
    Run analyzis of the reports and create actionable data.
    """
    hathi_report(source_fh)


def main() -> None:
    cli()
