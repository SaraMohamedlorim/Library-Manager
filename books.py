# books.py
"""
CRUD and search for books (catalog).
Books are global (not tied to an app user).
"""
from db import get_conn
from datetime import datetime
from typing import List, Tuple, Optional

def add_book(title: str, author: str, status: str="available", rating: Optional[int]=None, notes: str=""):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""INSERT INTO books (title, author, status, rating, notes, added_date)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (title, author, status, rating, notes, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def update_book(book_id: int, title: str, author: str, status: str, rating: Optional[int], notes: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""UPDATE books SET title=?, author=?, status=?, rating=?, notes=? WHERE id=?""",
                (title, author, status, rating, notes, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

def get_book(book_id: int) -> Optional[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, author, status, rating, notes, added_date FROM books WHERE id=?", (book_id,))
    r = cur.fetchone()
    conn.close()
    return r

def fetch_all_books(order_by: str="added_date", filters: dict=None, date_from: str=None, date_to: str=None) -> List[Tuple]:
    whitelist = ("added_date","title","author","status","rating")
    order_col = order_by.split()[0] if order_by else "added_date"
    if order_col not in whitelist:
        order_col = "added_date"
    conn = get_conn()
    cur = conn.cursor()
    query = "SELECT id, title, author, status, rating, notes, added_date FROM books WHERE 1=1"
    params = []
    if filters:
        if filters.get("status") and filters["status"] != "All":
            query += " AND status=?"
            params.append(filters["status"])
        if filters.get("rating_min") is not None:
            query += " AND rating>=?"
            params.append(filters["rating_min"])
        if filters.get("rating_max") is not None:
            query += " AND rating<=?"
            params.append(filters["rating_max"])
    if date_from:
        query += " AND date(added_date)>=date(?)"
        params.append(date_from)
    if date_to:
        query += " AND date(added_date)<=date(?)"
        params.append(date_to)
    query += f" ORDER BY {order_by} COLLATE NOCASE"
    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    conn.close()
    return rows

def search_books(keyword: str, filter_status: str="All", order_by: str="added_date") -> List[Tuple]:
    kw = f"%{keyword}%"
    conn = get_conn()
    cur = conn.cursor()
    query = """SELECT id, title, author, status, rating, notes, added_date FROM books
               WHERE (title LIKE ? OR author LIKE ? OR notes LIKE ?)"""
    params = [kw, kw, kw]
    if filter_status and filter_status != "All":
        query += " AND status=?"
        params.append(filter_status)
    whitelist = ("added_date","title","author","status","rating")
    order_col = order_by.split()[0] if order_by else "added_date"
    if order_col not in whitelist:
        order_col = "added_date"
    query += f" ORDER BY {order_by} COLLATE NOCASE"
    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    conn.close()
    return rows
