from fastapi import APIRouter, Body, Header
from passlib.context import CryptContext
from database.user_database import *
from models.user import *
from auth.jwt_handler import decodeJWT

user_router = APIRouter()
user_login_router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


# USER CRUD OPERATIONS
# -------------------------------------------------------------------------------------------------

@user_router.get("/", response_description="Users retrieved")
async def get_users(authorization: Optional[str] = Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    if is_admin:
        users = await retrieve_users()
        return ResponseModel(users, "Users data retrieved successfully") \
            if len(users) > 0 \
            else ResponseModel(
            users, "Empty list returned")
    return ErrorResponseModel(403, "Permission denied")
    
@user_router.get("/me", response_description="User data retrieved")
async def get_user_data(authorization: Optional[str] = Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    email = token_data['email']
    user = await retrieve_user(email=email)
    return ResponseModel(user, "User data retrieved successfully") \
        if user \
        else ErrorResponseModel(404, "User doesn't exist.")
    

@user_router.get("/{id}", response_description="User data retrieved")
async def get_user_data(id: str, authorization: Optional[str] = Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    if is_admin:
        user = await retrieve_user(id)
        return ResponseModel(user, "User data retrieved successfully") \
            if user \
            else ErrorResponseModel(404, "User doesn't exist.")
    return ErrorResponseModel(403, "Permission denied")



@user_router.put("/{id}")
async def update_user(id: str, req: UpdateUserModel = Body(...), authorization: Optional[str] = Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    if is_admin:
        updated_user = await update_user_data_admin(id, req.dict())
        return ResponseModel("User with ID: {} name update is successful".format(id),
                             "User name updated successfully") \
            if updated_user \
            else ErrorResponseModel(400, "There was an error updating the user.".format(id))
    else:
        try:
            user_id = (await retrieve_user(email=token_data['email']))['id']
        except:
            user_id = None
        if user_id:
            updated_user = await update_user_data(user_id, req.dict())
            if updated_user:
                return ResponseModel("User with ID: {} name update is successful".format(id),
                                     "User name updated successfully")
        return ErrorResponseModel(400, "There was an error updating the user.".format(id))


@user_router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(id: str, authorization: Optional[str] = Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    if is_admin:
        deleted_user = await delete_user_admin(id)
        return ResponseModel("User with ID: {} removed".format(id), "User deleted successfully") \
            if deleted_user \
            else ErrorResponseModel(404, "User with id {0} doesn't exist".format(id))
    else:
        user_id = (await retrieve_user(email=token_data['email']))['id']
        deleted_user = await delete_user(id, user_id)
        return ResponseModel("User with ID: {} removed".format(id), "User deleted successfully") \
            if deleted_user \
            else ErrorResponseModel(404, "User with id {0} doesn't exist".format(id))
