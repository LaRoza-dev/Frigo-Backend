from fastapi import APIRouter, Body,Header, Cookie
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError


from database.user_database import *
from models.user import *
from auth.jwt_handler import signJWT, decodeJWT, token_response

user_router = APIRouter()
user_login_router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])
#-------------------------------------------------------------------------------------------------
config = Config('.env')
oauth = OAuth(config)
google_route = APIRouter()
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

# SIGN IN AND SIGN UP WITH GOOGLE
#-------------------------------------------------------------------------------------------------
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    })


@google_route.post('/')
async def homepage(token:str=Body(...)):
    user =  decodeJWT(token) 
    if user:
        db_user = await user_collection.find_one({"email": user["email"]})
        if (db_user):
            return token_response(token)
        sign_user = {"fullname":user["fullname"],"email":user["email"],"is_admin":False}
        sign_user = jsonable_encoder(sign_user)
        new_user = await add_user(sign_user)
        new_user.update(token_response(token))
        return token_response(token)
    return ErrorResponseModel("An error occured.", 404, "Wrong format token")
    
    

# USER SIGN IN AND SIGN UP
#-------------------------------------------------------------------------------------------------
@user_login_router.post("/register", response_description="User data added into the database")
async def add_user_data(user: UserModel = Body(...)):
    user_exists = await user_collection.find_one({"email":  user.email})
    if(user_exists):
        return "Email already exists"
    user.password = hash_helper.encrypt(user.password)
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@user_login_router.post("/login")
async def user_login(user_credentials: UserPassModel = Body(...)):
    user = await user_collection.find_one({"email": user_credentials.email})
    print(user)
    if (user and "password" in user.keys()):
        password = hash_helper.verify(
            user_credentials.password, user["password"])
        if (password):
            return signJWT(user_credentials.email)

        return ErrorResponseModel("An error occured.", 404, "Incorrect email or password")

    return ErrorResponseModel("An error occured.", 404, "Incorrect email or password")


# USER CRUD OPERATIONS
#-------------------------------------------------------------------------------------------------

@user_router.get("/", response_description="Users retrieved")
async def get_users(authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    if is_admin:
        users = await retrieve_users()
        return ResponseModel(users, "Users data retrieved successfully") \
            if len(users) > 0 \
            else ResponseModel(
            users, "Empty list returned")
    return "Permission denied"


@user_router.get("/{id}", response_description="User data retrieved")
async def get_user_data(id: str, authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    if is_admin:
        user = await retrieve_user(id)
        return ResponseModel(user, "User data retrieved successfully") \
            if user \
            else ErrorResponseModel("An error occured.", 404, "User doesn't exist.")
    return "Permission denied"


@user_router.put("{id}")
async def update_user(id: str, req: UpdateUserModel = Body(...), authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    if is_admin:
        updated_user = await update_user_data_admin(id, req.dict())
        return ResponseModel("User with ID: {} name update is successful".format(id),
                            "User name updated successfully") \
            if updated_user \
            else ErrorResponseModel("An error occurred", 404, "There was an error updating the user.".format(id))
    else:
        user_id = (await retrieve_user(email=token_data['email']))['id']
        updated_user = await update_user_data(id, req.dict(),user_id)
        return ResponseModel("User with ID: {} name update is successful".format(id),
                            "User name updated successfully") \
            if updated_user \
            else ErrorResponseModel("An error occurred", 404, "There was an error updating the user.".format(id))


@user_router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(id: str, authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    if is_admin:
        deleted_user = await delete_user_admin(id)
        return ResponseModel("User with ID: {} removed".format(id), "User deleted successfully") \
            if deleted_user \
            else ErrorResponseModel("An error occured", 404, "User with id {0} doesn't exist".format(id))
    else:
        user_id = (await retrieve_user(email=token_data['email']))['id']
        deleted_user = await delete_user(id,user_id)
        return ResponseModel("User with ID: {} removed".format(id), "User deleted successfully") \
            if deleted_user \
            else ErrorResponseModel("An error occured", 404, "User with id {0} doesn't exist".format(id))
    
