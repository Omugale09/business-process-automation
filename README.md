# Business Process Automation

A Python-based automation project for processing structured business data from Excel files and generating organized Excel output automatically.

This project demonstrates an automated Excel data-processing workflow using Python and Pandas, along with automated testing using Pytest.

> **Note:** This repository is a sanitized version of a real-world business automation workflow. No confidential company, client, customer, vendor, financial, or proprietary information is included.

---

## Project Overview

The current functionality reads data from an Excel file, groups records according to the `Item Cd` column, and generates a separate worksheet for each Item Code.

### Main workflow

1. Read the Excel input file.
2. Load the data into a Pandas DataFrame.
3. Group records using the `Item Cd` column.
4. Process each Item Code group.
5. Clean the Item Code for use as an Excel worksheet name.
6. Create a separate worksheet for each Item Code.
7. Write the corresponding records to the worksheet.
8. Generate an output Excel workbook.
9. Validate the application using automated tests.

---

## Processing Flow

```text
Excel Input
     |
     v
Read Excel File
     |
     v
Pandas DataFrame
     |
     v
Group by "Item Cd"
     |
     v
Process Each Group
     |
     v
Clean Item Code
     |
     v
Create Worksheet
     |
     v
Write Group Data
     |
     v
Output Excel Workbook
     |
     v
Pytest Validation
```

---

## Technologies Used

* Python
* Pandas
* XlsxWriter
* Excel
* Pytest
* Git
* GitHub

---

## Project Structure

```text
business-process-automation/
|
├── invoice_generator.py
├── test_1_invoice_generator.py
├── requirements.txt
├── README.md
└── .gitignore
```

Sample or confidential Excel files are intentionally excluded from the public repository.

---

## Input Data

The application expects an Excel file containing an `Item Cd` column.

A typical business dataset may contain fields such as:

| Field            | Description              |
| ---------------- | ------------------------ |
| Invoice No.      | Invoice reference        |
| Date             | Transaction date         |
| Item Cd          | Item or product code     |
| Item Description | Description of the item  |
| PO No            | Purchase order reference |
| Quantity         | Quantity of the item     |

For public demonstration, use only fictional/sample data.

Example:

| Invoice No. | Date       | Item Cd | Item Description | PO No | Quantity |
| ----------- | ---------- | ------- | ---------------- | ----- | -------: |
| INV001      | 01-01-2026 | ITEM001 | Sample Item      | PO001 |       10 |
| INV002      | 02-01-2026 | ITEM002 | Sample Item      | PO002 |       20 |
| INV003      | 03-01-2026 | ITEM001 | Sample Item      | PO003 |        5 |

---

## How the Code Works

### 1. Import libraries

```python
import pandas as pd
import os
```

* `pandas` is used for reading and processing Excel data.
* `os` is used for working with file and directory paths.

### 2. Get the current directory

```python
cd_path = os.getcwd()
```

Gets the current working directory of the application.

### 3. Create file paths

```python
input_file_path = os.path.join(cd_path, "Book1.xlsx")
output_file_path = os.path.join(cd_path, "output_invoice.xlsx")
```

`os.path.join()` combines the directory path with the filename.

This avoids manually constructing operating-system-specific paths.

### 4. Read the Excel file

```python
df = pd.read_excel(input_file_path)
```

Pandas reads the Excel file and stores the data in the DataFrame `df`.

### 5. Group the data

```python
grouped = df.groupby('Item Cd')
```

The data is divided into groups based on the `Item Cd` column.

For example:

```text
ITEM001
ITEM001
ITEM002
ITEM002
ITEM003
```

creates separate groups for:

```text
ITEM001
ITEM002
ITEM003
```

### 6. Create the output workbook

```python
with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
```

Creates an Excel writer that will generate the output workbook.

### 7. Process every group

```python
for invoice_no, group in grouped:
```

The first variable contains the group key, which in this implementation is the `Item Cd` value.

The second variable contains all rows belonging to that Item Code.

### 8. Clean the Item Code

```python
cleaned_invoice_no = ''.join(
    c for c in str(invoice_no)
    if c.isalnum() or c in ['-', '_', ' ']
)
```

