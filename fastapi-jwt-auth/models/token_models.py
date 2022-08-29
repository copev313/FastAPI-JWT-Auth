"""
    For defining pydantic models for JavaScript Web Tokens.
"""
from pydantic import BaseModel


class JWTModel(BaseModel):
    """ A model for representing a JWT. """
    access_token: str
    refresh_token: str


class RefreshTokenModel(BaseModel):
    """ A model for representing a refresh token. """
    access_token: str
