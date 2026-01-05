# members.py
"""
Manage library members (patrons).
"""
from db import get_conn
from datetime import datetime
from typing import List, Tuple, Optional

def add_member(full_name: str, email: str="", phone: str=""):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""INSERT INTO members (full_name, email, phone, created_date)
                   VALUES (?, ?, ?, ?)""", (full_name, email, phone, datetime.now().strftime("%Y-%m-%d")))
    conn.commit(); conn.close()

def update_member(member_id: int, full_name: str, email: str, phone: str):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""UPDATE members SET full_name=?, email=?, phone=? WHERE id=?""",
                (full_name, email, phone, member_id))
    conn.commit(); conn.close()

def delete_member(member_id: int):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("DELETE FROM members WHERE id=?", (member_id,))
    conn.commit(); conn.close()

def get_member(member_id: int) -> Optional[Tuple]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT id, full_name, email, phone, created_date FROM members WHERE id=?", (member_id,))
    r = cur.fetchone(); conn.close(); return r

def fetch_all_members() -> List[Tuple]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT id, full_name, email, phone, created_date FROM members ORDER BY full_name COLLATE NOCASE")
    rows = cur.fetchall(); conn.close(); return rows
