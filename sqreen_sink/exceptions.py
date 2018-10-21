import logging
from flask import current_app, jsonify
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


class BasicError(Exception):
    status_code = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BadRequest(BasicError):
    status_code = 400


class InternalServerError(BasicError):
    status_code = 500


def exception_handler(exc):

    if isinstance(exc, HTTPException):
        status_code = exc.code
        err_description = exc.description

    elif isinstance(exc, BasicError):
        status_code = exc.status_code
        err_description = f"{type(exc).__name__}: {exc}"

    else:
        status_code = 500
        err_description = f"{type(exc).__name__}: {exc}"

    response = jsonify(
        {
            "status_code": status_code,
            "error": err_description
        }
    )

    response.status_code = status_code

    # if DEBUG, log exception
    if current_app.config['DEBUG']:
        logger.exception(exc)

    return response
