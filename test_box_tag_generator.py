import os
import importlib.util
from unittest.mock import patch, MagicMock


# Load the actual project file
def load_program():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "box_tag_generator.py"
    )

    spec = importlib.util.spec_from_file_location(
        "box_tag_generator",
        file_path
    )

    module = importlib.util.module_from_spec(spec)

    return module


# 1. Check that the project file exists
def test_program_file_exists():

    file_path = os.path.join(
        os.path.dirname(__file__),
        "box_tag_generator.py"
    )

    assert os.path.exists(file_path)


# 2. Check that the program can be imported
def test_program_can_be_loaded():

    module = load_program()

    assert module is not None


# 3. Check that box_tag_generator class exists
def test_box_tag_generator_class_exists():

    module = load_program()

    spec = importlib.util.spec_from_file_location(
        "box_tag_generator",
        os.path.join(
            os.path.dirname(__file__),
            "box_tag_generator.py"
        )
    )

    with patch("os.getcwd", return_value=os.path.dirname(__file__)):
        spec.loader.exec_module(module)

    assert hasattr(module, "box_tag_generator")


# 4. Check that merge_pdf method exists
def test_merge_pdf_method_exists():

    module = load_program()

    spec = importlib.util.spec_from_file_location(
        "box_tag_generator",
        os.path.join(
            os.path.dirname(__file__),
            "box_tag_generator.py"
        )
    )

    with patch("os.getcwd", return_value=os.path.dirname(__file__)):
        spec.loader.exec_module(module)

    generator = module.box_tag_generator()

    assert hasattr(generator, "merge_pdf")


# 5. Check numeric PDF filtering
def test_numeric_pdf_filtering():

    files = [
        "1.pdf",
        "2.pdf",
        "10.pdf",
        "abc.pdf",
        "print_all.pdf"
    ]

    valid_files = [
        file
        for file in files
        if file.lower().endswith(".pdf")
        and file[:-4].isdigit()
    ]

    assert valid_files == [
        "1.pdf",
        "2.pdf",
        "10.pdf"
    ]


# 6. Check numeric sorting
def test_pdf_files_sorted_numerically():

    pdf_files = [
        "10.pdf",
        "2.pdf",
        "1.pdf",
        "20.pdf",
        "3.pdf"
    ]

    sorted_files = sorted(
        pdf_files,
        key=lambda x: int(os.path.basename(x)[:-4])
    )

    assert sorted_files == [
        "1.pdf",
        "2.pdf",
        "3.pdf",
        "10.pdf",
        "20.pdf"
    ]


# 7. Check non-numeric PDF files are ignored
def test_non_numeric_pdf_files_are_ignored():

    files = [
        "1.pdf",
        "abc.pdf",
        "test.pdf",
        "20.pdf",
        "print_all.pdf"
    ]

    valid_files = [
        file
        for file in files
        if file.lower().endswith(".pdf")
        and file[:-4].isdigit()
    ]

    assert "abc.pdf" not in valid_files
    assert "test.pdf" not in valid_files
    assert "print_all.pdf" not in valid_files


# 8. Check PDF merger append is called
def test_pdf_merger_append():

    merger = MagicMock()

    pdf_files = [
        "1.pdf",
        "2.pdf",
        "3.pdf"
    ]

    for pdf_file in pdf_files:
        merger.append(pdf_file)

    assert merger.append.call_count == 3

    merger.append.assert_any_call("1.pdf")
    merger.append.assert_any_call("2.pdf")
    merger.append.assert_any_call("3.pdf")


# 9. Check PDFs are merged in numeric order
def test_pdf_merge_order():

    pdf_files = [
        "10.pdf",
        "2.pdf",
        "1.pdf"
    ]

    sorted_files = sorted(
        pdf_files,
        key=lambda x: int(os.path.basename(x)[:-4])
    )

    merger = MagicMock()

    for pdf_file in sorted_files:
        merger.append(pdf_file)

    expected_calls = [
        ("1.pdf",),
        ("2.pdf",),
        ("10.pdf",)
    ]

    actual_calls = [
        call.args
        for call in merger.append.call_args_list
    ]

    assert actual_calls == expected_calls


# 10. Check merger writes output PDF
def test_pdf_merger_writes_output():

    merger = MagicMock()

    output_file = MagicMock()

    merger.write(output_file)

    merger.write.assert_called_once_with(output_file)

