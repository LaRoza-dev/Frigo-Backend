import time
from typing import Dict

import jwt
from google.auth import jwt as gjwt
from decouple import config

from database.validate_google_token import validate_security_token


def token_response(token: str):
    return {
        "access_token": token
    }

JWT_SECRET = config('secret')
client_ids = [config('CLIENT_ANDROID'), config('CLIENT_IOS'),config('CLIENT_WEB')]

def signJWT(email: str,is_admin:bool=False) -> Dict[str, str]:
    # Set the expiry time.
    payload = {
        'email': email,
        'expires': time.time() + 3600,
        'is_admin':is_admin 
    }
    return token_response(jwt.encode(payload, JWT_SECRET, algorithm="HS256"))


def decodeJWT(token: str) -> dict:
    try:
        dheader = gjwt.decode_header(token)
        if (dheader['alg']=='RS256' and dheader['kid']):
            dtoken = validate_security_token(token,client_ids)
            decoded_token = {'email': dtoken['email'],'fullname':dtoken['name'],
                            'expires': time.time() + 3600,
                            'is_admin':False}
            return decoded_token if decoded_token['expires'] >= time.time() else None

        elif(dheader['alg']=='HS256'):
            decoded_token = jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])
            return decoded_token if decoded_token['expires'] >= time.time() else None
        else:
            return{}
    except:
        return {}
