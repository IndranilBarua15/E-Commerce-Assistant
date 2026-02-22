import streamlit as st
import bcrypt
import sqlite3
import os

DB = "storage/shopsmart.db"

def init_users():
    os.makedirs("storage", exist_ok=True)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password BLOB
        )
    """)
    conn.commit()
    conn.close()

def login():
    if "user" not in st.session_state:
        st.session_state.user = None

    st.sidebar.subheader("🔐 Login / Register")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Register"):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed)
            )
            conn.commit()
            st.sidebar.success("Registered successfully")
        except:
            st.sidebar.error("User already exists")
        conn.close()

    if st.sidebar.button("Login"):
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute(
            "SELECT password FROM users WHERE username=?",
            (username,)
        )
        row = cur.fetchone()
        conn.close()

        if row and bcrypt.checkpw(password.encode(), row[0]):
            st.session_state.user = username
            st.sidebar.success(f"Welcome {username}")
            st.rerun()
        else:
            st.sidebar.error("Invalid credentials")

    return st.session_state.user
