"""
    Various routes for authentication and authorization.
"""
import re
from fastapi import APIRouter, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth import Auth
from database.db import Database
from models.token_models import JWTModel, RefreshTokenModel
from models.user_models import (
    UserAuthModel, UserModelCreate, UserModelOut
)


auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)

auth_handler = Auth()
Database = Database()
security = HTTPBearer()


@auth_router.post("/create-account",
                  response_model=UserModelOut, status_code=201)
def create_account(user_details: UserModelCreate):
    """Creates a new user account. """
    user_out = Database.create_user(user_details=user_details)
    return user_out


@auth_router.post("/login", response_model=JWTModel, status_code=200)
def login(user_details: UserAuthModel):
    """Authenticates a user and returns a JWT when successful. """
    # User's email forced to lowercase:
    user_email = user_details.email.lower()
    user_found = Database.get_user(user_email)
    # [CASE] User not found:
    if not user_found:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    # [CASE] User found, but password is incorrect:
    elif not auth_handler.verify_password(pswd=user_details.password,
                                          hashed_pswd=user_found["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    # [CASE] User found and password is correct:
    access_token = auth_handler.encode_token(user_id=user_email)
    refresh_token = auth_handler.encode_token(user_id=user_email)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@auth_router.get("/refresh-token",
                 response_model=RefreshTokenModel, status_code=200)
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security)):
    """Provides a new access token for a user as a JWT. """
    refresh_token = credentials.credentials
    new_token = auth_handler.encode_refresh_token(refresh_token)
    return {
        "access_token": new_token
    }
