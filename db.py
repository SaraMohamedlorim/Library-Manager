# db.py
"""
Database initialization and connection helper.
Creates tables:
- users (app accounts)
- members (library patrons)
- books (catalog)
- borrowings (who borrowed which book)
"""
from pathlib import Path
import sqlite3
# السطر ده بيخلي DB_PATH = المجلد اللي فيه الملف الحالي.
DB_PATH = Path(__file__).parent / "library_manager.db"

def get_conn():
    """Return a new sqlite3 connection (caller must close)."""
    return sqlite3.connect(str(DB_PATH))

def init_db():
    """Create database tables if they don't exist."""
    conn = get_conn()
    cur = conn.cursor()

    # users: application user accounts 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT
        )
    """)

    # members: library members / borrowers
    cur.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            created_date TEXT NOT NULL
        )
    """)

    # books: library catalog
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT NOT NULL,
            rating INTEGER,
            notes TEXT,
            added_date TEXT NOT NULL
        )
    """)

    # borrowings: record of borrow/return
    cur.execute("""
        CREATE TABLE IF NOT EXISTS borrowings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            borrow_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            returned INTEGER DEFAULT 0,
            return_date TEXT,
            FOREIGN KEY(member_id) REFERENCES members(id),
            FOREIGN KEY(book_id) REFERENCES books(id)
        )
    """)

    conn.commit()
    conn.close()
