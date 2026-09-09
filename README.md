# Business Process Automation

## Overview

This project is a Python-based business process automation solution designed to automate repetitive data-processing and document-generation tasks.

The current workflow automates the conversion of structured Excel data into organized Excel worksheets and subsequently generates separate PDF documents from those worksheets.

The project is designed with a modular approach so that additional business automation processes can be added in the future.

---

## Current Automation Workflow

```text
Input Excel File
       │
       ▼
Excel Data Processing
       │
       ▼
Group Data by Item Code
       │
       ▼
Separate Excel Worksheets
       │
       ▼
PDF Generation
       │
       ▼
Separate PDF Files
```

---

# 1. Excel Data Separation

### File

```text
1_invoice_generator.py
```

### Purpose

The first automation processes an Excel input file and separates the data based on the `Item Cd` column.

Instead of manually filtering and copying data into multiple worksheets, the program automatically:

1. Reads the input Excel file.
2. Identifies the `Item Cd` column.
3. Groups records according to the item code.
4. Cleans the item code so it can safely be used in an Excel worksheet name.
5. Creates a separate worksheet for each item code.
6. Writes the corresponding records into the worksheet.
7. Generates an output Excel file.

### Example

The actual company Excel data is **not included in this repository**.

For demonstration purposes, the process can be represented as:

```text
Input:

Item Cd     Item Description     Quantity
A100        Product A            10
B200        Product B            20
A100        Product A            15
C300        Product C            5
```

The automation produces:

```text
output_invoice.xlsx

├── Part_no_A100
├── Part_no_B200
└── Part_no_C300
```

Each worksheet contains only the records belonging to that item code.

---

# 2. Separate PDF Generation

### File

```text
2_separate_pdf_generator.py
```

### Purpose

The second automation takes the generated Excel workbook and creates a separate PDF document for each worksheet.

The program automatically:

1. Reads the generated Excel workbook.
2. Identifies all worksheets.
3. Reads each worksheet into a Pandas DataFrame.
4. Extracts the item code and item description.
5. Creates a PDF document.
6. Adds the worksheet data to the PDF.
7. Uses landscape A4 page formatting.
8. Creates a date-based output directory.
9. Saves each generated PDF separately.

### Output Structure

The actual company output is not included in this repository.

The generated structure is conceptually:

```text
invoice_pdf_YYYY-MM-DD/

├── ITEM_CODE_ITEM_DESCRIPTION.pdf
├── ITEM_CODE_ITEM_DESCRIPTION.pdf
└── ITEM_CODE_ITEM_DESCRIPTION.pdf
```

The actual company item codes, descriptions, filenames and business data are intentionally excluded.

---

# 3. Box Tag PDF Generation and PDF Merging

### File

```text
box_tag_generator.py
```

### Purpose

The third automation processes box-wise data from a CSV file and generates a separate PDF box tag for each `Box_no`.

The program automatically:

1. Reads the input CSV file.
2. Groups the data using the `Box_no` column.
3. Creates a separate PDF for each box.
4. Adds the required part information to the PDF.
5. Adds a verification field to the generated box tag.
6. Uses landscape A4 page formatting.
7. Creates an output directory for the generated PDFs.
8. Generates PDF filenames based on the box number.
9. Merges all generated box PDFs into one PDF file.
10. Sorts the box PDFs numerically before merging.

### Input Data

The actual company CSV file is **not included in this repository**.

For demonstration purposes, the input structure can be represented as:

```text
Box_no    Part_name       Drg_no       Quantity    Dispatched_date
101       Sample Part A   DRG-001      10          2026-09-01
101       Sample Part B   DRG-002      5           2026-09-01
102       Sample Part C   DRG-003      8           2026-09-02
103       Sample Part D   DRG-004      12          2026-09-03
```

The values above are **dummy data only** and do not represent actual company information.

---

## PDF Generation

For every unique `Box_no`, the program creates a separate PDF.

Conceptually:

```text
input.csv
    │
    ▼
Group by Box_no
    │
    ├── Box 101 → 101.pdf
    ├── Box 102 → 102.pdf
    └── Box 103 → 103.pdf
```

Each generated PDF contains information such as:

```text
Box No: 101

Part_name | Drg_no | Quantity | Dispatched_date | Verified By
```

The generated PDFs are stored inside:

```text
pdf_output_1/
```

The actual output directory name may vary depending on the version of the automation being used.

---

## PDF Merging

The `merge_pdf()` functionality combines the individual box PDFs into a single PDF.

Before merging, the program:

1. Finds PDF files in the output directory.
2. Selects PDFs whose filenames contain numeric box numbers.
3. Ignores non-numeric PDF filenames.
4. Sorts the PDFs according to their numeric box number.
5. Appends the PDFs in that order.
6. Creates a final merged PDF.

Example:

```text
Individual PDFs:

103.pdf
101.pdf
102.pdf
105.pdf
104.pdf

        │
        ▼

Numeric sorting:

101.pdf
102.pdf
103.pdf
104.pdf
105.pdf

        │
        ▼

Merged PDF:

print_all.pdf
```

This ensures that the final document follows the correct box-number sequence.

---

## Box Tag Automation Workflow

```text
Input CSV
    │
    ▼
Read CSV Data
    │
    ▼
Group Data by Box_no
    │
    ▼
Generate Individual Box PDFs
    │
    ├── Box 101.pdf
    ├── Box 102.pdf
    ├── Box 103.pdf
    └── ...
    │
    ▼
Filter Numeric PDF Files
    │
    ▼
Sort PDFs Numerically
    │
    ▼
Merge PDFs
    │
    ▼
print_all.pdf
```

---

## Unit Testing

The Box Tag PDF Generator is also tested using **Pytest**.

Test file:

