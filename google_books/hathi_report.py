from pathlib import Path

from google_books.utils import save2csv, report_name_base


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


def parse_report(fh: str) -> None:
    """
    Parses Hathi job report and filters the results into three separate
    files: hathi-success.csv, hathi-unspecified-oclc.csv, hathi-missing-oclc.csv.
    """
    fh_date = report_name_base(fh)
    with open(fh, "r") as file:
        for line in file.readlines():
            if "new cid =" in line:
                cid = find_cid(line)
                save2csv(f"files/out/hathi-{fh_date}-success.csv", [cid])
            elif line.startswith("WARNING: .b"):
                bibno = find_bibno(line)
                if "OCLC number found in unspecifed 035$" in line:
                    save2csv(
                        f"files/out/hathi-{fh_date}-unspecified-oclc.cvs",
                        [bibno],
                    )
                elif "no OCLC number in record" in line:
                    save2csv(
                        f"files/out/hathi-{fh_date}-missing-oclc.csv",
                        [bibno],
                    )
