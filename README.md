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

# Technologies Used

* Python
* Pandas
* OpenPyXL / Excel processing
* XlsxWriter
* ReportLab
* Pytest
* Git
* GitHub

---

# Project Structure

```text
business-process-automation/
│
├── 1_invoice_generator.py
│
├── 2_separate_pdf_generator.py
│
├── test_1_invoice_generator.py
│
├── test_2_separate_pdf_generator.py
│
├── README.md
│
├── .gitignore
│
└── requirements.txt
```

> Actual company Excel files, generated PDFs and other confidential files should not be committed to the repository.

---

# Requirements

Python 3.12 or compatible Python 3 version.

Required packages include:

```text
pandas
xlsxwriter
openpyxl
reportlab
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

Use a **dummy or sanitized Excel file** for development and demonstration.

Do not upload the original company Excel file if it contains:

* Customer information
* Supplier information
* Employee information
* Internal item codes
* Pricing information
* Business-sensitive data
* Confidential transaction information
* Internal company identifiers

---

## 5. Run Excel automation

```bash
python 1_invoice_generator.py
```

This generates the processed Excel workbook.

---

## 6. Run PDF automation

After the required Excel output has been generated:

```bash
python 2_separate_pdf_generator.py
```

This generates the separate PDF documents.

---

# Unit Testing

The project uses **Pytest** for automated testing.

Two test files are currently included:

```text
test_1_invoice_generator.py
test_2_separate_pdf_generator.py
```

## Run all tests

```bash
python -m pytest -v
```

## Run Excel automation tests

```bash
python -m pytest -v test_1_invoice_generator.py
```

## Run PDF automation tests

```bash
python -m pytest -v test_2_separate_pdf_generator.py
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

### PDF Automation

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
4. Generate PDF documents
             │
             ▼
5. Run unit tests
             │
             ▼
6. Review generated output
             │
             ▼
7. Commit source-code changes
             │
             ▼
8. Push approved code to GitHub
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
