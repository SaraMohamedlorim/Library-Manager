# borrow.py
"""
Borrowing system: borrow a book, return, and list borrowings per member.
"""
from db import get_conn
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
from books import get_book

def borrow_book(member_id: int, book_id: int, days: int=14) -> bool:
    """Create borrowing; return False if book doesn't exist."""
    if not get_book(book_id):
        return False
    conn = get_conn()
    cur = conn.cursor()
    borrow_date = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    cur.execute("""INSERT INTO borrowings (member_id, book_id, borrow_date, due_date, returned)
                   VALUES (?, ?, ?, ?, 0)""", (member_id, book_id, borrow_date, due_date))
    conn.commit()
    conn.close()
    return True

def return_borrowing(borrowing_id: int) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT returned FROM borrowings WHERE id=?", (borrowing_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False
    if row[0] == 1:
        conn.close()
        return False
    cur.execute("UPDATE borrowings SET returned=1, return_date=? WHERE id=?", (datetime.now().strftime("%Y-%m-%d"), borrowing_id))
    conn.commit()
    conn.close()
    return True

def get_member_borrowings(member_id: int) -> List[Tuple]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""
        SELECT br.id, b.id, b.title, br.borrow_date, br.due_date, br.returned, br.return_date
        FROM borrowings br
        JOIN books b ON br.book_id = b.id
        WHERE br.member_id=?
        ORDER BY br.borrow_date DESC
    """, (member_id,))
    rows = cur.fetchall(); conn.close(); return rows

def get_all_borrowings() -> List[Tuple]:
    """Return all borrowings (useful for admin view)."""
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""
        SELECT br.id, m.full_name, b.title, br.borrow_date, br.due_date, br.returned, br.return_date
        FROM borrowings br
        JOIN members m ON br.member_id = m.id
        JOIN books b ON br.book_id = b.id
        ORDER BY br.borrow_date DESC
    """)
    rows = cur.fetchall(); conn.close(); return rows
