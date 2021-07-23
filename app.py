from fastapi import FastAPI, Depends

from routes.recipe import recipe_router as recipeRouter
from auth.jwt_bearer import JWTBearer
from routes.user import user_router as UserRouter
from routes.user import user_login_router as UserLoginRouter
from routes.admin import admin_router as AdminRouter
from routes.google_auth import google_route as GoogleRouter
from starlette.middleware.sessions import SessionMiddleware
from decouple import config


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=config("secret"))

token_listener = JWTBearer()

app.include_router(recipeRouter, tags=["Recipe"], prefix="/recipe", dependencies=[Depends(token_listener)])
app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
app.include_router(UserLoginRouter, tags=["User Signup and Login"])
app.include_router(UserRouter, tags=["Users"], prefix="/users", dependencies=[Depends(token_listener)])
app.include_router(GoogleRouter, tags=["google"], prefix="/google")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}