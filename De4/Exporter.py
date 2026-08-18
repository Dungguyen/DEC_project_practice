import csv
import os
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from Cfg import CSV_FIELDS, OUTPUT_DIR

HEADER_FILL  = PatternFill("solid", fgColor="EE4D2D")
ALT_FILL     = PatternFill("solid", fgColor="FFF3F0")
WHITE_FILL   = PatternFill("solid", fgColor="FFFFFF")
_thin        = Side(style="thin", color="DDDDDD")
BORDER       = Border(left=_thin, right=_thin, top=_thin, bottom=_thin)
 
COL_HEADERS = ["Product Name", "Product URL", "Rating ⭐", "Price (VND)", "Revenue (VND)"]
COL_WIDTHS  = [45, 55, 12, 18, 22]

def _slug(name:str) -> str:
    return re.sub(r"[^\w]+", "-", name).strip("-").lower()

def _write_excel(rows: list[dict], path : str) -> None:
    """Write rows to an Excel file."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Products"

    # Header row
    for col, (h, w) in enumerate(zip(COL_HEADERS, COL_WIDTHS), start=1):
        c = ws.cell(row=1, column=col, value=h)
        c.font      = Font(name="Arial", bold=True, color="FFFFFF", size=11)
        c.fill      = HEADER_FILL
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border    = BORDER
        ws.column_dimensions[get_column_letter(col)].width = w
    ws.row_dimensions[1].height = 28
    
    # Write headers
    for i, row in enumerate(rows, start=2):
        fill = ALT_FILL if i % 2 == 0 else WHITE_FILL
 
        # product_name
        c = ws.cell(row=i, column=1, value=row["product_name"])
        c.font = Font(name="Arial", size=10)
        c.fill = fill; c.border = BORDER
        c.alignment = Alignment(vertical="center", wrap_text=True)
 
        # product_url
        c = ws.cell(row=i, column=2, value=row["product_url"])
        c.font = Font(name="Arial", size=10, color="0563C1", underline="single")
        c.hyperlink = row["product_url"]
        c.fill = fill; c.border = BORDER
        c.alignment = Alignment(vertical="center")
 
        # rating
        c = ws.cell(row=i, column=3, value=row["product_rating"])
        c.font = Font(name="Arial", size=10)
        c.fill = fill; c.border = BORDER
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = "0.0"
 
        # price
        c = ws.cell(row=i, column=4, value=row["product_price"])
        c.font = Font(name="Arial", size=10)
        c.fill = fill; c.border = BORDER
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '#,##0 "₫"'
 
        # revenue
        c = ws.cell(row=i, column=5, value=row["product_revenue"])
        c.font = Font(name="Arial", size=10, bold=True, color="C00000")
        c.fill = fill; c.border = BORDER
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '#,##0 "₫"'
 
        ws.row_dimensions[i].height = 20
 
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:E{len(rows) + 1}"
    wb.save(path)

def export_category(cat_name: str, rows: list[dict]) -> None:
    """Export rows to CSV and Excel files."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    slug = _slug(cat_name)
    csv_path = os.path.join(OUTPUT_DIR, f"{slug}.csv")
    # Write CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    # Write Excel
    xlsx_path = os.path.join(OUTPUT_DIR, f"{slug}.xlsx")
    _write_excel(rows, xlsx_path)

    print(f"  💾 {cat_name}: {csv_path} | {xlsx_path}")
