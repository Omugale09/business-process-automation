import os
import importlib.util
import pandas as pd


def load_program():
    file_path = os.path.join(os.getcwd(), "1_invoice_generator.py")

    spec = importlib.util.spec_from_file_location(
        "invoice_generator",
        file_path
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def test_input_file_exists():
    assert os.path.exists("Book1.xlsx")


def test_input_file_can_be_read():
    df = pd.read_excel("Book1.xlsx")

    assert df is not None
    assert not df.empty


def test_item_cd_column_exists():
    df = pd.read_excel("Book1.xlsx")

    assert "Item Cd" in df.columns


def test_item_cd_has_values():
    df = pd.read_excel("Book1.xlsx")

    assert df["Item Cd"].notna().any()


def test_program_runs():
    load_program()

    assert os.path.exists("output_invoice.xlsx")


def test_output_file_can_be_read():
    load_program()

    excel_file = pd.ExcelFile("output_invoice.xlsx")

    assert excel_file is not None


def test_output_has_sheets():
    load_program()

    excel_file = pd.ExcelFile("output_invoice.xlsx")

    assert len(excel_file.sheet_names) > 0


def test_sheet_names_start_with_part_no():
    load_program()

    excel_file = pd.ExcelFile("output_invoice.xlsx")

    for sheet_name in excel_file.sheet_names:
        assert sheet_name.startswith("Part_no_")


def test_output_sheets_contain_data():
    load_program()

    excel_file = pd.ExcelFile("output_invoice.xlsx")

    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(
            "output_invoice.xlsx",
            sheet_name=sheet_name
        )

        assert not df.empty


def test_output_contains_item_cd():
    load_program()

    excel_file = pd.ExcelFile("output_invoice.xlsx")

    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(
            "output_invoice.xlsx",
            sheet_name=sheet_name
        )

        assert "Item Cd" in df.columns