```text
test_box_tag_generator.py
```

Important tests include:

* Program file availability
* Program loading
* `box_tag_generator` class availability
* `merge_pdf()` method availability
* Numeric PDF filtering
* Numeric PDF sorting
* Ignoring non-numeric PDF files
* PDF merger append operation
* PDF merge order
* Final merged PDF creation

Run the tests using:

```bash
python -m pytest -v test_box_tag_generator.py
```

---

# Technologies Used

* Python
* Pandas
* OpenPyXL / Excel processing
* XlsxWriter
* ReportLab
* PyPDF2
* Pytest
* Git
* GitHub

---

# Project Structure

```text
business-process-automation/
│
├── 1_invoice_generator.py
├── 2_separate_pdf_generator.py
├── 3_box_tag_generator.py
│
├── test_1_invoice_generator.py
├── test_2_separate_pdf_generator.py
├── test_box_tag_generator.py
│
├── README.md
├── .gitignore
└── requirements.txt
```

> Actual company Excel files, CSV files, generated PDFs and other confidential files should not be committed to the repository.

---

# Requirements

Python 3.12 or compatible Python 3 version.

Required packages include:

```text
pandas
xlsxwriter
openpyxl
reportlab
PyPDF2
pytest
```

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

# Quick Start

## 1. Clone the repository

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd business-process-automation
```

---

## 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on Linux/macOS:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Provide test/demo input

Use a **dummy or sanitized Excel/CSV file** for development and demonstration.

Do not upload the original company Excel or CSV files if they contain:

* Customer information
* Supplier information
* Employee information
* Internal item codes
* Pricing information
* Business-sensitive data
* Confidential transaction information
* Internal company identifiers
* Manufacturing information

---

## 5. Run Excel automation

```bash
python 1_invoice_generator.py
```

This generates the processed Excel workbook.

---

## 6. Run Invoice PDF automation

After the required Excel output has been generated:

```bash
python 2_separate_pdf_generator.py
```

This generates the separate PDF documents.

---

## 7. Run Box Tag automation

Provide a sanitized/demo `input.csv` file and run:

```bash
python 3_box_tag_generator.py
```

This generates individual box PDFs and merges them into a single PDF.

---

# Unit Testing

The project uses **Pytest** for automated testing.

Three test files are currently included:

```text
test_1_invoice_generator.py
test_2_separate_pdf_generator.py
test_box_tag_generator.py
```

## Run all tests

```bash
python -m pytest -v
```

## Run Excel automation tests

```bash
python -m pytest -v test_1_invoice_generator.py
```

## Run Invoice PDF automation tests

```bash
python -m pytest -v test_2_separate_pdf_generator.py
```

## Run Box Tag automation tests

```bash
python -m pytest -v test_box_tag_generator.py
```

---

# Testing Approach

The tests verify important parts of the automation workflow.

### Excel Automation

Tests include checks for:

* Input Excel file availability
* Excel file readability
* Required columns
* Valid input data
* Program execution
* Output workbook generation
* Output worksheets
* Worksheet data

### Invoice PDF Automation

Tests include checks for:

* Input Excel availability
* Excel workbook readability
* Worksheet availability
* Required columns
* Program execution
* PDF output directory creation
* PDF file generation
* PDF file validity
* Number of generated PDFs

### Box Tag Automation

Tests include checks for:

* Program file availability
* Program loading
* Required class availability
* Required method availability
* Numeric PDF filtering
* Numeric PDF sorting
* Non-numeric PDF filtering
* PDF merger append operation
* PDF merge order
* Final merged PDF creation

---

# Data Privacy and Security

This repository is intended to contain **source code and sanitized demonstration data only**.

The following information should not be committed to a public repository:

```text
❌ Real company name
❌ Client name
❌ Customer information
❌ Supplier information
❌ Employee information
❌ Real invoices
❌ Real pricing
❌ Real transaction records
❌ Confidential item codes
❌ Confidential part numbers
❌ Confidential drawing numbers
❌ Internal file paths
❌ Credentials
❌ API keys
❌ Passwords
❌ Access tokens
❌ Private configuration files
```

Use:

```text
✓ Dummy data
✓ Sanitized examples
✓ Generic filenames
✓ Environment variables for secrets
✓ .gitignore for local/company files
```

---

# Files That Should Not Be Committed

The following types of files should normally remain outside the public repository:

```text
*.xlsx
*.xls
*.xlsm
*.csv
*.pdf

.env
*.key
*.pem

venv/
__pycache__/
.pytest_cache/
.hypothesis/

output/
logs/
```

The `.gitignore` file should be configured according to the actual project requirements.

---

# Development Workflow

A typical development workflow is:

```text
1. Receive / prepare sanitized input
             │
             ▼
2. Process Excel data
             │
             ▼
3. Generate structured Excel output
             │
             ▼
4. Generate invoice PDFs
             │
             ▼
5. Generate box tag PDFs
             │
             ▼
6. Merge box tag PDFs
             │
             ▼
7. Run unit tests
             │
             ▼
8. Review generated output
             │
             ▼
9. Commit source-code changes
             │
             ▼
10. Push approved code to GitHub
```

---

# Future Improvements

The project can be extended with additional automation modules such as:

* Automated email generation
* Automated email attachments
* PDF validation
* Input data validation
* Error logging
* Configuration management
* Database integration
* REST API integration
* Automated report generation
* Scheduled processing
* Improved exception handling
* Production logging
* Centralized configuration
* Automated deployment

---

# Important Note

This repository contains a generalized representation of a business automation workflow.

Actual company-specific implementation details, business rules, confidential data, customer information and internal documents are intentionally excluded for security and confidentiality reasons.

The repository demonstrates the **technical approach and automation capability**, rather than exposing proprietary company information.
