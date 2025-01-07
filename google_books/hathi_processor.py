from collections import Counter
import csv
import datetime
from pathlib import Path

from google_books.marc_manipulator import marcxml_reader, save2marcxml
from google_books.utils import save2csv, fh_date, shipment_date_obj


def find_bibno(line: str) -> str:
    """Extracts Sierra bib # from the report"""
    bibno_idx = line.find(".b")
    if bibno_idx >= 0:
        bibno = line[bibno_idx + 1 : bibno_idx + 11]  # noqa: E203
    else:
        raise ValueError(f"Invalid Sierra bib # encountered. Line: {line}")
    return bibno


def find_cid(line: str) -> str:
    """Extracts Hathi cid from the report"""
    cid = line[-10:].strip()
    if not cid.isdigit():
        raise ValueError("Invalid Hathi CID encountered.")
    return cid


def find_err_msg(line: str) -> str:
    """Extracts error message given in Zephir report"""
    if line.startswith("ERROR"):
        err_idx = line.find("): ")
        return line[err_idx + 3 :].strip()  # noqa: E203
    else:
        return ""


def parse_hathi_processing_report(fh: str) -> None:
    """
    Parses Hathi job report and filters the results into three separate
    files: hathi-success.csv, hathi-unspecified-oclc.csv, hathi-missing-oclc.csv.

    Args:
        fh:             path to processing report
    """
    date = fh_date(fh)
    succ_count = 0
    succ_fh = f"files/out/hathi-{date}-success.csv"
    inval_oclc_loc_count = 0
    inval_oclc_fh = f"files/out/hathi-{date}-unspecified-oclc.csv"
    miss_oclc_count = 0
    miss_oclc_fh = f"files/out/hathi-{date}-missing-oclc.csv"
    err_count = 0
    err_fh = f"files/out/hathi-{date}-errors.csv"
    with open(fh, "r") as file:
        for line in file.readlines():
            if "new cid =" in line:
                cid = find_cid(line)
                save2csv(succ_fh, ",", [cid])
                succ_count += 1
            elif line.startswith("WARNING: .b"):
                bibno = find_bibno(line)
                if "OCLC number found in unspecified 035$" in line:
                    save2csv(
                        inval_oclc_fh,
                        ",",
                        [bibno],
                    )
                    inval_oclc_loc_count += 1
                elif "no OCLC number in record" in line:
                    save2csv(
                        miss_oclc_fh,
                        ",",
                        [bibno],
                    )
                    miss_oclc_count += 1
            elif line.startswith("ERROR"):
                bibno = find_bibno(line)
                err_msg = find_err_msg(line)
                save2csv(
                    err_fh,
                    ",",
                    [
                        bibno,
                        f"{date}",
                        "Zephir validation",
                        f"nyp_{date}_google.xml",
                        err_msg,
                        "NO",
                    ],
                )
                err_count += 1
    print("Report:\n\t")
    print(f"success: {succ_count} ({succ_fh})\n")
    print(f"\tOCLC in 035 only: {inval_oclc_loc_count} ({inval_oclc_fh})\n")
    print(f"\tmissing OCLC#: {miss_oclc_count} ({miss_oclc_fh})\n")
    print(f"\trejected: {err_count} ({err_fh})")


def google_reconciliation_to_barcodes_lst(fh: Path) -> list[str]:
    """
    Parses GRIN report of not scanned by Google items and returns a list.
    The list is deduped.

    Args:
        fh:             path to google reconciliation report

    Returns:
        A list of rejected barcodes
    """
    barcodes = set()
    grin_codes = []
    with fh.open() as report:
        reader = csv.reader(report, delimiter="\t")
        next(reader)
        for row in reader:
            barcodes.add(row[0].strip())
            grin_codes.append((row[4]))

    c = Counter(grin_codes)
    print(
        "Most common problems Google scanning encountered "
        f"(total not scanned={c.total()}):"
    )
    for v, n in c.most_common():
        print(f"{v} = {n}")
    return sorted(list(barcodes))


def get_hathi_meta_destination(shipment_date: datetime.date) -> Path:
    """
    Creates path to output file for HathiTrust metadata.

    Args:
        shipment_date:      date string (YYYYMMDD format) which corresponds to
                            files/shipments/YYYY-MM-DD directory
    """
    return Path(
        f"files/shipments/{shipment_date:%Y-%m-%d}/nyp_{shipment_date:%Y%m%d}_google.xml"
    )


def get_marcxml(shipment_date: datetime.date) -> Path:
    """
    Returns path to source MARCXML file to be used for submission to Hathi.

    Args:
        shipment_date:      date string (YYYYMMDD format) which corresponds to
                            files/shipments/YYYY-MM-DD directory
    """
    return Path(
        f"files/shipments/{shipment_date:%Y-%m-%d}/NYPL_{shipment_date:%Y%m%d}.xml"
    )


def get_grin_report(shipment_date: datetime.date) -> Path:
    """
    Determines path to the grin report.

    Args:
        shipment_date:      which corresponds to
                            files/shipments/YYYY-MM-DD directory
    """
    return Path(f"files/shipments/{shipment_date:%Y-%m-%d}/_query.txt")


def clean_metadata_for_hathi_submission(shipment_date: str) -> None:
    """
    Using GRIN's not scanned report removes from a given metadata file records
    that include rejected for digitization items (barcodes).

    Args:
        shipment_date:      date in the format YYYYMMDD
    """
    date = shipment_date_obj(shipment_date)
    marcxml = get_marcxml(date)
    grin_report = get_grin_report(date)
    out = get_hathi_meta_destination(date)

    rejected_barcodes = google_reconciliation_to_barcodes_lst(grin_report)
    print(marcxml.absolute(), type(marcxml.absolute()))
    bibs = marcxml_reader(str(marcxml))

    bibs2keep = []
    for bib in bibs:
        for field in bib.get_fields("945"):
            try:
                barcode = field.get("i").strip()
                if barcode not in rejected_barcodes:
                    bibs2keep.append(bib)
            except AttributeError:
                continue

    print(f"Saving {len(bibs2keep)} items to {out}")
    save2marcxml(out, bibs2keep)
