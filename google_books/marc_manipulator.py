from collections import Counter
from typing import Optional, Iterator
import warnings

from pymarc import MARCReader, Record, Field, Subfield, XMLWriter, parse_xml_to_array

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


def get_bibs(source_fh: str) -> Iterator[tuple[int, Record]]:
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
        bib.add_ordered_field(
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


def generate_hathi_url(
    barcode: Optional[str], volume: Optional[str]
) -> Optional[Field]:
    """
    Generates the 856 MARC field with HathiTrust URL

    Args:
        bibno:                  Sierra bib number from 907$a
        barcode:                NYPL RL barcode
        volume:                 value of the 945$c

    Returns:
        `pymarc.Field` instance
    """
    subfields = []
    if isinstance(volume, str):
        volume = volume.strip()

    if barcode:
        subfields.append(Subfield("u", f"http://hdl.handle.net/2027/nyp.{barcode}"))
    else:
        return None

    if volume:
        subfields.append(Subfield("z", f"Full text available via HathiTrust--{volume}"))
    else:
        subfields.append(Subfield("z", "Full text available via HathiTrust"))

    return Field(tag="856", indicators=["4", "0"], subfields=subfields)


def is_item_field(field: Field) -> bool:
    """
    Tests if the field is item 945 field.

    Args:
        field:                  instance of `pymarc.Field` of the 945 MARC tag
    """
    if field.tag != "945":
        return False
    else:
        if field.get("y"):
            return True
        else:
            return False


def create_stub_hathi_records(
    marcxml_submitted: str, marcxml_errors: str, out: str
) -> None:
    """
    Creates stub records that include only LDR, 245, 856, & 907 fields.
    Generates 856 fields with HathiTrust URLs.
    Args:
        marcxml_submitted:      path to MARCXML file submitted to HathiTrust
        marcxml_errors:         path to Hathi's MARCXML with invalid records
        out:                    path to MARC21 file with output stub records
    """
    if marcxml_errors == "clean":
        invalid_bibs = []
    else:
        invalid_bibs = get_invalid_bib_nos(marcxml_errors)
    print(f"Found {len(invalid_bibs)} rejected record(s) by Zephir.")
    total_out_bibs = Counter()  # type: ignore

    for bib in marcxml_reader(marcxml_submitted):

        bibno = bib.get("907").get("a")  # type: ignore
        if bibno not in invalid_bibs:
            # create new stub records
            stub_bib = Record()
            stub_bib.leader = bib.leader
            stub_bib.add_ordered_field(bib.get("245"))
            stub_bib.add_ordered_field(bib.get("907"))
            has_item_field = False

            # construct 856s with Hathi URLs
            for f in bib.get_fields("945"):
                barcode = f.get("i")
                volume = f.get("c")
                t856 = generate_hathi_url(barcode, volume)

                if t856 and is_item_field(f):
                    has_item_field = True
                    stub_bib.add_ordered_field(t856)

            if not has_item_field:
                warnings.warn(
                    f"{bibno} has no barcode in 945 field. Skipping.", UserWarning
                )
            else:
                # output bibs in MARC21 format
                total_out_bibs.update(bibno=1)
                append2marc(stub_bib, out)

    print(f"Output {total_out_bibs.total()} stub records.")


def get_invalid_bib_nos(marcxml_error: str) -> list[str]:
    """
    Reads provided by Hathi MARCXML error report file and creates a list of Sierra
    bib #s.
    Args:
        marcxml_error:              path to marxml with invalid bibs provided by Hathi
    """
    try:
        bibNos = []
        for bib in marcxml_reader(marcxml_error):
            bibNos.append(bib.get("907").get("a"))  # type: ignore
        return bibNos
    except AttributeError:
        warnings.warn("Encountered bib without Sierra bib # in 907$a).")
        return []


def marcxml_reader(fh: str) -> Iterator[Record]:
    reader = parse_xml_to_array(fh)
    for bib in reader:
        yield bib


def save2marcxml(marcxml: str, bibs: list[Record]) -> None:
    writer = XMLWriter(open(marcxml, "ab"))
    for bib in bibs:
        writer.write(bib)
    writer.close()


def append2marc(record: Record, out: str) -> None:
    with open(out, "ab") as marcfile:
        marcfile.write(record.as_marc())
