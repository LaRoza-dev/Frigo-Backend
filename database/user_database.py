import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config
from .database_helper import user_helper


stage = config('stage')
if stage == "development":
    MONGO_DETAILS = config('MONGO_DETAILS_DEV')
elif stage == "production":
    MONGO_DETAILS = config('MONGO_DETAILS_PROD')
else:
    print("WRONG MONGO ENV")

client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_DETAILS, tls=True, tlsAllowInvalidCertificates=True)

database = client.users

user_collection = database.get_collection('users_collection')


# ADD -----------------------------------------------
# Add admin user
async def add_admin(admin_data: dict) -> dict:
    admin_data['is_admin'] = True
    admin = await user_collection.insert_one(admin_data)
    new_admin = await user_collection.find_one({"_id": admin.inserted_id})
    return user_helper(new_admin)


# Add user
async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


# Get -----------------------------------------------
# Get all users
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Retrieve user with matching is
async def retrieve_user(id: str = None, email: str = None) -> dict:
    if email:
        user = await user_collection.find_one({"email": email})
    else:
        user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


# Update -----------------------------------------------
# Update custom ingrediens of user with matching id
async def update_user_wishlist(id: str, data: list):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    for k, v in list(data.items()):
        if v is None:
            del data[k]
    if user:
        data = {"wishlist": data}
        user_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True


# Update fridge items of user with matchind id
async def update_user_fridge(id: str, data: list):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        data = {"fridge": data}
        for k, v in list(data.items()):
            if v is None:
                del data[k]
        user_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True

# Udate User data of user with matching id
async def update_user_data(id: str, data: dict):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    for k, v in list(data.items()):
        if v is None:
            del data[k]
    if user:
        user_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True


# ADMIN Udates User data of user with matching id
async def update_user_data_admin(id: str, data: dict):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    for k, v in list(data.items()):
        if v is None:
            del data[k]
    if user:
        user_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True


# DELETE -----------------------------------------------
# Delete user
async def delete_user(id: str, user_id: str):
    user = await user_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True

# ADMIN Deletes user


async def delete_user_admin(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True
