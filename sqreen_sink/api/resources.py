import logging

from flask import request, jsonify
from flask_restful import Resource

from .dispatch_backends import FileBackend, LogBackend, MailBackend
from ..exceptions import BadRequest
from ..utils import check_signature

logger = logging.getLogger(__name__)


class SqreenWebhook(Resource):

    def post(self):
        """
        responses:
            - 200:
                - description:
                    object with the dispatch result (bool) of each
                    target backend
                - example:
                    {
                        "FileBackend": true,
                        "MailBackend": true
                    }
            - 400:
                - description:
                    invalid webhook signature
                - example:
                    {
                        "error": "BadRequest: Invalid signature",
                        "status_code": 400
                    }
        """
        self._verify_signature()

        # TODO: Send this to an async task manager instead
        # Sqreen seems to have a timeout for the registration of webhook
        dispatch = self._dispatch(request)

        return jsonify(dispatch)

    def _dispatch(self, request):

        result = {}

        # TODO: Crete more elegant way to register dispatch targets
        for backend in [LogBackend, FileBackend, MailBackend]:
            result[backend.__name__] = backend(request).dispatch()

        return result

    def _verify_signature(self, raise_exception=True):

        request_body = request.get_data()
        request_signature = request.headers.get('X-Sqreen-Integrity', '')

        if not check_signature(request_signature, request_body):
            logger.warning("Invalid sqreen webhook notification signature")

            if raise_exception:
                raise BadRequest("Invalid signature")
