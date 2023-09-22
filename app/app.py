import os
import atexit
import logging
import importlib
from http import HTTPStatus

from dotenv import load_dotenv
from flask import Flask, request, jsonify

from app.config import Config
from app.db import DatabaseManager
from app.schema import validate_schema, SchemaError


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s \
                        [%(filename)s:%(funcName)s] %(message)s',
                    handlers=[logging.StreamHandler()])

# Load environment variables from .flaskenv
load_dotenv()


class HTTPException(Exception):
    """
    Typed exception raised when the app encounters an error during execution

    :param str reason: The reason of the exception. Meaningfull message to show
     the user to understand what happened.
    :param int status_code: the integer representation of the http status code
     to return.
    """

    def __init__(self, reason, status_code):
        self.reason = reason
        self.status_code = status_code

        super().__init__(
            'HTTPException raised with status: {}, error: {}'.format(
                status_code, reason,
            )
        )


def register_blueprints(app):
    """
    This will iterate over all API folders located under "api" folder and
    register each of their blueprints to flask.

    :param Flask app: the flask object that represents the app.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    api_file_path = os.path.join(current_directory, 'api')
    api_names = [
        folder
        for folder in os.listdir(api_file_path)
        if os.path.isdir(os.path.join(api_file_path, folder)) and
        '__' not in folder
    ]
    logging.info('Found APIs to register: %s', api_names)

    for api in api_names:
        try:
            module = importlib.import_module(f'app.api.{api}.views.{api}')
            blueprint = getattr(module, 'BP')
            app.register_blueprint(blueprint)
            logging.info('Successfully registered blueprint for API: %s', api)
        except ImportError as e:
            logging.error(
                "Error importing Blueprint in folder '%s': %s", api, e)


def validate_input_payload_schema():
    """
    Validates input payload schema according to each endpoint where is meant
    to be routed. Since it needs to read the payload in here, we store the
    validated payload in a request context variable called "payload", you can
    then access it from the request endpoint with request.payload
    """
    schema_id = 'request_{}'.format(request.endpoint)
    try:
        payload = request.get_json()
    except Exception as e:
        logging.error('Exception in check schema while parsing json: %s', e)
        response = {'error': 'A JSON payload was expected'}
        return jsonify(response), HTTPStatus.BAD_REQUEST

    try:
        validate_schema(schema_id, payload)
    except SchemaError as e:
        message = 'Schema violation for API: {}, errors: {}'.format(
            request.path, e)
        logging.info(message)
        response = {'error': message}
        return jsonify(response), HTTPStatus.BAD_REQUEST

    request.payload = payload


def validate_server_response(response_dict):
    """
    Validates that the server response fullfill the expected schema.

    :param dict response_dict: the dictionary representation of the response
     that is going to be send to the user.
    """
    schema_id = 'response_{}'.format(request.endpoint)
    try:
        validate_schema(schema_id, response_dict)
    except ValueError:
        logging.warning('Missing schema for response: %s', schema_id)
    except SchemaError as e:
        logging.warning('Server returned an invalid response: %s', e)


def create_app():
    """
    Create and returns the flask application object.
    """
    app = Flask(__name__)

    config = Config()
    app.config.update(config.to_dict())

    # Initialize database connection
    DatabaseManager(
        config.DATABASE_HOST,
        config.DATABASE_PORT,
        config.DATABASE_NAME
    )

    register_blueprints(app)

    return app


app = create_app()


@app.before_request
def before_request_middleware():
    """
    Flask middleware that will be executed before each request.
    Validations performed in here:
     - Check that the route have an assigned endpoint to receive it
     - If request is POST, PUT or PATCH, check the payload schema.
    """
    logging.info('Received %s request to: %s', request.method, request.url)

    if request.endpoint is None:
        response = {'error': 'Unknow route'}
        return jsonify(response), HTTPStatus.BAD_REQUEST

    # All APIs that expects a payload should be validated first
    if request.method in ['POST', 'PUT', 'PATCH']:
        response = validate_input_payload_schema()
        if response:
            return response


@app.after_request
def after_request_middleware(response):
    """
    Flask middleware that will be executed after each request.
    Validations performed in here:
     - Check that the response is a json, if not, parse it to a json.
     - Validate that the server returned a valid response (that is according
       to the expected schema)
    """
    logging.info('Returning response for %s %s', request.method, request.url)
    if response.status_code != HTTPStatus.OK:
        return response

    response_data = response.get_json()
    if response_data is None:
        response_data_bytes = response.get_data()
        response_data_text = response_data_bytes.decode('utf-8')
        response_data = {'message': response_data_text}

    validate_server_response(response_data)

    return jsonify(response_data)


@app.errorhandler(HTTPException)
def http_error_handler(e):
    """
    This function will be executed every time we raise our custom HTTPException
    It will parse the exception reason and status code to send it to the user.
    """
    response = {'error': e.reason}
    return jsonify(response), e.status_code


@app.errorhandler(Exception)
def error_handler(e):
    """
    This function will be executed every time there is an Exception in the code
    It will parse the exception to send a meaningfull message to the user.
    """
    logging.exception(e)
    response = {'error': 'Internal Server Error - {}'.format(e)}
    return jsonify(response), HTTPStatus.INTERNAL_SERVER_ERROR


def close_app():
    """
    This code will be executed at application exit. Perform some cleaning.
    """
    logging.info('Closing flask application')
    db = DatabaseManager()
    db.close()


atexit.register(close_app)


if __name__ == '__main__':
    config = Config()
    app.run(host=config.APP_HOST, port=config.APP_PORT)
