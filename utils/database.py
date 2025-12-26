import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "app.db"

def get_db_connection():
    """
    Creates and returns a SQLite database connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    """
    Creates all required tables if they do not exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON;")
    # -----------------------------
    # Users table
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TEXT NOT NULL
    );
    """)

    # -----------------------------
    # Books table
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        author TEXT,
        chapter TEXT,
        file_path TEXT NOT NULL,
        raw_text TEXT,
        status TEXT DEFAULT 'uploaded',
        uploaded_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    );
    """)

    # -----------------------------
    # Summaries table
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS summaries (
        summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        summary_text TEXT NOT NULL,
        summary_length TEXT NOT NULL,
        summary_style TEXT NOT NULL,
        processing_time REAL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    );
    """)

    # -----------------------------
    # Chunk summaries table
    # -----------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunk_summaries (
        chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
        summary_id INTEGER NOT NULL,
        chunk_index INTEGER NOT NULL,
        chunk_text TEXT NOT NULL,
        FOREIGN KEY (summary_id) REFERENCES summaries(summary_id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

    # -----------------------------
    # User-related operations
    # -----------------------------
def create_user(name, email, password_hash):
        """
        Inserts a new user into the database.
        Returns True on success, False if email already exists.
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO users (name, email, password_hash, created_at)
            VALUES (?, ?, ?, ?);
            """, (name, email, password_hash, datetime.utcnow().isoformat()))

            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Email already exists
            return False

        finally:
            conn.close()
    
def get_user_by_email(email):
        """
        Fetches a user by email.
        Returns user row or None.
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM users WHERE email = ?;
        """, (email,))

        user = cursor.fetchone()
        conn.close()
        return user

def store_chunks(summary_id: int, chunks: list[str]):
    """
    Store text chunks in the database linked to a summary.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    for index, chunk in enumerate(chunks):
        cursor.execute("""
        INSERT INTO chunk_summaries (summary_id, chunk_index, chunk_text)
        VALUES (?, ?, ?);
        """, (
            summary_id,
            index,
            chunk
        ))

    conn.commit()
    conn.close()
