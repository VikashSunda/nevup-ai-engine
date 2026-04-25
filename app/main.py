from fastapi import FastAPI, Depends, Body
from fastapi.responses import StreamingResponse
from .database import init_db
from .auth import verify_token
from .profiler import generate_profile
from .memory_engine import store_memory, fetch_context, get_raw_session
from .coaching import stream_coaching_message
from .audit import audit_response
from .utils import get_trader

init_db()
app = FastAPI(title="NevUp AI Trading Coach")

@app.get("/")
def root():
    return {"message": "NevUp AI Trading Coach Running"}

@app.get("/profile/{user_id}")
def profile(user_id:str, token=Depends(verify_token)):
    if token["sub"] != user_id:
        return {"error":"FORBIDDEN"}
    return generate_profile(user_id)

@app.put("/memory/{user_id}/sessions/{session_id}")
def put_memory(user_id:str, session_id:str, body:dict=Body(...), token=Depends(verify_token)):
    if token["sub"] != user_id:
        return {"error":"FORBIDDEN"}

    trader = get_trader(user_id)
    raw = None
    for s in trader["sessions"]:
        if s["sessionId"] == session_id:
            raw = s

    return store_memory(user_id, session_id, body["summary"], body["metrics"], body["tags"], raw)

@app.get("/memory/{user_id}/context")
def context(user_id:str, relevantTo:str, token=Depends(verify_token)):
    if token["sub"] != user_id:
        return {"error":"FORBIDDEN"}
    return fetch_context(user_id, relevantTo)

@app.get("/memory/{user_id}/sessions/{session_id}")
def raw_session(user_id:str, session_id:str, token=Depends(verify_token)):
    if token["sub"] != user_id:
        return {"error":"FORBIDDEN"}
    return get_raw_session(user_id, session_id)

@app.post("/session/events")
def session_events(body:dict=Body(...), token=Depends(verify_token)):
    user_id = body["userId"]
    if token["sub"] != user_id:
        return {"error":"FORBIDDEN"}
    return StreamingResponse(stream_coaching_message(user_id), media_type="text/event-stream")

@app.post("/audit")
def audit(body:dict=Body(...), token=Depends(verify_token)):
    user_id = body["userId"]
    if token["sub"] != user_id:
        return {"error":"FORBIDDEN"}
    return audit_response(user_id, body["coachingText"])