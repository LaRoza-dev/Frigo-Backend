from auth.jwt_handler import decodeJWT
from fastapi import APIRouter, Body,Header

from fastapi.encoders import jsonable_encoder
from typing import Optional

import time

from database.recipe_database import (
    add_recipe,
    delete_recipe,
    retrieve_recipe,
    retrieve_recipe_name,
    retrieve_recipes,
    update_recipe,
    retrieve_recipes_by_ingredients,
    delete_recipe_admin,
    update_recipe_admin
)

from database.user_database import (
    retrieve_user
)
from models.recipe import (
    ErrorResponseModel,
    ResponseModel,
    RecipeSchema,
    UpdateRecipeModel,
)

recipe_router = APIRouter()


# ADD -------------------------------------------------------------------------------
# Add a recipe
@recipe_router.post("/", response_description="Recipe data added into the database")
async def add_recipe_data(recipe: RecipeSchema = Body(...),authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    if is_admin:
        user_id = "1"
    else:
        user_id = (await retrieve_user(email=token_data['email']))['id']
    recipe.user_id = user_id
    recipe = jsonable_encoder(recipe)
    new_recipe = await add_recipe(recipe)
    return ResponseModel(new_recipe, "Recipe added successfully.")


# GET -------------------------------------------------------------------------------
# Get all recipes
@recipe_router.get("/", response_description="Recipes retrieved")
async def get_recipes(authorization:Optional[str]=Header(None),pageNumber:int=0, nPerPage:int=10):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    user_id = (await retrieve_user(email=token_data['email']))['id']
    recipes = await retrieve_recipes(user_id,pageNumber, nPerPage,is_admin)
    if recipes:
        return ResponseModel(recipes, "Recipes data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")


# Get recipes with matching list
@recipe_router.post("/search", response_description="Recipes retrieved")
async def get_recipes_by_ingredients(query:list=Body(...),authorization:Optional[str]=Header(None),pageNumber:int=0, nPerPage:int=10):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    user_id = (await retrieve_user(email=token_data['email']))['id']
    recipes = await retrieve_recipes_by_ingredients(user_id,pageNumber, nPerPage,is_admin,query)
    if recipes:
        return ResponseModel(recipes, "Recipes data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")


# Get recipe with matchin id
@recipe_router.get("/get_id/{id}", response_description="Recipe data retrieved")
async def get_recipe_data(id,authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    user_id = (await retrieve_user(email=token_data['email']))['id']
    recipe = await retrieve_recipe(id,user_id)
    if recipe:
        return ResponseModel(recipe, "Recipe data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Recipe doesn't exist.")


# Get recipes with matching name
@recipe_router.get("/{name}", response_description="Recipe data retrieved")
async def get_recipe_name(name,authorization:Optional[str]=Header(None),pageNumber:int=0, nPerPage:int=10):
    token_data = decodeJWT(authorization.split(' ')[1])
    user_id = (await retrieve_user(email=token_data['email']))['id']
    recipe = await retrieve_recipe_name(name,user_id,pageNumber, nPerPage)
    if recipe:
        return ResponseModel(recipe, "Recipe data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Recipe doesn't exist.")


# Update -------------------------------------------------------------------------------
# Update recipe with maching id
@recipe_router.put("/{id}")
async def update_recipe_data(id: str, req: UpdateRecipeModel = Body(...),authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']

    if is_admin:
        req = {k: v for k, v in req.dict().items() if v is not None}
        updated_recipe = await update_recipe_admin(id, req)

    else:
        user_id = (await retrieve_user(email=token_data['email']))['id']
        req = {k: v for k, v in req.dict().items() if v is not None}
        updated_recipe = await update_recipe(id, req,user_id)
    
    if updated_recipe:
        return ResponseModel(
            "Recipe with ID: {} name update is successful".format(id),
            "Recipe name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the recipe data.",
    )


# DELETE -------------------------------------------------------------------------------
# Delete recipe with matching id
@recipe_router.delete("/{id}", response_description="Recipe data deleted from the database")
async def delete_recipe_data(id: str,authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    if is_admin:
        deleted_recipe = await delete_recipe_admin(id)
    else:
        user_id = (await retrieve_user(email=token_data['email']))['id']
        deleted_recipe = await delete_recipe(id,user_id)
    if deleted_recipe:
        return ResponseModel(
            "Recipe with ID: {} removed".format(id), "Recipe deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Recipe with id {0} doesn't exist".format(id)
    )