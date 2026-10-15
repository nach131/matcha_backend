from app.repositories.users import (
    find_user_by_id,
    insert_user
)

def get_user(user_id):
    return find_user_by_id(user_id)

def create_user(name, email):

    if not name:
        raise ValueError("Name cannot be empty")

    if not email:
        raise ValueError("Email cannot be empty")

    return insert_user(
        name=name,
        email=email
    )