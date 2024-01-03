from collections.abc import Generator
from typing import Optional
import warnings

from pymarc import MARCReader, Record, Field, Subfield


def get_bibs(source_fh: str) -> Generator[Record, None, None]:
    with open(source_fh, "rb") as marcfile:
        reader = MARCReader(marcfile)
        for bib in reader:
            yield bib


def find_oclcno(bib: Record) -> Optional[str]:
    """Identifies OCLC # in a given record."""

    # check 035$a
    for f in bib.get_fields("035"):
        for s in f.get_subfields("a"):
            print(s)
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


def fix_oclc_info(bib: Record) -> None:
    """
    Manipulates given MARC record to enforce OCLC data in 001/003/035
    based on present 035 or 991 with OCLC identifier.
    """
    oclcno = find_oclcno(bib)
    if oclcno:
        pass
    else:
        pass
