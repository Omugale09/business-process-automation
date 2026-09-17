import os
import csv
import ast
import types

import pytest
import PyPDF2


# =========================================================
# LOAD pdf_merger_new.py WITHOUT RUNNING THE CODE AT BOTTOM
# =========================================================

with open("pdf_merger_new.py", "r") as f:
    source = f.read()

tree = ast.parse(source)

allowed_nodes = []

for node in tree.body:

    if isinstance(
        node,
        (
            ast.Import,
            ast.ImportFrom,
            ast.Assign,
            ast.FunctionDef
        )
    ):
        allowed_nodes.append(node)


module = ast.Module(
    body=allowed_nodes,
    type_ignores=[]
)

compiled_code = compile(
    module,
    "pdf_merger_new.py",
    "exec"
)

generator = types.ModuleType(
    "pdf_merger_new"
)

exec(
    compiled_code,
    generator.__dict__
)


# =========================================================
# HELPER FUNCTION
# =========================================================

def create_test_pdf(file_path):

    writer = PyPDF2.PdfWriter()

    writer.add_blank_page(
        width=300,
        height=300
    )

    with open(file_path, "wb") as f:
        writer.write(f)


# =========================================================
# TEST 1
# =========================================================

def test_index_csv_exists(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    csv_file = tmp_path / "index.csv"

    with open(csv_file, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Part No",
            "Quantity"
        ])

        writer.writerow([
            "P001",
            "10"
        ])

    assert csv_file.exists()


# =========================================================
# TEST 2
# =========================================================

def test_index_csv_can_be_read(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    csv_file = tmp_path / "index.csv"

    with open(csv_file, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Part No",
            "Quantity"
        ])

        writer.writerow([
            "P001",
            "10"
        ])

    with open(csv_file, "r") as f:

        reader = csv.reader(f)

        data = list(reader)

    assert len(data) == 2


# =========================================================
# TEST 3
# =========================================================

def test_create_index_generates_pdf(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    # Update the global path used by create_index()
    generator.cd_path = str(tmp_path)

    csv_file = tmp_path / "input.csv"

    with open(csv_file, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Part No",
            "Quantity"
        ])

        writer.writerow([
            "P001",
            "10"
        ])

    generator.create_index()

    pdf_file = tmp_path / "A.pdf"

    assert pdf_file.exists()


# =========================================================
# TEST 4
# =========================================================

def test_generated_index_pdf_not_empty(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    generator.cd_path = str(tmp_path)

    csv_file = tmp_path / "input.csv"

    with open(csv_file, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Part No",
            "Quantity"
        ])

        writer.writerow([
            "P001",
            "10"
        ])

    generator.create_index()

    pdf_file = tmp_path / "A.pdf"

    assert pdf_file.stat().st_size > 0


# =========================================================
# TEST 5
# =========================================================

def test_generated_index_pdf_is_valid(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    generator.cd_path = str(tmp_path)

    csv_file = tmp_path / "input.csv"

    with open(csv_file, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "Part No",
            "Quantity"
        ])

        writer.writerow([
            "P001",
            "10"
        ])

    generator.create_index()

    pdf_file = tmp_path / "A.pdf"

    reader = PyPDF2.PdfReader(
        str(pdf_file)
    )

    assert len(reader.pages) > 0


# =========================================================
# TEST 6
# =========================================================

def test_merge_folder_with_no_pdfs(tmp_path):

    folder = tmp_path / "Folder1"

    folder.mkdir()

    generator.merge_pdfs_in_folder(
        str(folder)
    )

    merged_file = folder / "Folder1_merged.pdf"

    assert not merged_file.exists()


# =========================================================
# TEST 7
# =========================================================

def test_merge_one_pdf(tmp_path):

    folder = tmp_path / "Folder1"

    folder.mkdir()

    pdf_file = folder / "1.pdf"

    create_test_pdf(
        pdf_file
    )

    generator.merge_pdfs_in_folder(
        str(folder)
    )

    merged_file = folder / "Folder1_merged.pdf"

    assert merged_file.exists()


# =========================================================
# TEST 8
# =========================================================

def test_merge_multiple_pdfs(tmp_path):

    folder = tmp_path / "Folder1"

    folder.mkdir()

    create_test_pdf(
        folder / "1.pdf"
    )

    create_test_pdf(
        folder / "2.pdf"
    )

    generator.merge_pdfs_in_folder(
        str(folder)
    )

    merged_file = folder / "Folder1_merged.pdf"

    assert merged_file.exists()


# =========================================================
# TEST 9
# =========================================================

def test_merged_pdf_page_count(tmp_path):

    folder = tmp_path / "Folder1"

    folder.mkdir()

    create_test_pdf(
        folder / "1.pdf"
    )

    create_test_pdf(
        folder / "2.pdf"
    )

    generator.merge_pdfs_in_folder(
        str(folder)
    )

    merged_file = folder / "Folder1_merged.pdf"

    reader = PyPDF2.PdfReader(
        str(merged_file)
    )

    assert len(reader.pages) == 2


# =========================================================
# TEST 10
# =========================================================

def test_empty_pdf_causes_error(tmp_path):

    folder = tmp_path / "Folder1"

    folder.mkdir()

    empty_pdf = folder / "empty.pdf"

    empty_pdf.touch()

    with pytest.raises(
        PyPDF2.errors.EmptyFileError
    ):

        generator.merge_pdfs_in_folder(
            str(folder)
        )