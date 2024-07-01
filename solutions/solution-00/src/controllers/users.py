"""
Users controller module
"""

from flask import abort, request
from src.models.user import User
from src.models import get_class

def get_users():
    """Returns all users"""
    _cles = get_class("User")
    users: list[User] = _cles.get_all()

    return [user.to_dict() for user in users]


def create_user():
    """Creates a new user"""
    _cles = get_class("User")
    data = request.get_json()

    try:
        user = _cles.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(400, "User already exists")

    return user.to_dict(), 201


def get_user_by_id(user_id: str):
    """Returns a user by ID"""
    _cles = get_class("User")
    user: User | None = _cles.get(user_id)

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


def update_user(user_id: str):
    """Updates a user by ID"""
    _cles = get_class("User")
    data = request.get_json()

    try:
        user = _cles.update(user_id, data)
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


def delete_user(user_id: str):
    """Deletes a user by ID"""
    _cles = get_class("User")
    if not _cles.delete(user_id):
        abort(404, f"User with ID {user_id} not found")

    return "", 204
