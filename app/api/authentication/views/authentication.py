from flask import Blueprint, request

from app.api import authenticated
from app.api.authentication.controller.authentication_controller import \
    login_user

BP = Blueprint('authentication', __name__, url_prefix='/auth')


@BP.route('/login', methods=["POST"])
def authenticate():
    """
    Performs user authentication. If user is not found, it will create it.
    """
    user = request.payload.get('user')
    password = request.payload.get('password')
    token = login_user(user, password)

    return {'token': token}


@BP.route('')
@authenticated
def get_user():
    """
    Returns the authenticated user email.
    """
    return {'user': request.user}
