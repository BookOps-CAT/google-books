[![Build Status](https://github.com/BookOps-CAT/google-books/actions/workflows/unit-tests.yaml/badge.svg?branch=main)](https://github.com/BookOps-CAT/google-books/actions) [![Coverage Status](https://coveralls.io/repos/github/BookOps-CAT/google-books/badge.svg?branch=main)](https://coveralls.io/github/BookOps-CAT/google-books?branch=main) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Scripts to support NYPL submission and reconciliation of metadata for the Google Books/HathiTrust project.

### Version
> 0.1.0

### Installation
Always use [virtual environment](https://docs.python.org/3/library/venv.html). After activating your virtual environment, invoke `pip` to install the package:
```bash
$ pip install git+https://github.com/BookOps-CAT/google-books.git
```

### Usage

To use this application, activate your virtual environment.

The package uses CLI commands to run a particular process. All scripts are launched by invoking `google-books` command in your preferred command line tool.
All commands have the following pattern: `google-books [OPTIONS] COMMAND [ARGS]`

Use the help function to learn about all available options:
```bash
$ google-books --help
```

#### Prep Onsite Manifest for Google Submission
#### Prep ReCAP Manifest for Google Submission
#### Parse HathiTrust Processing Report

```bash
$ google-books hathi-report [FILE PATH]
```

#### Prepping MARCXML for HathiTrust Submission
Received Google's reconciliation report can be used to remove from MARCXML file, intended for HathiTrust, any records for materials that have not been scanned. Expect to receive a such reconciliation report via email about 2 months after shipment to Google. Only then remove records for any not digitized items and submit processed MARCXML file to Zephir.

```bash
$ google-books hathi-metadata-prep MARCXML=[FILE PATH] GOOG-REPORT=[FILE PATH] OUT=[FILE PATH]
```

#### Move OCLC Identifiers to the Control Field
Use MARC21 exports from Sierra to fix records that do not have an OCLC # in the control number field (001 MARC tag). Records that have OCLC identifiers in the 035 field or 991$y will have the 001 replaced with OCLC # with properly encoded 003 tag. This process deletes present 991 fields from the records.

Manipulated this way file can then be reloaded into Sierra to overwrite original records.

```bash
$ google-books oclc [MARC21 FILE PATH]
```


### HathiTrust
#### Catalog Record URL
https://catalog.hathitrust.org/Record/[cid]
https://babel.hathitrust.org/cgi/pt?id=nyp.[barcode]

example:
https://catalog.hathitrust.org/Record/100405490
https://babel.hathitrust.org/cgi/pt?id=nyp.33433105117174


### Questions
+ When ingested records show up in HathiTrust?
+ ~~Should the MARCXML file send to Google/Hathi be deduped? Is this a problem for either one? Duplication stems from type of Sierra list being used = item record search.~~
  + It appears duplication is fine - Hathi includes item record data and that can be parsed from dup bibs, each with different item (945 tag)
+ What happens when we resubmit a record that passed validation (minor problems only) and was ingested to Hathi? Will it get overwritten?
+ ~~Does warning like that from Hathi indicates the metadata was not ingested? WARNING: .b13299222x (93): OCLC number found in unspecified 035$(OcoLC) field: 64405402~~
  + Confirmed, these are not being ingested and must be corrected - OCLC info provided in 001/003/035
+ ~~For Hathi, does it matter if OCLC # is in the first 035?~~
  + It appears it does not matter
+ Zephir gives the following submission warning: WARNING: -d nyp_20231208_google run option is not YYYYMMDD: using 20231208 . Is this relevant? Submissions are getting processed and we follow the file name convention specified in the docs.
+ Zephir gives the following submission warning: WARNING: using namespace nyp for NUC code in 852. What is this about?