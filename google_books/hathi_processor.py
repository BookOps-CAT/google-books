import csv

from google_books.marc_manipulator import marcxml_reader, save2marcxml
from google_books.utils import save2csv, fh_date


def find_bibno(line: str) -> str:
    """Extracts Sierra bib # from the report"""
    bibno = line[9:20]
    if not bibno.startswith(".b"):
        print(line)
        raise ValueError("Invalid Sierra bib # encountered.")
    return bibno


def find_cid(line: str) -> str:
    """Extracts Hathi cid from the report"""
    cid = line[-10:].strip()
    if not cid.isdigit():
        raise ValueError("Invalid Hathi CID encountered.")
    return cid


def parse_hathi_processing_report(fh: str) -> None:
    """
    Parses Hathi job report and filters the results into three separate
    files: hathi-success.csv, hathi-unspecified-oclc.csv, hathi-missing-oclc.csv.

    Args:
        fh:             path to processing report
    """
    date = fh_date(fh)
    with open(fh, "r") as file:
        for line in file.readlines():
            if "new cid =" in line:
                cid = find_cid(line)
                save2csv(f"files/out/hathi-{date}-success.csv", [cid])
            elif line.startswith("WARNING: .b"):
                bibno = find_bibno(line)
                if "OCLC number found in unspecifed 035$" in line:
                    save2csv(
                        f"files/out/hathi-{date}-unspecified-oclc.csv",
                        [bibno],
                    )
                elif "no OCLC number in record" in line:
                    save2csv(
                        f"files/out/hathi-{date}-missing-oclc.csv",
                        [bibno],
                    )


def google_reconciliation_to_barcodes_lst(fh: str) -> list[str]:
    """
    Parses Google's *FOreconciled.txt report and returns a list

    Args:
        fh:             path to google reconciliation report

    Returns:
        A list of rejected barcodes
    """
    barcodes = []
    with open(fh, "r") as report:
        reader = csv.reader(report)
        next(reader)
        for row in reader:
            barcodes.append(row[0])
    return barcodes


def clean_metadata_for_hathi_submission(
    metadata_fh: str, reconcile_report_fh: str, out: str
) -> None:
    """
    Using Google's reconcilation FO report removes from a given metadata file records
    that include rejected for digitizaiton items (barcodes).

    Args:
        metadata_fh:            path to marcxml file with records
        reconcile_report_fh:    path to google reconciliation FO report
    """
    rejected_barcodes = google_reconciliation_to_barcodes_lst(reconcile_report_fh)
    bibs = marcxml_reader(metadata_fh)

    bibs2keep = []
    for bib in bibs:
        barcode = bib.get("945").get("i").strip()
        if barcode not in rejected_barcodes:
            bibs2keep.append(bib)

    save2marcxml(out, bibs2keep)


if __name__ == "__main__":
    import sys

    print(sys.argv[1])
    clean_metadata_for_hathi_submission(sys.argv[1], sys.argv[2], sys.argv[3])
