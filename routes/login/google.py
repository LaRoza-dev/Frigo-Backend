from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from fastapi.responses import JSONResponse


from database.user_database import *
from models.user import *
from auth.jwt_handler import decodeJWT, token_response

user_router = APIRouter()
user_login_router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


# SIGN IN AND SIGN UP WITH GOOGLE
# -------------------------------------------------------------------------------------------------
google_route = APIRouter()


@google_route.post('/', responses={404: {"model": str}})
async def homepage(token: str = Body(...)):
    user = decodeJWT(token)
    if user:
        db_user = await user_collection.find_one({"email": user["email"]})
        if (db_user):
            return token_response(token)
        sign_user = {"fullname": user["fullname"],
                     "email": user["email"], "is_admin": False}
        sign_user = jsonable_encoder(sign_user)
        new_user = await add_user(sign_user)
        new_user.update(token_response(token))
        return token_response(token)
    return ErrorResponseModel(status.HTTP_404_NOT_FOUND, "Wrong format token")
