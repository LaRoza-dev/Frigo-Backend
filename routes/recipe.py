from auth.jwt_handler import decodeJWT
from fastapi import APIRouter, Body,Header

from fastapi.encoders import jsonable_encoder
from typing import Optional

from database.recipe_database import (
    add_recipe,
    delete_recipe,
    retrieve_recipe,
    retrieve_recipes,
    update_recipe,
    retrieve_recipes_by_ingredients
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


@recipe_router.post("/", response_description="Recipe data added into the database")
async def add_recipe_data(recipe: RecipeSchema = Body(...),authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    if is_admin:
        user_id = "1"
    else:
        user_id = (await retrieve_user(email=token_data['user_id']))['id']
    recipe.user_id = user_id
    recipe = jsonable_encoder(recipe)
    new_recipe = await add_recipe(recipe)
    return ResponseModel(new_recipe, "Recipe added successfully.")


@recipe_router.get("/", response_description="Recipes retrieved")
async def get_recipes(authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    user_id = (await retrieve_user(email=token_data['user_id']))['id']
    recipes = await retrieve_recipes(user_id,is_admin)
    if recipes:
        return ResponseModel(recipes, "Recipes data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")

@recipe_router.post("/search", response_description="Recipes retrieved")
async def get_recipes_by_ingredients(query:list=Body(...),authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    is_admin = token_data['is_admin']
    user_id = (await retrieve_user(email=token_data['user_id']))['id']
    recipes = await retrieve_recipes_by_ingredients(user_id,is_admin,query)
    if recipes:
        return ResponseModel(recipes, "Recipes data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")


@recipe_router.get("/{id}", response_description="Recipe data retrieved")
async def get_recipe_data(id,authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    user_id = (await retrieve_user(email=token_data['user_id']))['id']
    recipe = await retrieve_recipe(id,user_id)
    if recipe:
        return ResponseModel(recipe, "Recipe data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Recipe doesn't exist.")


@recipe_router.put("/{id}")
async def update_recipe_data(id: str, req: UpdateRecipeModel = Body(...),authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    user_id = (await retrieve_user(email=token_data['user_id']))['id']
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


@recipe_router.delete("/{id}", response_description="Recipe data deleted from the database")
async def delete_recipe_data(id: str,authorization:Optional[str]=Header(None)):
    token_data = decodeJWT(authorization.split(' ')[1])
    user_id = (await retrieve_user(email=token_data['user_id']))['id']
    deleted_recipe = await delete_recipe(id,user_id)
    if deleted_recipe:
        return ResponseModel(
            "Recipe with ID: {} removed".format(id), "Recipe deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Recipe with id {0} doesn't exist".format(id)
    )