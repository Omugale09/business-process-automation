import os
import pandas as pd
import PyPDF2

import final_index_page_generator as generator


# ============================================================
# TEST 1: Excel file is created and grouped by Part no
# ============================================================

def test_sort_the_file_as_per_part_no(tmp_path, monkeypatch):

    input_file = tmp_path / "dispatched_details.xlsx"
    output_file = tmp_path / "output_file.xlsx"

    data = pd.DataFrame({
        "Part no": ["P001", "P002", "P001"],
        "Item": ["Item A", "Item B", "Item C"],
        "Quantity": [10, 20, 30]
    })

    data.to_excel(input_file, index=False)

    monkeypatch.setattr(
        generator,
        "input_file_path",
        str(input_file)
    )

    monkeypatch.setattr(
        generator,
        "output_file_path",
        str(output_file)
    )

    generator.sort_the_file_as_per_part_no()

    assert output_file.exists()

    excel_file = pd.ExcelFile(output_file)

    assert "Part_no_P001" in excel_file.sheet_names
    assert "Part_no_P002" in excel_file.sheet_names


# ============================================================
# TEST 2: Correct rows are stored in each Part no sheet
# ============================================================

def test_correct_rows_in_part_no_sheet(tmp_path, monkeypatch):

    input_file = tmp_path / "input.xlsx"
    output_file = tmp_path / "output.xlsx"

    data = pd.DataFrame({
        "Part no": ["P001", "P001", "P002"],
        "Item": ["A", "B", "C"]
    })

    data.to_excel(input_file, index=False)

    monkeypatch.setattr(
        generator,
        "input_file_path",
        str(input_file)
    )

    monkeypatch.setattr(
        generator,
        "output_file_path",
        str(output_file)
    )

    generator.sort_the_file_as_per_part_no()

    p001 = pd.read_excel(
        output_file,
        sheet_name="Part_no_P001"
    )

    p002 = pd.read_excel(
        output_file,
        sheet_name="Part_no_P002"
    )

    assert len(p001) == 2
    assert len(p002) == 1


# ============================================================
# TEST 3: PDF is generated from output Excel
# ============================================================

def test_make_pdf_file_from_output_excel(tmp_path, monkeypatch):

    data = pd.DataFrame({
        "Part no": ["P001", "P001"],
        "Item": ["A", "B"],
        "Quantity": [10, 20]
    })

    # Create output_file.xlsx inside temporary folder
    output_excel = tmp_path / "output_file.xlsx"

    with pd.ExcelWriter(
        output_excel,
        engine="xlsxwriter"
    ) as writer:

        data.to_excel(
            writer,
            sheet_name="Part_no_P001",
            index=False
        )

    # Change current working directory temporarily
    monkeypatch.chdir(tmp_path)

    # Run the actual function
    generator.make_pdf_file_from_the_output_excel()

    # Function creates index_pdf automatically
    pdf_file = tmp_path / "index_pdf" / "P001.pdf"

    # Check PDF was created
    assert pdf_file.exists()

    # Check PDF is not empty
    assert pdf_file.stat().st_size > 0

# ============================================================
# TEST 4: Generated PDF is valid
# ============================================================

def test_generated_pdf_is_valid(tmp_path, monkeypatch):

    data = pd.DataFrame({
        "Part no": ["P001"],
        "Item": ["Test Item"],
        "Quantity": [5]
    })

    # Create output_file.xlsx inside temporary folder
    output_excel = tmp_path / "output_file.xlsx"

    with pd.ExcelWriter(
        output_excel,
        engine="xlsxwriter"
    ) as writer:

        data.to_excel(
            writer,
            sheet_name="Part_no_P001",
            index=False
        )

    # Change current working directory temporarily
    monkeypatch.chdir(tmp_path)

    # Run the actual function
    generator.make_pdf_file_from_the_output_excel()

    # Find generated PDF
    pdf_file = tmp_path / "index_pdf" / "P001.pdf"

    # Check PDF exists
    assert pdf_file.exists()

    # Open PDF
    reader = PyPDF2.PdfReader(str(pdf_file))

    # Check PDF contains at least one page
    assert len(reader.pages) > 0
    
