from cerberus import Validator

# ------  Authentication Schemas ------
SCHEMA_REQUEST_LOGIN = {
    'user': {
        'required': True,
        'type': 'string',
        'maxlength': 100,
        'regex': r'[\S]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+'
    },
    'password': {
        'required': True,
        'type': 'string',
        'empty': False,
        'maxlength': 100,
    }
}


SCHEMA_RESPONSE_LOGIN = {
    'token': {
        'required': True,
        'type': 'string',
        'regex': r'[\S]+'
    }
}

SCHEMA_RESPONSE_GET_USER = {
    'user': {
        'required': True,
        'type': 'string'
    }
}


# ------  Cart Schemas ------

SCHEMA_RESPONSE_GET_CART = {
    'cart_items': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'item_id': {'type': 'string', 'required': True},
                'description': {'type': 'string', 'required': True},
                'price': {'type': 'integer', 'required': True, 'min': 1},
            }
        }
    }
}


SCHEMA_REQUEST_CREATE_CART = {
    'cart_items': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'string'
        }
    }
}

SCHEMA_RESPONSE_CREATE_CART = {
    'message': {
        'required': True,
        'type': 'string'
    }
}

SCHEMA_RESPONSE_DELETE_CART_ITEM = {
    'message': {
        'required': True,
        'type': 'string'
    }
}

SCHEMA_RESPONSE_DELETE_CART = {
    'message': {
        'required': True,
        'type': 'string'
    }
}

SCHEMA_REQUEST_ADD_CART_ITEMS = {
    'cart_items': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'string'
        }
    }
}


SCHEMA_RESPONSE_ADD_CART_ITEMS = {
    'message': {
        'required': True,
        'type': 'string'
    }
}


# ------ Catalog Schemas ------
SCHEMA_RESPONSE_GET_CATALOG = {
    'items': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'item_id': {'type': 'string', 'required': True},
                'item_name': {'type': 'string', 'required': True},
                'description': {'type': 'string', 'required': False},
                'price': {'type': 'integer', 'required': True, 'min': 1},
            }
        }
    }
}


SCHEMA_REQUEST_CREATE_CATALOG = {
    'items': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'item_name': {'type': 'string', 'required': True},
                'description': {'type': 'string', 'required': False},
                'price': {'type': 'integer', 'required': True, 'min': 1}
            }
        }
    }
}


SCHEMA_RESPONSE_CREATE_CATALOG = {
    'items': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'string'
        }
    }
}


SCHEMAS_REGISTRY = {
    # Authentication schemas
    'request_authentication.authenticate': SCHEMA_REQUEST_LOGIN,
    'response_authentication.authenticate': SCHEMA_RESPONSE_LOGIN,
    'response_authentication.get_user': SCHEMA_RESPONSE_GET_USER,

    # Cart schemas
    'response_cart.get_cart': SCHEMA_RESPONSE_GET_CART,
    'request_cart.create_cart': SCHEMA_REQUEST_CREATE_CART,
    'response_cart.create_cart': SCHEMA_RESPONSE_CREATE_CART,
    'response_cart.delete_cart_item': SCHEMA_RESPONSE_DELETE_CART_ITEM,
    'response_cart.delete_cart': SCHEMA_RESPONSE_DELETE_CART,
    'request_cart.add_cart_items': SCHEMA_REQUEST_ADD_CART_ITEMS,
    'response_cart.add_cart_items': SCHEMA_RESPONSE_ADD_CART_ITEMS,

    # Catalog schemas
    'response_catalog.get_catalog': SCHEMA_RESPONSE_GET_CATALOG,
    'request_catalog.create_catalog': SCHEMA_REQUEST_CREATE_CATALOG,
    'response_catalog.create_catalog': SCHEMA_RESPONSE_CREATE_CATALOG,
}


class SchemaError(Exception):
    """
    Typed exception raised when some data failed to validate against a schema.
    """
    def __init__(self, schema_id, errors):
        self.schema_id = schema_id
        self.errors = errors

        super().__init__(
            'Schema "{}" violation: {}'.format(schema_id, errors)
        )


def validate_schema(schema_id, data):
    """
    Generic schema validation function.

    :param str schema_id: Identifier of the schema to validate against.
    :param dict data: Data to validate.

    :return: a dictionary with validated and coersed data.
    :rtype: dict

    :raises SchemaError: If data fails to validate against the schema
     identified by schema_id.
    """
    if schema_id not in SCHEMAS_REGISTRY:
        raise ValueError('Unknown schema "{}"'.format(schema_id))

    validator = Validator(SCHEMAS_REGISTRY[schema_id])
    validated = validator.validated(data)

    if validator.errors:
        raise SchemaError(schema_id, validator.errors)

    return validated
