from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from fastapi.security import HTTPBasicCredentials

from database.user_database import *
from models.user import *
from auth.jwt_handler import signJWT

user_router = APIRouter()
user_login_router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@user_login_router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserModel = Body(...)):
    user_exists = await user_collection.find_one({"email":  user.email}, {"_id": 0})
    if(user_exists):
        return "Email already exists"
    user.password = hash_helper.encrypt(user.password)
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@user_login_router.post("/login")
async def user_login(user_credentials: HTTPBasicCredentials = Body(...)):
    # NEW CODE
    user = await user_collection.find_one({"email": user_credentials.username}, {"_id": 0})
    if (user):
        password = hash_helper.verify(
            user_credentials.password, user["password"])
        if (password):
            return signJWT(user_credentials.username)

        return "Incorrect email or password"

    return "Incorrect email or password"


@user_router.get("/", response_description="Users retrieved")
async def get_users():
    users = await retrieve_users()
    return ResponseModel(users, "Users data retrieved successfully") \
        if len(users) > 0 \
        else ResponseModel(
        users, "Empty list returned")


@user_router.get("/{id}", response_description="User data retrieved")
async def get_user_data(id):
    user = await retrieve_user(id)
    return ResponseModel(user, "User data retrieved successfully") \
        if user \
        else ErrorResponseModel("An error occured.", 404, "User doesn't exist.")


@user_router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    return ResponseModel("User with ID: {} removed".format(id), "User deleted successfully") \
        if deleted_user \
        else ErrorResponseModel("An error occured", 404, "User with id {0} doesn't exist".format(id))


@user_router.put("{id}")
async def update_user(id: str, req: UpdateUserModel = Body(...)):
    updated_user = await update_user_data(id, req.dict())
    return ResponseModel("User with ID: {} name update is successful".format(id),
                         "User name updated successfully") \
        if updated_user \
        else ErrorResponseModel("An error occurred", 404, "There was an error updating the user.".format(id))
