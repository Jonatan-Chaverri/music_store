import bcrypt

from app.db import DatabaseManager

COLLECTION_NAME = "users"
db = DatabaseManager()


def get_user(user):
    """
    Search for the user document in db.

    :param str user: the user email to search.
    """
    query = {'user': user}
    user = db.find_one(COLLECTION_NAME, query)
    return user


def store_user(user, password):
    """
    Store the user document in db. Password will be encrypted.

    :param str user: the user email to store.
    :param str password: the user password to store.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    result = db.insert_one(
        COLLECTION_NAME, {"user": user, "password": hashed_password}
    )
    return result
