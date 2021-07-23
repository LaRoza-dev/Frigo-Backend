import json
from fastapi import APIRouter
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from auth.jwt_handler import decodeJWT, token_response, decodeGoogle


config = Config('.env')
oauth = OAuth(config)

google_route = APIRouter()

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@google_route.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user :
        return user.find('email')
    return RedirectResponse('/google/login')


@google_route.get('/login')
async def login(request: Request):
    user = request.session.get('user')
    token = request.session.get('token')
    if user and token:
        return RedirectResponse('/google')
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri) 

@google_route.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)   
    except OAuthError as error:
        return HTMLResponse(error.error)
    user = await oauth.google.parse_id_token(request, token)
    request.session['user'] = dict(user)
    request.session['token'] = dict(token)
    return RedirectResponse('/google')
