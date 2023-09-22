from app.db import DatabaseManager

COLLECTION_NAME = "catalog"
db = DatabaseManager()


def get_all_catalog_items():
    """
    Get all items in catalog database
    """
    result = db.find_all(COLLECTION_NAME)
    return result


def create_catalog(items):
    """
    Insert catalog items documents.

    :param list items: a list of documents that represents the items.
    """
    inserted_ids = db.insert_many(COLLECTION_NAME, items)
    return inserted_ids


def find_catalog_items_by_name(items_names):
    """
    Search catalog items by name.

    :param list<str> items_names: the items names to search for.
    """
    query = {"item_name": {"$in": items_names}}
    item_docs = db.find_all(COLLECTION_NAME, query)
    return item_docs
