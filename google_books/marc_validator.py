from pymarc import MARCReader
from pydantic_marc import MarcRecord


with open("files/shipments/2025-07-11/TEST.mrc", "rb") as fh:
    reader = MARCReader(fh)
    for record in reader:
        model = MarcRecord.model_validate(record, from_attributes=True)
        print(model.model_dump())
