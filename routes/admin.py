from fastapi import Body, APIRouter,Header,Depends
from typing import Optional
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext

from database.user_database import user_collection
from auth.jwt_handler import signJWT,decodeJWT
from database.user_database import add_admin,retrieve_user
from models.user import UserModel, UserPassModel

from auth.jwt_bearer import JWTBearer
token_listener = JWTBearer()

admin_router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

@admin_router.post("/login")
async def admin_login(admin_credentials: UserPassModel = Body(...)):
    admin_user = await user_collection.find_one({"email": admin_credentials.email})
    if (admin_user):
        password = hash_helper.verify(
            admin_credentials.password, admin_user["password"])
        if (password and admin_user['is_admin']):
            return signJWT(admin_credentials.email,admin_user['is_admin'])

        return "Incorrect email or password"

    return "Incorrect email or password"

@admin_router.post("/regsiter", dependencies=[Depends(token_listener)])
async def admin_signup(admin: UserModel = Body(...),authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    if is_admin:
        admin_exists = await user_collection.find_one({"email":  admin.email})
    
        if(admin_exists):
            return "Email already exists"
        
        
        admin.password = hash_helper.encrypt(admin.password)
        new_admin = await add_admin(jsonable_encoder(admin))
        return new_admin
    return 'Permission denied'