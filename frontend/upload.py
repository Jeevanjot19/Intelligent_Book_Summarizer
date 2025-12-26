# frontend/upload.py

import streamlit as st
from pathlib import Path
from utils.session import is_logged_in
from utils.database import get_db_connection
from datetime import datetime
import os


UPLOAD_DIR = Path("data/uploads")
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = [".txt", ".pdf", ".docx"]


def upload_page():
    if not is_logged_in():
        st.error("You must be logged in to upload files.")
        return

    st.title("📄 Upload Book for Summarization")

    st.write("Supported formats: TXT, PDF, DOCX (Max size: 10MB)")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["txt", "pdf", "docx"]
    )

    title = st.text_input("Book Title (optional)")
    author = st.text_input("Author (optional)")
    chapter = st.text_input("Chapter / Section (optional)")

    if uploaded_file is None:
        return

    # ---------- File validation ----------
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error("File size exceeds 10MB limit.")
        return

    file_ext = Path(uploaded_file.name).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        st.error("Unsupported file type.")
        return

    # ---------- Save file ----------
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    safe_filename = f"{timestamp}_{uploaded_file.name}"
    file_path = UPLOAD_DIR / safe_filename

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ---------- Insert into DB ----------
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO books (user_id, title, author, chapter, file_path, uploaded_at, status)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        st.session_state.user_id,
        title or uploaded_file.name,
        author,
        chapter,
        str(file_path),
        datetime.utcnow().isoformat(),
        "uploaded"
    ))

    conn.commit()
    conn.close()

    st.success("File uploaded successfully!")
