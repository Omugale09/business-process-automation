# Business Process Automation

## Overview

This project is a Python-based **Business Process Automation** solution designed to automate repetitive Excel data-processing and document-generation tasks.

The automation reduces manual work involved in:

* Processing structured Excel data
* Separating data based on item/part information
* Generating organized Excel worksheets
* Generating separate PDF documents
* Creating box/tag-related documents
* Generating index PDFs
* Organizing PDFs into their associated folders
* Merging multiple PDFs into a final document
* Validating the automation through unit testing

The project follows a modular approach so that additional business automation processes can be added in the future.

> **Confidentiality:** Actual company, client, customer, supplier, transaction, pricing, item-code and document data are intentionally excluded from this repository.

---

# Project Structure

```text
business-process-automation/
│
├── 1_invoice_generator.py
├── 2_separate_pdf_generator.py
├── box_tag_generator.py
├── final_index_page_generator.py
│
├── test_1_invoice_generator.py
├── test_2_separate_pdf_generator.py
├── test_box_tag_generator.py
├── test_final_index_page_generator.py
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── dispatched_details.xlsx       # Local/company input - NOT committed
├── output_file.xlsx              # Generated output - NOT committed
│
├── input_folder/                 # Local/company files - NOT committed
│   ├── <part_no_1>/
│   │   ├── A.pdf
│   │   └── other.pdf
│   │
│   └── <part_no_2>/
│       ├── A.pdf
│       └── other.pdf
│
├── index_pdf/                    # Generated index PDFs - NOT committed
│   ├── <part_no_1>.pdf
│   └── <part_no_2>.pdf
│
└── venv/                         # Local virtual environment - NOT committed
```

---

# Automation Workflow

The overall business automation workflow can be represented as:

```text
                    Input Excel / Business Data
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ 1_invoice_generator.py  │
                 │                         │
                 │ Excel Data Processing   │
                 │ Data Separation         │
                 └────────────┬────────────┘
                              │
                              ▼
                    Organized Excel File
                              │
                              ▼
              ┌──────────────────────────────┐
              │ 2_separate_pdf_generator.py │
              │                              │
              │ Excel → Separate PDFs        │
              └──────────────┬───────────────┘
                             │
                             ▼
                     Separate PDF Files
                             │
                             ▼
                  ┌──────────────────────┐
                  │ box_tag_generator.py │
                  │                      │
                  │ Box / Tag Generation │
                  └──────────┬───────────┘
                             │
                             ▼
                      Box / Tag Documents
                             │
                             ▼
              ┌──────────────────────────────┐
              │ final_index_page_generator │
              │                              │
              │ Index PDF Generation        │
              │ PDF Organization            │
              │ PDF Merging                 │
              └──────────────┬───────────────┘
                             │
                             ▼
                       Final PDF Output
```

---

# 1. Excel Data Processing

## File

```text
1_invoice_generator.py
```

## Purpose

The first automation processes the input Excel file and separates the records according to the required business identifier.

The program automates tasks that would otherwise require manually filtering and copying Excel data.

The process generally includes:

1. Reading the input Excel file.
2. Identifying the required column.
3. Grouping records according to the business identifier.
4. Cleaning values before using them as worksheet names.
5. Creating separate worksheets.
6. Writing the corresponding records to each worksheet.
7. Generating the processed Excel workbook.

### Example

Actual company data is not included in this repository.

A sanitized example:

```text
Input Excel

Item Cd    Description       Quantity
A100       Product A         10
B200       Product B         20
A100       Product A         15
C300       Product C         5
```

The automation can produce:

```text
output_invoice.xlsx

├── Part_no_A100
├── Part_no_B200
└── Part_no_C300
```

Each worksheet contains the records belonging to the corresponding item code.

---

# 2. Separate PDF Generation

## File

```text
2_separate_pdf_generator.py
```

## Purpose

The second automation converts the processed Excel workbook into separate PDF documents.

The program automatically:

1. Reads the generated Excel workbook.
2. Identifies the worksheets.
3. Reads worksheet data.
4. Processes the required fields.
5. Creates PDF documents.
6. Formats the PDF using the required page layout.
7. Saves the PDFs separately.
8. Organizes the generated documents into the required output structure.

### Conceptual Flow

```text
Processed Excel
      │
      ▼
Read Worksheets
      │
      ▼
Process Worksheet Data
      │
      ▼
Create PDF
      │
      ▼
Separate PDF Files
```

Actual company item codes, descriptions and business data are intentionally excluded.

---

# 3. Box / Tag Generation

## File

```text
box_tag_generator.py
```