This creates a cleaned version of the Item Code containing:

* Letters
* Numbers
* `-`
* `_`
* Spaces

Characters outside these allowed characters are removed from the value used for the worksheet name.

For example:

```text
ITEM#001
```

can become:

```text
ITEM001
```

The cleaning is used for the worksheet name; it does not modify the original `Item Cd` value stored in the data.

### 9. Create the worksheet

```python
if cleaned_invoice_no and cleaned_invoice_no not in writer.sheets:
    group.to_excel(
        writer,
        sheet_name=f'Part_no_{cleaned_invoice_no}',
        index=False
    )
```

A separate worksheet is created for each valid Item Code group.

Example:

```text
Part_no_ITEM001
Part_no_ITEM002
Part_no_ITEM003
```

---

## Output

The application generates an Excel workbook containing separate worksheets for the different Item Codes.

Example:

```text
output_invoice.xlsx
|
├── Part_no_ITEM001
├── Part_no_ITEM002
└── Part_no_ITEM003
```

Each worksheet contains the records belonging to its corresponding Item Code.

---

## Testing

The project includes automated tests using **Pytest**.

The tests verify areas such as:

* Input file availability
* Excel file readability
* Required columns
* Input data availability
* Program execution
* Output file creation
* Output workbook readability
* Worksheet creation
* Worksheet naming
* Special-character handling
* Output columns
* Output data
* Item Code grouping
* Data preservation
* Output row counts
* Expected worksheet generation

Run the tests with:

```bash
pytest -v
```

Run the specific test file with:

```bash
pytest -v test_1_invoice_generator.py
```

---

## Installation

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment on Linux:

```bash
source venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Requirements

The basic dependencies are:

```text
pandas
xlsxwriter
pytest
```

These can be stored in:

```text
requirements.txt
```

---

## Running the Application

Place a suitable sample Excel input file in the project directory.

The application expects:

```text
Book1.xlsx
```

Run:

```bash
python invoice_generator.py
```

The output workbook will be generated as:

```text
output_invoice.xlsx
```

---

## Running Tests

Run all tests:

```bash
pytest -v
```

Run only the invoice generator tests:

```bash
pytest -v test_1_invoice_generator.py
```

---

## Data Privacy and Security

This repository is intended for public demonstration and should not contain confidential information.

The following information must not be committed to a public repository:

* Client or company names
* Customer information
* Vendor information
* Real invoice records
* Real purchase order information
* Financial information
* Employee information
* Internal URLs
* Internal server addresses
* Database credentials
* Passwords
* API keys
* Access tokens
* Private certificates
* Proprietary configuration
* Confidential business data

Real company Excel files should not be uploaded.

Use fictional or sanitized data for demonstrations.

---

## `.gitignore`

The project uses `.gitignore` to prevent accidental tracking of confidential or unnecessary files.

Important examples include:

```text
.env
venv/
__pycache__/
.pytest_cache/
*.xlsx
*.xls
*.csv
```

This helps prevent real business data, environment files, virtual environments, and temporary files from being committed accidentally.

---

## Purpose

The purpose of this project is to automate repetitive Excel-based business data processing.

The automation can help:

* Reduce manual Excel operations
* Improve consistency
* Reduce repetitive work
* Minimize manual processing errors
* Generate structured output
* Make the process repeatable
* Validate functionality through automated testing

---

## Future Improvements

Potential improvements include:

* Convert the script into reusable functions
* Add input validation
* Add error handling
* Add logging
* Support configurable input and output paths
* Handle empty input files
* Handle missing columns
* Add more comprehensive unit tests
* Add GitHub Actions for automated testing
* Support multiple input files
* Generate processing reports
* Add command-line arguments
* Improve project modularity

---

## Project Status

The current version implements Excel-based data processing, grouping by Item Code, worksheet generation, and automated testing.

Additional business automation modules can be added to this repository as the project evolves.

---

## Disclaimer

This public repository contains a sanitized implementation intended for demonstration and learning purposes.

No confidential client or company information should be included in this repository.
