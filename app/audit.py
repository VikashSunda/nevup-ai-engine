import re
from .database import get_connection

def audit_response(user_id, coaching_text):
    ids = re.findall(r'[a-f0-9\\-]{36}', coaching_text)

    conn = get_connection()
    cur = conn.cursor()

    results = []
    for sid in ids:
        cur.execute("SELECT session_id FROM memory_sessions WHERE session_id=? AND user_id=?", (sid, user_id))
        found = cur.fetchone()
        results.append({"sessionId": sid, "status": "found" if found else "not-found"})

    conn.close()
    return {"audit": results}