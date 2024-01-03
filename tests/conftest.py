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
    return bib
