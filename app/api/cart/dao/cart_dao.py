from app.db import DatabaseManager

COLLECTION_NAME = "cart"
db = DatabaseManager()


def get_cart(user):
    """
    Get the user cart document.
    """
    query = {'user': user}
    user_cart = db.find_one(COLLECTION_NAME, query)
    return user_cart


def insert_cart(user, cart_items):
    """
    Create a cart for the user and insert cart items
    """
    result = db.insert_one(
        COLLECTION_NAME, {"user": user, "cart_items": cart_items}
    )
    return result


def remove_cart_item(user, cart_item):
    """
    Remove a cart item from user cart
    """
    filter_query = {'user': user}
    update_query = {'$pull': {'cart_items': cart_item}}
    modified_count = db.update_one(COLLECTION_NAME, filter_query, update_query)
    return modified_count


def update_cart_items(user, cart_items):
    """
    Update user cart items in user cart
    """
    filter_query = {'user': user}
    update_query = {'$set': {'cart_items': cart_items}}
    modified_count = db.update_one(COLLECTION_NAME, filter_query, update_query)
    return modified_count


def remove_cart(user):
    """
    Delete user cart
    """
    filter_query = {'user': user}
    count = db.delete_one(COLLECTION_NAME, filter_query)
    return count
