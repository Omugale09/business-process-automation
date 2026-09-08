import pandas as pd
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Spacer
from io import BytesIO
import os
import datetime

today_date = datetime.date.today().strftime("%Y-%m-%d")
output_folder = os.path.join(os.getcwd(), f"invoice_pdf_{today_date}")
os.makedirs(output_folder, exist_ok=True)
input_file_path = os.path.join(os.getcwd(), "sample_business_automation_input.xlsx")
xls = pd.ExcelFile(input_file_path)
sheet_data = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
font_size = 28

for sheet_name, data in sheet_data.items():
    pdf_buffer = BytesIO()#It creates temporary memory for the PDF. 
    pdf_file_name = f"{data.iloc[0]['Item Cd']}_{data.iloc[0]['Item Description']}.pdf"
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

    print(f"Output PDF file has been generated: {pdf_file_path}")
