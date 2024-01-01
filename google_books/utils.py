import csv

import click


def save2csv(dst_fh, row):
    """
    Appends a list with data to a dst_fh csv
    args:
        dst_fh: str, output file
        row: list, list of values to write in a row
    """

    with open(dst_fh, "a", encoding="utf-8") as csvfile:
        out = csv.writer(
            csvfile,
            delimiter=",",
            lineterminator="\n",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        try:
            out.writerow(row)
        except UnicodeEncodeError:
            pass


def report_name_base(fh: str) -> str:
    """Creates base name for analysis report files"""
    err_msg = "The name of the file to be parsed is invalid. Correct pattern: 'nyp_YYYYMMDD_google'."
    try:
        fh_str = click.format_filename(fh)
        print(fh_str)
        fh_date = fh_str.split("_")[1]
    except IndexError:
        raise ValueError(err_msg)
    if not fh_date.isdigit():
        raise ValueError(err_msg)
    return fh_date
