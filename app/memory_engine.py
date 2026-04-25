import json
from .database import get_connection

def store_memory(user_id, session_id, summary, metrics, tags, raw_record):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO memory_sessions (session_id, user_id, summary, metrics, tags, raw_record)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        session_id,
        user_id,
        summary,
        json.dumps(metrics),
        json.dumps(tags),
        json.dumps(raw_record)
    ))

    conn.commit()
    conn.close()

    return {"status": "stored", "sessionId": session_id}

def fetch_context(user_id, signal):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM memory_sessions WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()

    sessions = []
    pattern_ids = []

    for r in rows:
        tags = json.loads(r["tags"])
        if signal in tags or len(tags) > 0:
            sessions.append({"sessionId": r["session_id"], "summary": r["summary"]})
            pattern_ids.extend(tags)

    return {"sessions": sessions, "patternIds": list(set(pattern_ids))}

def get_raw_session(user_id, session_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT raw_record FROM memory_sessions WHERE user_id=? AND session_id=?", (user_id, session_id))
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return json.loads(row["raw_record"])