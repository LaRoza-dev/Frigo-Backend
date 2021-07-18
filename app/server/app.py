from fastapi import FastAPI

from app.server.routes.recipe import router as recipeRouter

app = FastAPI()

app.include_router(recipeRouter, tags=["recipe"], prefix="/recipe")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}