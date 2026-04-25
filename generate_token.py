from jose import jwt
import time

SECRET = "97791d4db2aa5f689c3cc39356ce35762f0a73aa70923039d8ef72a2840a1b02"
ALGORITHM = "HS256"

payload = {
    "sub": "f412f236-4edc-47a2-8f54-8763a6ed2ce8",
    "iat": int(time.time()),
    "exp": int(time.time()) + 86400,
    "role": "trader",
    "name": "Alex Mercer"
}

token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
print(token)