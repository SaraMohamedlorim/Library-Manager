# auth.py
"""
# User authentication helpers (simple SHA-256 hashing).
Note: For production use a stronger password hashing (bcrypt/argon2).
"""
from db import get_conn
# import hashlib
from typing import Optional
import bcrypt

def hash_password(password: str) -> str:
    if password is None:
        password = ""
    # return hashlib.sha256(password.encode("utf-8")).hexdigest()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(plain_password: str, hashed_password: str)-> bool:
    """Check if plain password matches the hashed password."""
    if not plain_password:
        plain_password = ""
    if not hash_password:
        return False
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False
    

def create_user(username: str, password: Optional[str] = None) -> bool:
    """Create a new application user. Returns False if username exists."""
    conn = get_conn()
    cur = conn.cursor()
    try:
        hashed = hash_password(password or "")
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hashed))
        conn.commit()
    except Exception:
        conn.close()
        return False
    conn.close()
    return True

def authenticate_user(username: str, password: Optional[str]) -> Optional[int]:
    """Return user id if credentials match, else None."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    uid, stored_hash = row
    if check_password(password or "", stored_hash):
        return uid
    else:
        return None
   

def change_user_password(username: str, new_password: str) -> bool:
    """Change password for an existing username."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=?", (username,))
    if not cur.fetchone():
        conn.close()
        return False
    
    hashed = hash_password(new_password or "")
    cur.execute("UPDATE users SET password_hash=? WHERE username=?", (hashed, username))
    conn.commit()
    conn.close()
    return True

def change_username(old_username: str, new_username: str) -> bool:
    """Change username if new_username not already taken."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=?", (old_username,))
    if not cur.fetchone():
        conn.close()
        return False
    try:
        cur.execute("UPDATE users SET username=? WHERE username=?", (new_username, old_username))
        conn.commit()
    except Exception:
        conn.close()
        return False
    conn.close()
    return True

def get_all_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows
