from fastapi import FastAPI

from routes.recipe import recipe_router as recipeRouter

app = FastAPI()

app.include_router(recipeRouter, tags=["Recipe"], prefix="/recipe")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}