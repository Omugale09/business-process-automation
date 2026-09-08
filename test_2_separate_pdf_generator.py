import os
import importlib.util
from unittest.mock import patch
import pandas as pd


def load_program():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "2_separate_pdf_generator.py"
    )

    spec = importlib.util.spec_from_file_location(
        "invoice_pdf_generator",
        file_path
    )

    module = importlib.util.module_from_spec(spec)

    with patch("os.getcwd", return_value=os.path.dirname(__file__)):
        spec.loader.exec_module(module)

    return module


# 1. Check input Excel file exists
def test_input_file_exists():
    input_file = os.path.join(
        os.path.dirname(__file__),
        "output_invoice.xlsx"
    )

    assert os.path.exists(input_file)


# 2. Check Excel file can be read
def test_input_excel_can_be_read():
    input_file = os.path.join(
        os.path.dirname(__file__),
        "output_invoice.xlsx"
    )

    xls = pd.ExcelFile(input_file)

    assert xls is not None


# 3. Check Excel contains sheets
def test_input_excel_has_sheets():
    input_file = os.path.join(
        os.path.dirname(__file__),
        "output_invoice.xlsx"
    )

    xls = pd.ExcelFile(input_file)

    assert len(xls.sheet_names) > 0


# 4. Check required Item Cd column
def test_item_cd_column_exists():
    input_file = os.path.join(
        os.path.dirname(__file__),
        "output_invoice.xlsx"
    )

    xls = pd.ExcelFile(input_file)

    for sheet_name in xls.sheet_names:
        data = xls.parse(sheet_name)

        assert "Item Cd" in data.columns


# 5. Check required Item Description column
def test_item_description_column_exists():
    input_file = os.path.join(
        os.path.dirname(__file__),
        "output_invoice.xlsx"
    )

    xls = pd.ExcelFile(input_file)

    for sheet_name in xls.sheet_names:
        data = xls.parse(sheet_name)

        assert "Item Description" in data.columns


# 6. Check program runs successfully
def test_program_runs():
    module = load_program()

    assert module is not None


# 7. Check output folder is created
def test_output_folder_created():
    module = load_program()

    assert os.path.exists(module.output_folder)
    assert os.path.isdir(module.output_folder)


# 8. Check PDF files are generated
def test_pdf_files_are_created():
    module = load_program()

    pdf_files = [
        file
        for file in os.listdir(module.output_folder)
        if file.lower().endswith(".pdf")
    ]

    assert len(pdf_files) > 0


# 9. Check generated files are valid PDF files
def test_generated_files_are_valid_pdf():
    module = load_program()

    pdf_files = [
        file
        for file in os.listdir(module.output_folder)
        if file.lower().endswith(".pdf")
    ]

    for file in pdf_files:
        file_path = os.path.join(module.output_folder, file)

        with open(file_path, "rb") as f:
            content = f.read()

        assert content.startswith(b"%PDF")
        assert b"%%EOF" in content


# 10. Check number of PDFs matches Excel sheets
def test_pdf_count_matches_sheet_count():
    module = load_program()

    xls = pd.ExcelFile(module.input_file_path)

    pdf_files = [
        file
        for file in os.listdir(module.output_folder)
        if file.lower().endswith(".pdf")
    ]

    assert len(pdf_files) == len(xls.sheet_names)