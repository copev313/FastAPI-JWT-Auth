"""
    Various routes for authentication and authorization.
"""
from fastapi import APIRouter, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth import Auth
from database.users_db import create_user, get_user
from models.token_models import JWTModel, RefreshTokenModel
from models.user_models import (
    UserAuthModel, UserModelCreate, UserModelCreateOut, UserModelOut
)


auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)

security = HTTPBearer()
auth_handler = Auth()


@auth_router.post("/create-account",
                  response_model=UserModelCreateOut, status_code=201)
async def create_account(user_details: UserModelCreate):
    """ Creates a new user account. """
    # User's email forced to lowercase:
    user_email = user_details.email.lower()

    # [CHECK] Does the a user with this email already exist?
    if get_user(user_email):
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    try:
        new_user = UserModelCreate(
            username=user_details.username,
            email=user_email,
            fullname=user_details.fullname,
            password=auth_handler.encode_password(user_details.password)
        )
        # Add the new user to the database:
        new_user_obj = create_user(**new_user.dict())
        return UserModelCreateOut(
                message="User account created successfully",
                user=UserModelOut(
                    email=new_user_obj["email"],
                    fullname=new_user_obj["fullname"],
                    username=new_user_obj["username"]
                )
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create new user account. Error: {e}"
        )


@auth_router.post("/login", response_model=JWTModel, status_code=200)
async def login(user_details: UserAuthModel):
    """ Authenticates a user and returns a JWT when successful. """
    # User's email forced to lowercase:
    user_email = user_details.email.lower()
    user = get_user(user_email)
    # [CASE] User does not exist:
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    # [CASE] User exists, but password is incorrect:
    elif not auth_handler.verify_password(
        pswd=user_details.password, hased_pswd=user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    # [CASE] User exists and password is correct, return JWT:
    return {
        "access_token": auth_handler.encode_token(user_email),
        "refresh_token": auth_handler.encode_refresh_token(user_email)
    }


@auth_router.get("/refresh-token",
                 response_model=RefreshTokenModel, status_code=200)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """ Provides a new access token for a user as a JWT. """
    refresh_token = credentials.credentials
    new_token = auth_handler.encode_refresh_token(refresh_token)
    return RefreshTokenModel(access_token=new_token)
