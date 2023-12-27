Scripts to support submissiona and reconciliation of metadata in the Google Books/Hathi Trust project.

### HathiTrust
#### Catalog Record URL
https://catalog.hathitrust.org/Record/[cid]
example:
https://catalog.hathitrust.org/Record/100405490


### Questions
+ When ingested records show up in HathiTrust?
+ Should the MARCXML file send to Google/Hathi be deduped? Is this a problem for either one? Duplication stems from type of Sierra list being used = item record search.
  + It appears duplication is fine - Hathi includes item record data and that can be parsed from dup bibs, each with different item (945 tag)
+ What happens when we resubmit a record that passed validation (minor problems only) and was ingested to Hathi? Will it get overwritten?
+ Does warning like that from Hathi indicates the metadata was not ingested? WARNING: .b13299222x (93): OCLC number found in unspecifed 035$(OcoLC) field: 64405402
  + No, it appears these are not being ingested and must be corrected - OCLC info provided in 001/003/035
+ For Hathi, does it matter if OCLC # is in the first 035? 