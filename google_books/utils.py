import csv
from datetime import datetime

import click


def save2csv(dst_fh, delimiter, row):
    """
    Appends a list with data to a dst_fh csv
    args:
        dst_fh: str, output file
        row: list, list of values to write in a row
    """

    with open(dst_fh, "a", encoding="utf-8") as csvfile:
        out = csv.writer(
            csvfile,
            delimiter=delimiter,
            lineterminator="\n",
            quotechar="@",
            quoting=csv.QUOTE_MINIMAL,
        )
        try:
            out.writerow(row)
        except UnicodeEncodeError:
            pass


def fh_date(fh: str) -> str:
    """Creates base name for analysis report files"""
    err_msg = (
        "The name of the file to be parsed is invalid. "
        "Correct pattern: 'nyp_YYYYMMDD_google' or 'files/picklist/nypl-YYYY-MM-DD_'"
    )
    try:
        fh_str = click.format_filename(fh)
        if fh_str.startswith("files/picklist/nypl-"):
            fh_date = fh_str.split("_")[0][20:]
        else:
            fh_date = fh_str.split("_")[1]
    except IndexError:
        raise ValueError(err_msg)

    # check if the date is in the correct format
    try:
        datetime.strptime(fh_date, "%Y%m%d")
    except ValueError:
        pass
    else:
        return fh_date

    try:
        datetime.strptime(fh_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(err_msg)
    else:
        return fh_date
