import time
from typing import Dict

import jwt
from decouple import config


def token_response(token: str):
    return {
        "access_token": token
    }

JWT_SECRET = config('secret')
GOOGLE_SECRET = config('GOOGLE_CLIENT_SECRET')
GOOGLE_ID = config('GOOGLE_CLIENT_ID')

def signJWT(user_id: str,is_admin:bool=None) -> Dict[str, str]:
    # Set the expiry time.
    payload = {
        'user_id': user_id,
        'expires': time.time() + 3600,
        'is_admin':is_admin or False
    }
    return token_response(jwt.encode(payload, JWT_SECRET, algorithm="HS256"))


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return {}

def decodeGoogle(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token.encode(), GOOGLE_ID, algorithms=["HS256"])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return {}