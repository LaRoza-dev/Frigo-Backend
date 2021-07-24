import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config
# from main import stage
from .database_helper import user_helper


stage = config('stage')
if stage == "development":
    MONGO_DETAILS = config('MONGO_DETAILS_PROD')
else:
    MONGO_DETAILS = config('MONGO_DETAILS_DEV')
# else:
    # print("WRONG MONGO ENV")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS, tls=True, tlsAllowInvalidCertificates=True)

database = client.users

user_collection = database.get_collection('users_collection')


async def add_admin(admin_data: dict) -> dict:
    admin_data['is_admin']=True
    admin = await user_collection.insert_one(admin_data)
    new_admin = await user_collection.find_one({"_id": admin.inserted_id})
    return user_helper(new_admin)

async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def retrieve_user(id:str=None,email:str=None) -> dict:
    if email:
        user = await user_collection.find_one({"email": email})    
    else:
        user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True


async def update_user_data(id: str, data: dict):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        user_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True