# utils.py
"""
Helpers: export CSV/PDF, backup/restore DB, import CSV into members/books
"""
import csv
import shutil
import os
from typing import List, Tuple
from db import DB_PATH
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from books import add_book

def export_csv_file(filepath: str, rows: List[Tuple]):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID","Title","Author","Status","Rating","Notes","Added Date"])
        writer.writerows(rows)

def export_pdf_file(filepath: str, rows: List[Tuple], title: str="Library Report"):
    doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    elements = [Paragraph(title, styles["Title"]), Spacer(1,12)]
    data = [["ID","Title","Author","Status","Rating","Notes","Added Date"]]
    for r in rows:
        notes_text = r[5] or ""
        notes_para = Paragraph(notes_text.replace("\n","<br/>"), styles["BodyText"])
        data.append([str(r[0]), r[1], r[2], r[3], "" if r[4] is None else str(r[4]), notes_para, r[6]])
    colWidths = [30,140,120,60,35,160,60]
    table = Table(data, colWidths=colWidths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#4b8bbe")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.whitesmoke),
        ("ALIGN",(0,0),(-1,-1),"LEFT"),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("GRID",(0,0),(-1,-1),0.25,colors.grey),
        ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),
    ]))
    elements.append(table)
    doc.build(elements)

def backup_db(dst_path: str):
    src = str(DB_PATH)
    if not os.path.exists(src):
        raise FileNotFoundError("Database not found.")
    shutil.copyfile(src, dst_path)

def restore_db(src_path: str):
    if not os.path.exists(src_path):
        raise FileNotFoundError("Source DB not found.")
    dst = str(DB_PATH)
    if os.path.exists(dst):
        shutil.copyfile(dst, dst + ".bak")
    shutil.copyfile(src_path, dst)

def import_books_csv(filepath: str):
    """Import CSV with columns: Title,Author,Status,Rating,Notes,Added Date(optional)"""
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get("Title") or row.get("title") or ""
            author = row.get("Author") or row.get("author") or ""
            status = row.get("Status") or row.get("status") or "available"
            rating = row.get("Rating") or row.get("rating") or None
            notes = row.get("Notes") or row.get("notes") or ""
            # ignore Added Date and use current date for simplicity
            if rating == "":
                rating = None
            else:
                try: rating = int(rating)
                except: rating = None
            add_book(title, author, status, rating, notes)
