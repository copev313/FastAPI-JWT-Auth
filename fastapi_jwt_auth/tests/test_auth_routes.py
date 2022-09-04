"""
    Tests for the auth API routes.
"""
from fastapi.testclient import TestClient

from fastapi_jwt_auth.main import app


client = TestClient(app)


## Create User Route Tests ##
def test_create_user_route():
    """Test creating a new user account via the API. """
    
    assert False


def test_create_user_already_exists():
    """Test creating a new user account via the API, that already exists. """
    assert False


def test_create_user_with_invalid_email():
    """Test creating a new user account via the API, with an invalid
    email.
    """
    assert False


def test_create_user_no_fullname():
    """Test creating a new user account via the API, with no fullname
    provided.
    """
    assert False


def test_create_user_no_username():
    """Test creating a new user account via the API, with no username
    provided.
    """
    assert False


def test_create_user_no_password():
    """Test creating a new user account via the API, with no password
    provided.
    """
    assert False


## Login Route Tests ##
def test_login_route():
    """Test logging in via the API. """
    assert False


def test_login_with_invalid_email():
    """Test logging in via the API, with an invalid email. """
    assert False


def test_login_with_unknown_email():
    """Test logging in via the API, with an unknown email. """
    assert False


def test_login_with_incorrect_password():
    """Test logging in via the API, with an incorrect password. """
    assert False


## Refresh Token Route Tests ##
def test_refresh_token_route():
    assert False
