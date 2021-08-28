from fastapi import FastAPI, Depends
from routes.recipes.recipe import recipe_router as recipeRouter
from auth.jwt_bearer import JWTBearer
from routes.admin.users import user_router as UserRouter
from routes.login.login import user_login_router as UserLoginRouter
from routes.admin.login import admin_router as AdminRouter
from routes.login.google import google_route as GoogleRouter
from routes.recipes.ingredients import user_fridge  as UserFridge, user_ingredients as CustomIngredient
from starlette.middleware.sessions import SessionMiddleware
from decouple import config



stage = config('stage')
if stage == "development":
    app = FastAPI()
    print("INFO:     You are in the development environment")
elif stage == "production":
    app = FastAPI(docs_url=None, redoc_url=None)
    print("WARNING:  You are in the PRODUCTION environment !")
else:
    print("ERROR:   Stage in not define.")

app.add_middleware(SessionMiddleware, secret_key=config("secret"))

token_listener = JWTBearer()

app.include_router(recipeRouter, tags=["Recipe"], prefix="/recipe", dependencies=[Depends(token_listener)])
app.include_router(AdminRouter, tags=["Administrators"], prefix="/admin")
app.include_router(UserLoginRouter, tags=["User Signup and Login"])
app.include_router(UserRouter, tags=["Users"], prefix="/users", dependencies=[Depends(token_listener)])
app.include_router(GoogleRouter, tags=["google"], prefix="/google")
app.include_router(UserFridge, tags=["fridge"], prefix="/users/fridge",dependencies=[Depends(token_listener)])
app.include_router(CustomIngredient, tags=["custom ingredients"], prefix="/users/ingredients",dependencies=[Depends(token_listener)])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}



