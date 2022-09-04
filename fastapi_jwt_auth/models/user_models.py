"""
    For model definitions involving users objects.
"""
from pydantic import BaseModel, EmailStr


class MessageModel(BaseModel):
    message: str


class UserAuthModel(BaseModel):
    """ A model for user authentication. """
    email: EmailStr
    password: str


class UserModelOut(BaseModel):
    """ A model for representing users stored in the database. """
    email: EmailStr
    username: str


class UserModelCreate(UserModelOut):
    """ A model for users stored in the database. """
    fullname: str
    password: str


class UserModelGet(UserModelCreate):
    """ A model for representing users found by attribute in the database. """
    pass
