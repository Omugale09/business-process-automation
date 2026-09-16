import pandas as pd
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Spacer
from io import BytesIO
import shutil
import os
import PyPDF2

cd_path = os.getcwd()
input_file_path = os.path.join(cd_path, "dispatched_details .xlsx")
output_file_path = os.path.join(cd_path, "output_file.xlsx")
input_folder = os.path.join(os.getcwd(), "input_folder")
index_folder = os.path.join(os.getcwd(), "index_pdf")


def sort_the_file_as_per_part_no():
    df = pd.read_excel(input_file_path)
    grouped = df.groupby('Part no')

    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        for invoice_no, group in grouped:
            cleaned_invoice_no = ''.join(c for c in str(invoice_no) if c.isalnum() or c in ['-', '_', ' '])
            if cleaned_invoice_no and cleaned_invoice_no not in writer.sheets:
                group.to_excel(writer, sheet_name=f'Part_no_{cleaned_invoice_no}', index=False)

    print(f"Output Excel file has been generated:----Done---- {output_file_path}")


def make_pdf_file_from_the_output_excel():
    output_folder = os.path.join(os.getcwd(), f"index_pdf")
    os.makedirs(output_folder, exist_ok=True)
    input_file_path = os.path.join(os.getcwd(), "output_file.xlsx")
    xls = pd.ExcelFile(input_file_path)
    sheet_data = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
    font_size = 28

    for sheet_name, data in sheet_data.items():
        pdf_buffer = BytesIO()
        pdf_file_name = f"{data.iloc[0]['Part no']}.pdf"
        doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4))
        elements = []
        data_list = [data.columns.tolist()]
        data_list.extend(data.values.tolist())
        col_widths = [100] * len(data.columns)

        row_heights = [24] * len(data_list)
        header_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), (1, 1, 1)),
            ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold', font_size),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, 0), 1, (0, 0, 0)),
        ])

        data_style = TableStyle([
            ('BACKGROUND', (0, 1), (-1, -1), (1, 1, 1)),
            ('TEXTCOLOR', (0, 1), (-1, -1), (0, 0, 0)),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica', font_size),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
            ('GRID', (0, 1), (-1, -1), 1, (0, 0, 0)),
        ])

        table = Table(data_list, colWidths=col_widths, rowHeights=row_heights)
        table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), (1, 1, 1)),
            ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
        ])

        for i in range(len(data_list)):
            if i == 0:
                table.setStyle(header_style)
            else:
                table.setStyle(data_style)

        available_height = doc.height - (doc.topMargin + doc.bottomMargin)
        table_height = table.wrap(doc.width, available_height)[1]

        if table_height < available_height:
            space_height = (available_height - table_height) / 2
            elements.append(Spacer(1, space_height))

        elements.append(table)
        doc.build(elements)

        pdf_buffer.seek(0)
        pdf_file_path = os.path.join(output_folder, pdf_file_name)

        with open(pdf_file_path, 'wb') as f:
            f.write(pdf_buffer.read())

        print(f"Output PDF file has been generated:----Done---- {pdf_file_path}")


def place_index_file_in_associated_folder():
    for pdf_file in os.listdir(index_folder):
        if pdf_file.lower().endswith(".pdf"):
            pdf_file_path = os.path.join(index_folder, pdf_file)
            folder_name = os.path.splitext(pdf_file)[0]
            destination_folder = os.path.join(input_folder, folder_name)

            if os.path.exists(destination_folder):
                new_pdf_path = os.path.join(destination_folder, "A.pdf")
                shutil.move(pdf_file_path, new_pdf_path)
                print(f"Moved '{pdf_file}' to '{new_pdf_path}'")
            else:
                print(f"Folder '{folder_name}' not found in '{input_folder}'. Skipping '{pdf_file}'.")

    print("Index file generated ----Done---- ")


def merge_pdfs_in_folder(folder_path):
    pdf_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if
                 filename.lower().endswith(".pdf")]

    if not pdf_files:
        return


    pdf_files = sorted(pdf_files)


    pdf_merger = PyPDF2.PdfMerger()


    for pdf_file in pdf_files:
        try:
            pdf_merger.append(pdf_file)
        except Exception as e:
            print(f"Skipping '{pdf_file}' due to an error: {e}")


    if len(pdf_merger.pages) > 0:

        folder_name = os.path.basename(folder_path)
        output_pdf = os.path.join(folder_path, f"{folder_name}_merged.pdf")


        pdf_merger.write(output_pdf)
        pdf_merger.close()
        print(f"Merged PDFs in '{folder_name}' and saved as '{folder_name}_merged.pdf'.")


sort = sort_the_file_as_per_part_no()
make = make_pdf_file_from_the_output_excel()
place = place_index_file_in_associated_folder()
for folder_name in os.listdir(input_folder):
    folder_path = os.path.join(input_folder, folder_name)

    # Check if the item is a folder
    if os.path.isdir(folder_path):
        merge_pdfs_in_folder(folder_path)

print("PDF merging completed.----Done---- ")
