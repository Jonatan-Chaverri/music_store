from flask import Blueprint, request

from app.api import authenticated
from app.api.catalog.controller.catalog_controller import (
    get_all_catalog, create_catalog_items
)

BP = Blueprint('catalog', __name__, url_prefix='/catalog')


@BP.route('', methods=["GET"])
def get_catalog():
    """
    Get all catalog items
    """
    items = get_all_catalog()
    return {'items': items}


@BP.route('', methods=["POST"])
@authenticated
def create_catalog():
    """
    Create catalog items
    """
    payload = request.payload
    inserted_ids = create_catalog_items(payload['items'])
    return {'items': inserted_ids}
