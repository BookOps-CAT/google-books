Scripts to support submission and reconciliation of metadata for the Google Books/Hathi Trust project.

### HathiTrust
#### Catalog Record URL
https://catalog.hathitrust.org/Record/[cid]

example:
https://catalog.hathitrust.org/Record/100405490


### Questions
+ When ingested records show up in HathiTrust?
+ ~~Should the MARCXML file send to Google/Hathi be deduped? Is this a problem for either one? Duplication stems from type of Sierra list being used = item record search.~~
  + It appears duplication is fine - Hathi includes item record data and that can be parsed from dup bibs, each with different item (945 tag)
+ What happens when we resubmit a record that passed validation (minor problems only) and was ingested to Hathi? Will it get overwritten?
+ ~~Does warning like that from Hathi indicates the metadata was not ingested? WARNING: .b13299222x (93): OCLC number found in unspecifed 035$(OcoLC) field: 64405402~~
  + Confirmed, these are not being ingested and must be corrected - OCLC info provided in 001/003/035
+ ~~For Hathi, does it matter if OCLC # is in the first 035?~~
  + It appears it does not matter
+ Zephir gives the following submission warning: WARNING: -d nyp_20231208_google run option is not YYYYMMDD: using 20231208 . Is this relevant? Submissions are getting processed and we follow the file name convention specified in the docs.
+ Zephir gives the following submission warning: WARNING: using namespace nyp for NUC code in 852. What is this about?