import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config
from .database_helper import recipe_helper
import re
from operator import itemgetter


stage = config('stage')
if stage == "development":
    MONGO_DETAILS = config('MONGO_DETAILS_DEV')
elif stage == "production":
    MONGO_DETAILS = config('MONGO_DETAILS_PROD')
else:
    print("WRONG MONGO ENV")

client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_DETAILS, tls=True, tlsAllowInvalidCertificates=True)

database = client.recipes

recipe_collection = database.get_collection("recipes_collection")


# ADD -------------------------------------------------------------------------------
# Retrieve all recipes present in the database
async def retrieve_recipes(user_id, pageNumber: int, nPerPage: int, is_admin=None,name='',sort='name'):
    recipes = []
    if is_admin:
        async for recipe in recipe_collection.find({}):
            recipes.append(recipe_helper(recipe))

        recipes = list(filter(lambda x: name in x["name"] , recipes))
        total_number = len(recipes)
        if sort =='star':
            recipes = sorted(recipes, key=itemgetter('stars'),reverse=True)
        recipes = recipes[pageNumber*nPerPage:pageNumber*nPerPage+nPerPage]
    else:
        async for recipe in recipe_collection.find({"$or": [{"user_id": user_id}, {"user_id": "1"}]}):
            recipes.append(recipe_helper(recipe))

        recipes = list(filter(lambda x: name in x["name"] , recipes))
        total_number = len(recipes)
        if sort =='name':
            recipes = sorted(recipes, key=itemgetter('name'))
        elif sort =='star':
            recipes = sorted(recipes, key=itemgetter('stars'),reverse=True)
        recipes = recipes[pageNumber*nPerPage:pageNumber*nPerPage+nPerPage]
    return recipes, total_number


# Add a new recipe into to the database
async def add_recipe(recipe_data: dict) -> dict:
    recipe = await recipe_collection.insert_one(recipe_data)
    new_recipe = await recipe_collection.find_one({"_id": recipe.inserted_id})
    return recipe_helper(new_recipe)


# Get -------------------------------------------------------------------------------
# Retrieve all recipes present in the database which has ingredient list
async def retrieve_recipes_by_ingredients(user_id, pageNumber: int, nPerPage: int, is_admin=None, query: list = None,name='',sort='ing_count'):
    recipes = []
    queryRE = list(map(lambda recipe: re.compile(
        f"^.*{recipe}.*$", re.IGNORECASE), query))
    if is_admin:
        total_number = await recipe_collection.count_documents({"ingredients": {"$in": queryRE}})
        async for recipe in recipe_collection.find({"ingredients": {"$in": queryRE}}):
            recipes.append(recipe_helper(recipe))
        
        #For getting Ing count
        for recipe in recipes:
            ings =[]
            for q in query:
                for index,ing in enumerate(recipe["ingredients"]):
                    if re.findall(f"^.*{q}.*$", ing):
                        ings.append(index)
            #Ings indexes and count
            ings = list(dict.fromkeys(ings))
            recipe["finded_ing_count"] = len(ings)
            recipe["finded_ing_index"] = ings

        recipes = list(filter(lambda x: name in x["name"] , recipes))
        total_number = len(recipes)
        if sort =='star':
            recipes = sorted(recipes, key=itemgetter('stars'),reverse=True)
        elif sort =='name':
            recipes = sorted(recipes, key=itemgetter('name'))
        elif sort =='ing_count':
            recipes.sort(key=itemgetter('finded_ing_count'),reverse=True)
        recipes = recipes[pageNumber*nPerPage:pageNumber*nPerPage+nPerPage]

    else:
        async for recipe in recipe_collection.find({
            "$and": [
                {"$or": [
                    {"user_id": user_id},
                    {"user_id": "1"}
                ]
                }, {"ingredients": {"$in": queryRE}}
            ]
        }):
            recipes.append(recipe_helper(recipe))

        #For getting Ing count
        for recipe in recipes:
            ings =[]
            for q in query:
                for index,ing in enumerate(recipe["ingredients"]):
                    if re.findall(f"^.*{q}.*$", ing):
                        ings.append(index)
            #Ings indexes and count
            ings = list(dict.fromkeys(ings))
            recipe["finded_ing_count"] = len(ings)
            recipe["finded_ing_index"] = ings

        recipes = list(filter(lambda x: name in x["name"] , recipes))
        total_number = len(recipes)
        if sort =='star':
            recipes = sorted(recipes, key=itemgetter('stars'),reverse=True)
        elif sort =='name':
            recipes = sorted(recipes, key=itemgetter('name'))
        elif sort =='ing_count':
            recipes.sort(key=itemgetter('finded_ing_count'),reverse=True)
        recipes = recipes[pageNumber*nPerPage:pageNumber*nPerPage+nPerPage]
    return recipes, total_number


# Retrieve a recipe with a matching ID
async def retrieve_recipe(id: str, user_id: str) -> dict:
    recipe = await recipe_collection.find_one({"$or": [{"_id": ObjectId(id), "user_id": user_id}, {"_id": ObjectId(id), "user_id": "1"}]})
    if recipe:
        return recipe_helper(recipe)


# Retrieve a recipe with a matching name
async def retrieve_recipe_name(name: str, user_id: str, pageNumber: int, nPerPage: int) -> dict:
    recipes = []
    total_number = await recipe_collection.count_documents({"$or": [{"name": {'$regex': f".*{name}.*", "$options": "i"}, "user_id": user_id}, {"name": {'$regex': f".*{name}.*", "$options": "i"}, "user_id": "1"}]})
    async for recipe in recipe_collection.find({"$or": [{"name": {'$regex': f".*{name}.*", "$options": "i"}, "user_id": user_id}, {"name": {'$regex': f".*{name}.*", "$options": "i"}, "user_id": "1"}]}).sort("name").skip(((pageNumber - 1) * nPerPage) if (pageNumber > 0) else 0).limit(nPerPage):
        recipes.append(recipe_helper(recipe))
    return recipes, total_number


# Update -------------------------------------------------------------------------------
# Update a recipe with a matching ID
async def update_recipe(id: str, data: dict, user_id: str):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    recipe = await recipe_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
    if recipe:
        updated_recipe = await recipe_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_recipe:
            return True
        return False


# ADMIN Update any recipe with a matching ID
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


# DELETE -------------------------------------------------------------------------------
# Delete a recipe from the database
async def delete_recipe(id: str, user_id: str):
    recipe = await recipe_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
    if recipe:
        await recipe_collection.delete_one({"_id": ObjectId(id)})
        return True


# ADMIN Deletes any recipe from the database
async def delete_recipe_admin(id: str):
    return await recipe_collection.delete_one({"_id": ObjectId(id)})
