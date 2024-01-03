from collections.abc import Generator
from typing import Optional
import warnings

from pymarc import MARCReader, Record, Field, Subfield

from google_books.utils import fh_date


def manipulate_records(source_fh: str) -> None:
    """
    Reads given MARC file and replaces 001 & 003 to indicate OCLC control number
    based on present identifier in 035 or 991.
    Deletes 991 if present.
    """
    date = fh_date(source_fh)
    fh_out = f"files/out/hathi-{date}-fixed-oclc.mrc"
    for n, bib in get_bibs(source_fh):
        msg = fix_oclc_info(bib)
        if msg:
            with open(fh_out, "ab") as out:
                out.write(bib.as_marc())
            print(f"{msg} (record {n})")


def get_bibs(source_fh: str) -> Generator[Record, None, None]:
    with open(source_fh, "rb") as marcfile:
        reader = MARCReader(marcfile, hide_utf8_warnings=True)
        for n, bib in enumerate(reader, start=1):
            yield (n, bib)


def find_oclcno(bib: Record) -> Optional[str]:
    """Identifies OCLC # in a given record."""

    # check 035$a
    for f in bib.get_fields("035"):
        for s in f.get_subfields("a"):
            if s.startswith("(OCoLC)"):
                oclcno = s[7:].strip()
                if oclcno.isdigit():
                    return oclcno
                else:
                    warnings.warn(f"Encountered invalid OCLC #: {oclcno}.")

    # check 991$y
    for f in bib.get_fields("991"):
        for s in f.get_subfields("y"):
            oclcno = s.strip()
            if oclcno.isdigit():
                return oclcno
            else:
                warnings.warn(f"Encountered invalid OCLC #: {oclcno}.")

    return None


def fix_oclc_info(bib: Record) -> Optional[str]:
    """
    Manipulates given MARC record to enforce OCLC data in 001/003/035
    based on present 035 or 991 with OCLC identifier.
    """
    oclcno = find_oclcno(bib)
    bibno = bib["907"]["a"]
    if oclcno:
        bib.remove_fields(
            "001", "003", "852", "907", "910", "945", "949", "991", "997", "959", "998"
        )
        bib.add_ordered_field(Field(tag="001", data=oclcno))
        bib.add_ordered_field(Field(tag="003", data="OCoLC"))
        bib.add_ordered_field(
            Field(tag="945", indicators=[" ", " "], subfields=[Subfield("a", bibno)])
        )
        bib.add_ordere_field(
            Field(
                tag="949", indicators=[" ", " "], subfields=[Subfield("a", "*bn=xxx;")]
            )
        )

        return f"Processed bib {bibno}"
    else:
        warnings.warn(
            f"Unable to manipulate bib ({bibno}). No suitable OCLC # was found in bib."
        )
        return None
