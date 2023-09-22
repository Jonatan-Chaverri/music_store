from http import HTTPStatus

from app.app import HTTPException
from app.api.catalog.dao import catalog_dao


def get_all_catalog():
    """
    Get all catalog items
    """
    items = catalog_dao.get_all_catalog_items()
    if items is None:
        raise HTTPException(
            reason='Failed to get catalog',
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )

    for item in items:
        item['item_id'] = str(item['_id'])
        del item['_id']
    return items


def create_catalog_items(items):
    """
    Insert items in catalog database.

    :param list<dict> items: the items to insert.
    """
    items_names = [item['item_name'] for item in items]
    items_found = catalog_dao.find_catalog_items_by_name(items_names)
    if items_found:
        items_names_found = [item['item_name'] for item in items_found]
        raise HTTPException(
            reason='Failed to insert items: {} already exists'.format(
                items_names_found),
            status_code=HTTPStatus.BAD_REQUEST
        )

    inserted_ids = catalog_dao.create_catalog(items)
    inserted_ids_str = []
    if inserted_ids:
        inserted_ids_str = [str(mongo_id) for mongo_id in inserted_ids]
    return inserted_ids_str
