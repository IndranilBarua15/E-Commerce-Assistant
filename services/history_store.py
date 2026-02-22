import sqlite3
import os
from datetime import datetime

DB = "storage/shopsmart.db"

# Ensure storage folder exists
os.makedirs("storage", exist_ok=True)


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            query TEXT,
            price REAL,
            source TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_search(user, query, price, source):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO history (user, query, price, source, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user,
            query,
            price,
            source,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
    )
    conn.commit()
    conn.close()


def get_history(user, limit=10):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT query
        FROM history
        WHERE user=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user, limit)
    )
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]


def clear_history(user):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM history WHERE user=?",
        (user,)
    )
    conn.commit()
    conn.close()
