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

See a detailed walkthrough that includes instruction how to use the google-books tool in [this Google doc](https://docs.google.com/document/d/1xMqv9PjpOiJGxNZ0HsKS6ZXOykubqQPYoiqDSgJ3ivs/edit?usp=sharing).

#### Create New Shipment Folder
To store all associated files for a particular shipment, create a folder in `files/shipments/` using the following command:
```bash
$ google-books new-shipment [YYYYMMDD]
```
#### Prep Onsite Manifest for Google Submission
A Sierra export that includes Google patron account numbers and barcodes must be cleaned up before submitting it to Google. Use the following command where YYYYMMDD is the date of the shipment and folder:
```bash
$ google-books onsite-manifest [YYYYMMMDD]
```
This command produces `NYPL_YYYYMMDD.txt` manifest file.

#### Prep ReCAP Manifest for Sierra List Creation
ReCAP staff uploads a manifest to Google Drive. Use it to select relevant barcodes and create based on them a list in Sierra that is required to prepare metadata MARCXML file.
Use the following command to extract barcodes for the Create List:
```bash
$ google-books recap-manifest
```
The command creates `google-recap-barcodes-YYYYMMDD.csv` in the shipment folder. This list is used in the Data Exchange module.

#### Parse HathiTrust Processing Report

```bash
$ google-books hathi-report [FILE PATH]
```

#### Prepping MARCXML for HathiTrust Submission
Received Google's reconciliation report can be used to remove from MARCXML file, intended for HathiTrust, any records for materials that have not been scanned. Expect to receive a such reconciliation report via email about 2 months after shipment to Google. Only then remove records for any not digitized items and submit processed MARCXML file to Zephir.

```bash
$ google-books hathi-metadata-prep [MARCXML IN PATH] [GOOGLE FO REPORT PATH] [MARCXML OUT PATH]
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
http://hdl.handle.net/2027/nyp.[barcode]

example:
https://catalog.hathitrust.org/Record/100405490
https://babel.hathitrust.org/cgi/pt?id=nyp.33433105117174

### Google Books
http://books.google.com/books?vid=NYPL:[Barcode]


### To-do
+ verify 856's HathiTrust links were added to correct bibs from Nov 23
+ add notes about material's poor condition to items in Sierra based on GRIN's rejections (condition 25)
+ add more tests & increase test coverage
+ complete documentation