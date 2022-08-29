"""
    For model definitions involving users objects.
"""
from email import message
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
    fullname: str
    username: str


class UserModelCreate(UserModelOut):
    """ A model for users stored in the database. """
    password: str


class UserModelGet(UserModelCreate):
    """ A model for representing users found by attribute in the database. """
    pass


class UserModelCreateOut(UserModelCreate):
    """ A model for users stored in the database. """
    message: str
    user: UserModelOut
