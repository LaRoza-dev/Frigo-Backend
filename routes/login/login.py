from fastapi import APIRouter, Body, Header, status
from fastapi import responses
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from fastapi.responses import JSONResponse


from database.user_database import *
from models.user import *
from auth.jwt_handler import signJWT, decodeJWT, token_response

user_router = APIRouter()
user_login_router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


# USER SIGN IN AND SIGN UP
# -------------------------------------------------------------------------------------------------
@user_login_router.post("/register", response_description="User data added into the database")
async def add_user_data(user: UserModel = Body(...)):
    user_exists = await user_collection.find_one({"email":  user.email})
    if(user_exists):
        return "Email already exists"
    user.password = hash_helper.encrypt(user.password)
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User added successfully."})
# if the email is not in a correct format http response code 422 Error: Unprocessable Entity is returned


@user_login_router.post("/login", responses={404: {"model": str}})
async def user_login(user_credentials: UserPassModel = Body(...)):
    user = await user_collection.find_one({"email": user_credentials.email})
    if (user and "password" in user.keys()):
        password = hash_helper.verify(
            user_credentials.password, user["password"])
        if (password):
            return signJWT(user_credentials.email)
    return ErrorResponseModel(404, "Incorrect email or password")
