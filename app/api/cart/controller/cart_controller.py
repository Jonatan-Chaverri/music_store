
from http import HTTPStatus

from app.api.cart.dao import cart_dao
from app.app import HTTPException


def get_user_cart(user):
    """
    Get the user cart.

    :param str user: the user email of the owner of the cart.
    """
    cart = cart_dao.get_cart(user)
    if not cart:
        raise HTTPException(
            reason='Cart not found', status_code=HTTPStatus.NOT_FOUND
        )

    del cart['_id']
    return cart


def create_user_cart(user, cart_items):
    """
    Create user cart. If the user already has a cart, an error will be thrown.

    :param str user: the user email for which to create a cart.
    :param list cart_items: a list of item ids to add to the user cart.
    """
    cart = cart_dao.get_cart(user)
    if cart:
        raise HTTPException(
            reason='User already has a cart',
            status_code=HTTPStatus.BAD_REQUEST
        )

    result = cart_dao.insert_cart(user, cart_items)
    if not result:
        raise HTTPException(
            reason='Failed to create user cart',
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )

    return 'cart successfully created'


def remove_cart_item(user, cart_item):
    """
    Remove an item from the user cart.

    :param str user: the user email of the owner of the cart.
    :param str cart_item: the item id of the item to delete from the cart.
    """
    count = cart_dao.remove_cart_item(user, cart_item)
    if not count:
        raise HTTPException(
            reason='Cart item was not found',
            status_code=HTTPStatus.NOT_FOUND
        )
    return 'cart item successfully removed'


def delete_user_cart(user):
    """
    Deletes the user cart.

    :param str user: the user email of the owner of the cart.
    """
    count = cart_dao.remove_cart(user)
    if not count:
        raise HTTPException(
            reason='User cart does not exist',
            status_code=HTTPStatus.NOT_FOUND
        )
    return 'cart was successfully deleted'


def update_user_cart_items(user, cart_items):
    """
    Update the cart items for the cart of the user.

    :param str user: the user email of the owner of the cart.
    :param list cart_items: a list of the item ids to be set as new cart items.
    """
    count = cart_dao.update_cart_items(user, cart_items)
    if not count:
        raise HTTPException(
            reason='User cart does not exist',
            status_code=HTTPStatus.NOT_FOUND
        )
    return 'cart items was successfully updated'
