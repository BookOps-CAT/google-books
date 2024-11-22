from pymarc import Record, Field, Subfield
import pytest


@pytest.fixture
def stub_bib():
    bib = Record()
    bib.add_field(Field(tag="001", data="1234"))
    bib.add_field(Field(tag="003", data="CStRLIN"))
    bib.add_field(
        Field(
            tag="035",
            indicators=[" ", " "],
            subfields=[Subfield("a", "(WaOLN)nyp1235")],
        )
    )
    bib.add_field(
        Field(tag="907", indicators=[" ", " "], subfields=[Subfield("a", ".b00000001")])
    )
    return bib


@pytest.fixture
def stub_row_one_bib():
    return [
        "i105072515",
        "-",
        "33",
        "rc2ma",
        "-  ",
        "-",
        "2",
        "214",
        "2",
        "33433011077942",
        "",
        "*EC.A939",
        "v. 12 (1909)",
        "",
        "",
        "u",
        "1888",
        "9999",
        "25 cm.",
        "Report of meeting.",
        "Sydney : [The Association], 1888-",
        "*EC.A939",
        "*EC.A939",
    ]


@pytest.fixture
def stub_row_linked_bibs():
    return [
        "i240387521",
        "-",
        "3",
        "rc2ma",
        "-  ",
        "-",
        "2",
        "214",
        "4",
        "33433061786897",
        "",
        "L-10 9215",
        "no. 15",
        "",
        "",
        "c",
        "s",
        "1965",
        "1989",
        "19uu",
        "    ",
        "",
        "21 cm.",
        "Supplementary volume.",
        "Studies in Latin literature and its tradition : in honour of C.O. Brink / edited by J. Diggle, J.B. Hall, and H.D. Jocelyn.",
        "Cambridge, Eng.: Trinity College.",
        "Cambridge [England] : Cambridge Philological Society, 1989.",
        "L-10 9215 Library has: 1-24 (Incomplete). Some vols. classed separately.",
        "L-10 9215 no. 15",
        "L-10 9215 Library has: 1-24 (Incomplete). Some vols. classed separately.",
        "L-10 9215 no. 15",
    ]
