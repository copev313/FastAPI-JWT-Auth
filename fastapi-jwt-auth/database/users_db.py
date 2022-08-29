"""
    A module dedicated to handling database operations.
"""
from deta import Deta

from auth import Auth
from models.user_models import UserModelCreate, UserModelGet, UserModelOut


deta = Deta()
db = deta.Base(name="users")
auth_handler = Auth()


async def get_user(email: str) -> UserModelGet:
    """ Gets a user from the database by their key (email). """
    # Find user by key / email:
    user =  db.get(key=email.lower())
    if user:
        return UserModelGet(
            email=user.get("email"),
            fullname=user.get("fullname"),
            username=user.get("username"),
            password=user.get("password")
        ).dict()


async def create_user(user_details: UserModelCreate) -> UserModelOut:
    """ Creates a new user in the database. """
    try:
        user_email = user_details.email.lower()
        new_user = {
            "key": user_email,
            "username": user_details.username,
            "email": user_email,
            "fullname": user_details.fullname,
            "password": auth_handler.encode_password(user_details.password)
        }
        created_user_obj = db.put(new_user)
        return UserModelOut(
            email=created_user_obj["email"],
            fullname=created_user_obj["fullname"],
            username=created_user_obj["username"]
        )
    except Exception as e:
        return f"Failed to create new user account. Error: {e}"
