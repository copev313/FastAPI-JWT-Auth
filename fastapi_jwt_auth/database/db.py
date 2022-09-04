"""
    A module dedicated to handling database operations.
"""
from deta import Deta
from fastapi import HTTPException

from auth import Auth
from models.user_models import (
    UserModelCreate, UserModelGet, UserModelOut
)


deta = Deta()
auth_handler = Auth()


class Database:

    UsersDB = deta.Base(name="users")


    def create_user(self, user_details: UserModelCreate) -> UserModelOut:
        """Creates a new user in the users database. 
        
        Parameters
        ----------
        user_details: UserModelCreate
            A user model used for creating an account.
        
        Returns
        -------
        UserModelOut:
            The username & email of the newly created user.
        """
        # User's email forced to lowercase:
        user_email = user_details.email.lower()
        # [CHECK] Does the a user with this email already exist?
        if self.get_user(user_email):
            raise HTTPException(
                status_code=400,
                detail="User already exists"
            )

        try:
            user_email = user_details.email.lower()
            new_user = {
                "key": user_email,
                "username": user_details.username,
                "email": user_email,
                "fullname": user_details.fullname,
                "password": auth_handler.encode_password(
                    pswd=user_details.password
                )
            }
            # Add the new user to the database:
            new_user_obj = self.UsersDB.put(new_user)
            return {
                "email": new_user_obj.get("email"),
                "username": new_user_obj.get("username")
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create_user. Error: {e} "
            )


    def get_user(self, user_email: str) -> UserModelGet:
        """Gets a user from the users database by key (email). 
        
        Parameters
        ----------
        user_email: str
            The email of the user to be retrieved.
        
        Returns
        -------
        UserModelGet:
            The user's details.
        """
        try:
            user = self.UsersDB.get(key=user_email.lower())
            if user:
                return {
                    "fullname": user.get("fullname"),
                    "email": user.get("email"),
                    "username": user.get("username"),
                    "password": user.get("password")
                }
            return None

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get_user. Error: {e} "
            )


    def update_user(self, user_details: UserModelCreate) -> UserModelOut:
        """Updates a user's details in the users database. 
        
        Parameters
        ----------
        user_details: UserModelCreate
            A user model used for updating an account.
        
        Returns
        -------
        UserModelOut:
            The username & email of the updated user.
        """
        try:
            user_email = user_details.email.lower()
            updated_user = {
                "key": user_email,
                "username": user_details.username,
                "email": user_email,
                "fullname": user_details.fullname,
                "password": auth_handler.encode_password(
                    pswd=user_details.password
                )
            }
            # Update the user in the database:
            updated_user_obj = self.UsersDB.put(updated_user)
            return {
                "email": updated_user_obj.get("email"),
                "username": updated_user_obj.get("username")
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update_user. Error: {e} "
            )


    def remove_user(self, user_email: str) -> None:
        """Removes a user from the users database by key (email). 
        
        Parameters
        ----------
        user_email: str
            The email of the user to be removed.
        """
        try:
            self.UsersDB.delete(key=user_email.lower())

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to remove_user. Error: {e} "
            )