## Purpose

The third automation handles the generation of box/tag-related documents required as part of the business process.

The automation is designed to reduce manual document preparation and maintain consistency in the generated documents.

The general process is:

```text
Input / Processed Data
        │
        ▼
Read Required Information
        │
        ▼
Prepare Box / Tag Data
        │
        ▼
Generate Required Documents
        │
        ▼
Box / Tag Output
```

The actual company-specific box information, identifiers, labels and document contents are not included in this repository.

---

# 4. Final Index Page and PDF Processing

## File

```text
final_index_page_generator.py
```

## Purpose

The final automation performs the final PDF-processing stage of the workflow.

It performs multiple operations:

1. Processes dispatched Excel details.
2. Groups data according to `Part no`.
3. Creates separate Excel worksheets.
4. Generates an index PDF for each part number.
5. Places the generated index PDF into the corresponding folder.
6. Renames the index PDF to `A.pdf`.
7. Reads PDF files inside each associated folder.
8. Sorts the PDF files.
9. Merges the PDFs.
10. Generates a final merged PDF for each folder.

---

## Final Index Workflow

```text
dispatched_details.xlsx
          │
          ▼
Group by Part no
          │
          ▼
output_file.xlsx
          │
          ▼
Generate Index PDFs
          │
          ▼
index_pdf/
          │
          ▼
Find Associated Folder
          │
          ▼
Move Index PDF
          │
          ▼
A.pdf
          │
          ▼
Collect PDFs in Folder
          │
          ▼
Sort PDF Files
          │
          ▼
Merge PDFs
          │
          ▼
<folder_name>_merged.pdf
```

---

# PDF Organization

The final processing stage uses a folder structure similar to:

```text
input_folder/
│
├── <part_no_1>/
│   ├── A.pdf
│   ├── document_1.pdf
│   ├── document_2.pdf
│   └── <part_no_1>_merged.pdf
│
└── <part_no_2>/
    ├── A.pdf
    ├── document_1.pdf
    ├── document_2.pdf
    └── <part_no_2>_merged.pdf
```

The actual company folder names and PDF documents are intentionally excluded.

---

# Technologies Used

The project uses the following technologies and Python libraries:

* **Python**
* **Pandas**
* **OpenPyXL**
* **XlsxWriter**
* **ReportLab**
* **PyPDF2**
* **Pytest**
* **Git**
* **GitHub**

---

# Requirements

Recommended Python version:

```text
Python 3.12
```

Required packages:

```text
pandas
openpyxl
xlsxwriter
reportlab
PyPDF2
pytest
```

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd business-process-automation
```

---

## 2. Create a Virtual Environment

Linux/macOS:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Automation

## Excel Processing

Run:

```bash
python 1_invoice_generator.py
```

This processes the input Excel data and generates the required Excel output.

---

## PDF Generation

Run:

```bash
python 2_separate_pdf_generator.py
```

This generates the required PDF documents from the processed Excel data.

---

## Box / Tag Generation

Run:

```bash
python box_tag_generator.py
```

This executes the box/tag document generation process.

---

## Final PDF Processing

Run:

```bash
python final_index_page_generator.py
```

This performs the final index generation, PDF organization and PDF merging workflow.

---

# Unit Testing

The project uses **Pytest** for automated unit testing.

Each major automation module has a corresponding test file.

```text
1_invoice_generator.py
        │
        ▼
test_1_invoice_generator.py

2_separate_pdf_generator.py
        │
        ▼
test_2_separate_pdf_generator.py

box_tag_generator.py
        │
        ▼
test_box_tag_generator.py

final_index_page_generator.py
        │
        ▼
