import logging
import datetime
from http import HTTPStatus

import jwt
import bcrypt
from flask import current_app

from app.app import HTTPException
from app.api.authentication.dao import authentication_dao


def generate_token(user):
    """
    Generates a new JWT token for the given user. Tokens are set to expire in
    one hour.

    :param str user: the user email.
    """
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'user': user,
        'exp': expiration_time.timestamp()
    }

    token = jwt.encode(
        payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token


def login_user(user, password):
    """
    Performs user authentication. If user is not found, it will create a new
    user in the database.

    :param str user: the user email.
    :param str password: the plain text that represents the user password.
    """
    user_doc = authentication_dao.get_user(user)
    if user_doc:
        logging.info('User found, checking password...')
        hashed_password = user_doc["password"]
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            return generate_token(user)
        raise HTTPException(
            reason='Incorrect password', status_code=HTTPStatus.BAD_REQUEST)

    logging.info('User not found... creating')
    result = authentication_dao.store_user(user, password)
    if not result:
        raise HTTPException(
            reason='Failed to create user',
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )

    return generate_token(user)