# ============================================================
# TEST 5: Index PDF moves to associated folder as A.pdf
# ============================================================

def test_place_index_file_in_associated_folder(
    tmp_path,
    monkeypatch
):

    index_folder = tmp_path / "index_pdf"
    input_folder = tmp_path / "input_folder"

    index_folder.mkdir()
    input_folder.mkdir()

    part_folder = input_folder / "P001"
    part_folder.mkdir()

    pdf_file = index_folder / "P001.pdf"

    pdf_file.write_bytes(b"%PDF-test")

    monkeypatch.setattr(
        generator,
        "index_folder",
        str(index_folder)
    )

    monkeypatch.setattr(
        generator,
        "input_folder",
        str(input_folder)
    )

    generator.place_index_file_in_associated_folder()

    moved_file = part_folder / "A.pdf"

    assert moved_file.exists()
    assert not pdf_file.exists()


# ============================================================
# TEST 6: PDF remains in index_pdf if folder doesn't exist
# ============================================================

def test_index_pdf_remains_if_folder_missing(
    tmp_path,
    monkeypatch
):

    index_folder = tmp_path / "index_pdf"
    input_folder = tmp_path / "input_folder"

    index_folder.mkdir()
    input_folder.mkdir()

    pdf_file = index_folder / "P999.pdf"

    pdf_file.write_bytes(b"%PDF-test")

    monkeypatch.setattr(
        generator,
        "index_folder",
        str(index_folder)
    )

    monkeypatch.setattr(
        generator,
        "input_folder",
        str(input_folder)
    )

    generator.place_index_file_in_associated_folder()

    assert pdf_file.exists()


# ============================================================
# TEST 7: Empty folder does not create merged PDF
# ============================================================

def test_merge_empty_folder(tmp_path):

    folder = tmp_path / "P001"
    folder.mkdir()

    generator.merge_pdfs_in_folder(str(folder))

    merged_file = folder / "P001_merged.pdf"

    assert not merged_file.exists()


# ============================================================
# TEST 8: Two PDFs are merged successfully
# ============================================================

def test_merge_two_pdfs(tmp_path):

    folder = tmp_path / "P001"
    folder.mkdir()

    pdf1 = folder / "A.pdf"
    pdf2 = folder / "B.pdf"

    create_test_pdf(pdf1, "PDF A")
    create_test_pdf(pdf2, "PDF B")

    generator.merge_pdfs_in_folder(str(folder))

    merged_file = folder / "P001_merged.pdf"

    assert merged_file.exists()
    assert merged_file.stat().st_size > 0


# ============================================================
# TEST 9: Merged PDF has correct number of pages
# ============================================================

def test_merged_pdf_page_count(tmp_path):

    folder = tmp_path / "P001"
    folder.mkdir()

    pdf1 = folder / "A.pdf"
    pdf2 = folder / "B.pdf"

    create_test_pdf(pdf1, "PDF A")
    create_test_pdf(pdf2, "PDF B")

    generator.merge_pdfs_in_folder(str(folder))

    merged_file = folder / "P001_merged.pdf"

    reader = PyPDF2.PdfReader(str(merged_file))

    assert len(reader.pages) == 2


# ============================================================
# TEST 10: Corrupted PDF is skipped
# ============================================================

def test_corrupted_pdf_is_skipped(tmp_path):

    folder = tmp_path / "P001"
    folder.mkdir()

    bad_pdf = folder / "bad.pdf"
    good_pdf = folder / "good.pdf"

    bad_pdf.write_bytes(b"This is not a valid PDF")

    create_test_pdf(good_pdf, "GOOD PDF")

    generator.merge_pdfs_in_folder(str(folder))

    merged_file = folder / "P001_merged.pdf"

    assert merged_file.exists()

    reader = PyPDF2.PdfReader(str(merged_file))

    assert len(reader.pages) == 1


# ============================================================
# HELPER FUNCTION
# ============================================================

def create_test_pdf(file_path, text):

    from reportlab.pdfgen import canvas

    c = canvas.Canvas(str(file_path))

    c.drawString(100, 700, text)

    c.save()