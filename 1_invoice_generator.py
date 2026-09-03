import pandas as pd
import os

cd_path = os.getcwd()
input_file_path = os.path.join(cd_path, "Book1.xlsx")
output_file_path = os.path.join(cd_path, "output_invoice.xlsx")

df = pd.read_excel(input_file_path)
grouped = df.groupby('Item Cd')


with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
    for invoice_no, group in grouped:
        cleaned_invoice_no = ''.join(c for c in str(invoice_no) if c.isalnum() or c in ['-', '_', ' '])
        if cleaned_invoice_no and cleaned_invoice_no not in writer.sheets:
            group.to_excel(writer, sheet_name=f'Part_no_{cleaned_invoice_no}', index=False)

print(f"Output Excel file has been generated: {output_file_path}")
