"""
    Tests for database operations.
"""
from deta import Deta
# from fastapi.testclient import TestClient

# from fastapi_jwt_auth.main import app
from database.db import Database

# client = TestClient(app)
TestDatabase = Database()
# Use test_users table:
TestDatabase.UsersDB = Deta().Base(name="test_users")


def test_db_create_user():
    """Test creating a new user using the database function. """
    assert False

#TODO: Test creating users that should fail...


def test_db_get_user():
    """Test getting a user using the database function. """
    assert False

# TODO: Test getting users that should fail...


def test_db_delete_user():
    """Test deleting a user using the database function. """
    assert False

#TODO: Test deleting users that should fail...


def test_db_update_user():
    """Test updating a user using the database function. """
    assert False

#TODO: Test updating users that should fail...
