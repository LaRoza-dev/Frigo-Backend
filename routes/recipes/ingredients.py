from fastapi import APIRouter, Body,Header, Cookie
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError


from database.user_database import *
from models.user import *
from auth.jwt_handler import signJWT, decodeJWT

user_fridge = APIRouter()
user_ingredients = APIRouter()


# UPDATE USER'S FRIDGE
@user_fridge.post("/{user_id}")
async def add_user_fridge(user_id: str, req:list=Body(...), authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    # if is_admin:  
    updated_user = await update_user_fridge(user_id, req)
    return ResponseModel("User with ID: {} name update is successful".format(user_id),
                        "User name updated successfully") \
        if updated_user \
        else ErrorResponseModel(404, "There was an error updating the user.".format(user_id))
    # return "Permission denied"


# UPDATE USER'S CUSTOM INGREDIENTS
@user_ingredients.post("/{user_id}")
async def add_user_custom_ingredients(user_id: str, req:list=Body(...), authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    # if is_admin:  
    updated_user = await update_user_custom_ingredient(user_id, req)
    return ResponseModel("User with ID: {} name update is successful".format(user_id),
                        "User name updated successfully") \
        if updated_user \
        else ErrorResponseModel(404, "There was an error updating the user.".format(user_id))
    # return "Permission denied"


