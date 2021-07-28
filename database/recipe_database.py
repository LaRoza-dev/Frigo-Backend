import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config
from .database_helper import recipe_helper
import re

stage = config('stage')
if stage == "development":
    MONGO_DETAILS = config('MONGO_DETAILS_DEV')
elif stage == "production":
    MONGO_DETAILS = config('MONGO_DETAILS_PROD')
else:
    print("WRONG MONGO ENV")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS, tls=True, tlsAllowInvalidCertificates=True)

database = client.recipes

recipe_collection = database.get_collection("recipes_collection")


# Retrieve all recipes present in the database
async def retrieve_recipes(user_id,is_admin=None):
    recipes = []
    if is_admin:
        async for recipe in recipe_collection.find({}):
            recipes.append(recipe_helper(recipe))
    else:
        async for recipe in recipe_collection.find({"$or":[{ "user_id":user_id},{"user_id":"1"}]}):
            recipes.append(recipe_helper(recipe))
    return recipes

# Retrieve all recipes present in the database which has ingredient list 
async def retrieve_recipes_by_ingredients(user_id,is_admin=None,query:list=None):
    recipes = []
    if is_admin:
        query=list(map(lambda recipe: re.compile(f"^.*{recipe}.*$",re.IGNORECASE),query))
        async for recipe in recipe_collection.find({"ingredients":{"$in":query}}):
            recipes.append(recipe_helper(recipe))
    else:
        async for recipe in recipe_collection.find({
            "$and":[
                {"$or":[
                        {"user_id":user_id},
                        {"user_id":"1"}
                        ]
                }
                ,{"ingredients":{"$in":query}}
                ]
            }):
            recipes.append(recipe_helper(recipe))
    return recipes

# Add a new recipe into to the database
async def add_recipe(recipe_data: dict) -> dict:
    recipe = await recipe_collection.insert_one(recipe_data)
    new_recipe = await recipe_collection.find_one({"_id": recipe.inserted_id})
    return recipe_helper(new_recipe)


# Retrieve a recipe with a matching ID
async def retrieve_recipe(id: str,user_id: str) -> dict:
    recipe = await recipe_collection.find_one({"$or":[{"_id": ObjectId(id), "user_id":user_id},{"_id": ObjectId(id),"user_id":"1"}]})
    if recipe:
        return recipe_helper(recipe)

async def retrieve_recipe_name(name: str,user_id: str) -> dict:
    recipe = await recipe_collection.find_one({"$or":[{"name": {'$regex': f".*{name}.*","$options":"i"}, "user_id":user_id},{"name":{'$regex': f".*{name}.*","$options":"i"},"user_id":"1"}]})
    if recipe:
        return recipe_helper(recipe)

# Update a recipe with a matching ID
async def update_recipe(id: str, data: dict,user_id: str):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    recipe = await recipe_collection.find_one({"_id": ObjectId(id),"user_id":user_id})
    if recipe:
        updated_recipe = await recipe_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_recipe:
            return True
        return False


async def update_recipe_admin(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    recipe = await recipe_collection.find_one({"_id": ObjectId(id)})
    if recipe:
        updated_recipe = await recipe_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_recipe:
            return True
        return False


# Delete a recipe from the database
async def delete_recipe(id: str,user_id: str):
    recipe = await recipe_collection.find_one({"_id": ObjectId(id),"user_id":user_id})
    if recipe:
        await recipe_collection.delete_one({"_id": ObjectId(id)})
        return True

async def delete_recipe_admin(id: str):
    return await recipe_collection.delete_one({"_id": ObjectId(id)})