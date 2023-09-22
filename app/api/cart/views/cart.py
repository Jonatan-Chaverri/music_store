from flask import Blueprint, request

from app.api.cart.controller.cart_controller import (
    get_user_cart,
    create_user_cart,
    remove_cart_item,
    delete_user_cart,
    update_user_cart_items
)

from app.api import authenticated

BP = Blueprint('cart', __name__, url_prefix='/cart')


@BP.route('', methods=["GET"])
@authenticated
def get_cart():
    """
    Get authenticated user cart with cart items.
    """
    user = request.user
    cart = get_user_cart(user)
    del cart['user']
    return cart


@BP.route('/items', methods=["POST"])
@authenticated
def create_cart():
    """
    Create a cart for the authenticated user.
    """
    user = request.user
    payload = request.payload
    message = create_user_cart(user, payload.get('cart_items'))
    return {'message': message}


@BP.route('/items/<item_id>', methods=["DELETE"])
@authenticated
def delete_cart_item(item_id):
    """
    Delete an item in the cart of the authenticated user
    """
    user = request.user
    message = remove_cart_item(user, item_id)
    return {'message': message}


@BP.route('', methods=["DELETE"])
@authenticated
def delete_cart():
    """
    Delete the authenticated user cart
    """
    user = request.user
    message = delete_user_cart(user)
    return {'message': message}


@BP.route('/items', methods=["PATCH"])
@authenticated
def add_cart_items():
    """
    Update items in the cart of the authenticated user.
    """
    user = request.user
    payload = request.payload
    message = update_user_cart_items(user, payload.get('cart_items'))
    return {'message': message}
