# box tag generator and all the pdf merge inside one pdf
import os
import PyPDF2
import pandas as pd
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageTemplate, Frame
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Spacer


class box_tag_generator():
    def generate_pdf(self):
        cd_path = os.getcwd()
        input_file_path = os.path.join(cd_path, "input.csv")
        pdf_output_dir = os.path.join(cd_path, "pdf_output_11")
        os.makedirs(pdf_output_dir, exist_ok=True)
        df = pd.read_csv(input_file_path, encoding='utf-8-sig', sep=',', engine='python')
        right_aligned_style = ParagraphStyle('RightAlignedStyle', parent=getSampleStyleSheet()['Heading1'])
        right_aligned_style.alignment = 2 # 2 represents 'right' alignment
        header_1 = Paragraph("Address of the Company", right_aligned_style)
        header_2 = Paragraph("Address of the Company ", right_aligned_style)
        
        grouped = df.groupby('Box_no')
        for box_no, group in grouped:
            output_pdf_file = os.path.join(pdf_output_dir, f'{int(box_no)}.pdf')

            result = group[['Part_name', 'Drg_no', 'Quantity', 'Dispatched_date']]
            result['Verified By'] = '_______________________'

            data = [result.columns.tolist()] + result.values.tolist()
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

            header_0 = Paragraph("Box No : {}".format(int(box_no)), getSampleStyleSheet()['Heading2'])
            story = [header_1, header_2, header_0, Spacer(1, 0.5 * inch), table]
            doc = SimpleDocTemplate(output_pdf_file, pagesize=landscape(A4), fontSize=38)
            doc.build(story)

        print("PDF files have been generated in the 'pdf_output' directory.")

    def merge_pdf(self):
        cd_path = os.getcwd()
        pdf_folder = os.path.join(cd_path, "pdf_output_11")
        output_pdf = os.path.join(cd_path, "pdf_output_11/print_all.pdf")

        pdf_files = [os.path.join(pdf_folder, filename) for filename in os.listdir(pdf_folder) 
                     if filename.lower().endswith(".pdf") and filename[:-4].isdigit()]  # Check if filename is numeric

        # Sort PDF files by their numeric values
        pdf_files = sorted(pdf_files, key=lambda x: int(os.path.basename(x)[:-4]))

        pdf_merger = PyPDF2.PdfMerger()
        for pdf_file in pdf_files:
            pdf_merger.append(pdf_file)
        with open(output_pdf, 'wb') as output_file:
            pdf_merger.write(output_file)
        pdf_merger.close()
        print("All the PDFs have been merged in numeric order")

generate = box_tag_generator()
generate.generate_pdf()
generate.merge_pdf()
