import sqlite3

DB_NAME = "nevup_memory.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS memory_sessions (
        session_id TEXT PRIMARY KEY,
        user_id TEXT,
        summary TEXT,
        metrics TEXT,
        tags TEXT,
        raw_record TEXT
    )
    """)

    conn.commit()
    conn.close()