test_final_index_page_generator.py
```

---

# Run All Tests

From the project root:

```bash
python -m pytest -v
```

---

# Run Individual Test Files

### Excel automation tests

```bash
python -m pytest -v test_1_invoice_generator.py
```

### PDF generation tests

```bash
python -m pytest -v test_2_separate_pdf_generator.py
```

### Box/tag tests

```bash
python -m pytest -v test_box_tag_generator.py
```

### Final PDF processing tests

```bash
python -m pytest -v test_final_index_page_generator.py
```

---

# Testing Approach

The unit tests are designed to validate individual functions and important workflow conditions without requiring real company data.

## Excel Automation Tests

Tests may validate:

* Input file handling
* Excel readability
* Required columns
* Data grouping
* Worksheet creation
* Correct worksheet data
* Output file creation
* Invalid or missing input handling

---

## PDF Generation Tests

Tests may validate:

* Excel workbook reading
* Worksheet processing
* PDF creation
* PDF output path
* PDF file existence
* PDF validity
* PDF page generation
* Error handling

---

## Box / Tag Tests

Tests may validate:

* Input data handling
* Required fields
* Box/tag generation
* Output document creation
* File naming
* Invalid input handling
* Output validation

---

## Final PDF Processing Tests

Tests include validation of:

* Excel grouping
* Part number worksheets
* Index PDF generation
* PDF validity
* Index PDF movement
* Missing associated folders
* Empty PDF folders
* Multiple PDF merging
* Merged PDF page count
* Corrupted PDF handling

---

# Test Data

Unit tests should use **temporary or sanitized test data** rather than actual company information.

For example:

```python
data = pd.DataFrame({
    "Part no": ["P001", "P001"],
    "Item": ["Test A", "Test B"],
    "Quantity": [10, 20]
})
```

This allows the automation to be tested without exposing business information.

Pytest's temporary directories can also be used:

```python
tmp_path
```

This prevents tests from modifying actual project files.

---

# Data Privacy and Security

This repository is intended to contain:

```text
✓ Source code
✓ Unit tests
✓ Sanitized examples
✓ Generic documentation
✓ Requirements
```

It should not contain:

```text
❌ Real company data
❌ Customer information
❌ Supplier information
❌ Employee information
❌ Real invoices
❌ Real transaction records
❌ Pricing information
❌ Confidential item codes
❌ Internal identifiers
❌ Internal documents
❌ Credentials
❌ API keys
❌ Passwords
❌ Access tokens
❌ Private configuration files
```

---

# Files That Should Not Be Committed

The following files should normally remain outside the public GitHub repository:

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

Company-specific input and output folders should also be excluded.

---

# Recommended `.gitignore`

A basic `.gitignore` can contain:

```gitignore
# Virtual environment
venv/
.venv/

# Python
__pycache__/
*.py[cod]

# Pytest
.pytest_cache/
.hypothesis/

# Excel files
*.xlsx
*.xls
*.xlsm

# PDF files
*.pdf

# Output directories
output/
index_pdf/
input_folder/

# Logs
*.log
logs/

# Environment / secrets
.env
*.key
*.pem

# IDE
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db
```

If a particular Excel/PDF file is intentionally required as a sanitized public example, it can be explicitly allowed instead of globally excluding it.

---

# Development Workflow

The development process can be represented as:

```text
Prepare Sanitized Input
          │
          ▼
Process Excel Data
          │
          ▼
Generate Excel Output
          │
          ▼
Generate Separate PDFs
          │
          ▼
Generate Box / Tag Documents
          │
          ▼
Generate Index PDFs
          │
          ▼
Organize PDFs
          │
          ▼
Merge PDFs
          │
          ▼
Run Unit Tests
          │
          ▼
Review Output
          │
          ▼
Commit Source Code
          │
          ▼
Push to GitHub
```

---

# Git Workflow

Before committing code, verify that confidential files are not included.

Check repository status:

```bash
git status
```

Add source files:

```bash
git add *.py
git add README.md
git add requirements.txt
git add .gitignore
```

Commit:

```bash
git commit -m "Add business process automation"
```

Push:

```bash
git push
```

Before pushing, verify:

```bash
git status
```

and inspect the files being committed.

---

# Project Benefits

The automation provides several benefits:

* Reduces repetitive manual Excel operations
* Reduces manual document generation
* Provides consistent output formatting
* Reduces manual PDF organization
* Automates PDF merging
* Improves repeatability
* Makes the process easier to test
* Provides modular Python components
* Allows future automation modules to be added

---

# Future Improvements

Potential future improvements include:

* Centralized configuration
* Improved input validation
* Structured error handling
* Production-grade logging
* Database integration
* REST API integration
* Automated email generation
* Automated email attachments
* PDF content validation
* Configuration through environment variables
* Scheduled automation
* Automated deployment
* CI/CD integration
* GitHub Actions for automated testing
* Improved test coverage
* User interface for non-technical users

---

# Important Note

This repository provides a generalized representation of a business process automation solution.

Company-specific implementation details, business rules, confidential information, customer data, supplier data, transaction information, internal documents and proprietary identifiers are intentionally excluded.

The purpose of this repository is to demonstrate the **technical architecture, automation approach, Python development practices and testing methodology** without exposing confidential business information.

---

## Author

**Om Suryakant Ugale**

Python Developer | Automation | AI/ML | Software Development

---

## License

Add the appropriate license based on the ownership and distribution requirements of the project.

If this is company-owned or client-owned software, do not add an open-source license without authorization.
