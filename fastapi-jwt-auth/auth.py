import os
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime as dt, timedelta

class Auth:

    # Load environment variables from .env file:
    load_dotenv()

    # Initialize hasher and secret key:
    hasher = CryptContext(schemes=["bcrypt"])
    secret_key = os.getenv("SECRET_KEY")


    def encode_password(self, pswd) -> str:
        """Hashes a password and returns the encoded string. """
        return self.hasher.hash(pswd)


    def verify_password(self, pswd, hashed_pswd) -> bool:
        """Verifies that the password provided matches the hashed password. """
        return self.hasher.verify(pswd, hashed_pswd)


    def encode_token(self,
                     user_id: str,
                     expiry_mins: int = 30) -> str:
        """Encodes a payload with the username and expiration datetime, 
        returning the JWT.

        Parameters
        ----------
        user_id: str
            The user's identifier (email) to use as a subject in the payload.

        expiry_mins: int, optional (default=30)
            The number of minutes from now the token will expire.

        scope: str, optional (default="access_token")
            The scope assigned to the payload.
        """
        payload = {
            # Expiration time is in hours:
            "exp": dt.utcnow() + timedelta(hours=0, minutes=expiry_mins),
            # Initialized date time:
            "iat": dt.utcnow(),
            # Subject of payload:
            "sub": user_id,
            # Scope of payload:
            "scope": "access_token",
        }
        return jwt.encode(
            payload=payload,
            key=self.secret_key,
            algorithm="HS256"
        )


    def decode_token(self, token: str):
        """Decodes a JWT and returns the token's subject (user's email). """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            # [CASE] Token scope is 'access_token', return username:
            if payload["scope"] == "access_token":
                return payload["sub"]

            # [CASE] Token scope is is NOT 'access_token', raise Exception:
            raise HTTPException(
                    status_code=401,
                    detail="The scope for the token is invalid"
            )

        # [CASE] Token is expired, raise Exception:
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                    status_code=401,
                    detail="Token has expired"
            )
        # [CASE] Token is invalid, raise Exception:
        except jwt.InvalidTokenError:
            raise HTTPException(
                    status_code=401,
                    detail="Token is invalid"
            )
        # [CASE] Base PyJWT error, raise Exception:
        except jwt.PyJWTError:
            raise HTTPException(
                    status_code=401,
                    detail="JWT Error Encountered"
            )


    def encode_refresh_token(self,
                             user_id: str,
                             expiry_hrs: int = 8) -> str:
        """Encodes a refresh token with the username and expiration datetime, 
        returning a refreshed JWT.
        
        Parameters
        ----------
        user_id: str
            The user identifer (email) to use as a subject in the payload.
        
        expiry_hrs: int, optional (default=8)
            The number of hours from now the refresh token will expire.
        """
        payload = {
            # Expiration time is in hours:
            "exp": dt.utcnow() + timedelta(days=0, hours=expiry_hrs),
            # Initialized date time:
            "iat": dt.utcnow(),
            # Subject of payload:
            "sub": user_id,
            # Scope of payload:
            "scope": "refresh_token",
        }
        return jwt.encode(
            payload=payload,
            key=self.secret_key,
            algorithm="HS256"
        )
