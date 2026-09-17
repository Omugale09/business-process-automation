import PyPDF2
import os
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

cd_path = os.getcwd()
input_file_path = os.path.join(cd_path, "pdf_output_14")
pdf_output_dir = os.path.join(cd_path, "pdf_output")


def create_index():
    input_csv_file = os.path.join(cd_path, "input.csv")
    output_pdf_file = os.path.join(cd_path, "A.pdf")

    data = []
    with open(input_csv_file, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)
    doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)
    elements = [table]
    doc.build(elements)

    print(f"PDF saved to {output_pdf_file}")


def merge_pdfs_in_folder(folder_path):
    pdf_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if
                 filename.lower().endswith(".pdf")]

    if not pdf_files:
        return
    pdf_files = sorted(pdf_files)

    pdf_merger = PyPDF2.PdfMerger()
    for pdf_file in pdf_files:
        pdf_merger.append(pdf_file)
    folder_name = os.path.basename(folder_path)
    output_pdf = os.path.join(folder_path, f"{folder_name}_merged.pdf")

    with open(output_pdf, "wb") as output_file:
        pdf_merger.write(output_file)
    pdf_merger.close()


for folder, _, _ in os.walk(input_file_path):
    merge_pdfs_in_folder(folder)

print("PDF merging complete.")
