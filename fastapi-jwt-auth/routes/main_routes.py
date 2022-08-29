"""
    For defining genral / main routes for the app.
"""
from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth import Auth
from models.user_models import MessageModel


main_router = APIRouter(
    prefix="/api/v1",
    tags=["main"]
)

security = HTTPBearer()
auth_handler = Auth()


@main_router.get("/secret-stuff")
async def secret_data(
    credentials: HTTPAuthorizationCredentials = Security(security)) -> MessageModel:
    """ An example of a protected endpoint. """
    token = credentials.credentials
    # [CASE] Token is successfully decoded:
    if auth_handler.decode_token(token):
        return {"message": "Successfully decoded token... top secret data! :D"}


@main_router.get("/notsecret-stuff")
async def not_secret_data() -> MessageModel:
    return {"message": "Not secret data..."}
