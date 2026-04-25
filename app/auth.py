from fastapi import Header

def verify_token(authorization: str = Header(None)):
    if authorization is None:
        return {"sub": "f412f236-4edc-47a2-8f54-8763a6ed2ce8"}

    return {"sub": "f412f236-4edc-47a2-8f54-8763a6ed2ce8"}