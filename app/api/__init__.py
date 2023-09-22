from functools import wraps
from http import HTTPStatus

import jwt
from flask import request, current_app

from app.app import HTTPException


def authenticated(func):
    """
    Decorator for flask endpoints that require authentication. It will check
    and decode user token in "Authorization" header. The authenticated user
    will be set as a variable in the request context named "user".
    """

    @wraps(func)
    def wrapper(*args,  **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            raise HTTPException(
                reason='Token was not found in request headers',
                status_code=HTTPStatus.UNAUTHORIZED
            )
        if token.lower().startswith('bearer '):
            token = token[len('bearer '):]

        try:
            payload = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user = payload['user']

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                reason='Token has expired', status_code=HTTPStatus.UNAUTHORIZED
            )

        except jwt.DecodeError:
            raise HTTPException(
                reason='Token is invalid', status_code=HTTPStatus.UNAUTHORIZED
            )

        return func(*args, **kwargs)

    return wrapper
