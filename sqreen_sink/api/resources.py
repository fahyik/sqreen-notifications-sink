import logging

from flask import request, jsonify
from flask_restful import Resource

from ..dispatch_backends import FileBackend, MailBackend
from ..exceptions import BadRequest
from ..utils import check_signature

logger = logging.getLogger(__name__)


class SqreenWebhook(Resource):

    def post(self):
        """
        Returns a json object with the backends dispatched to
        and respective result (bool) of the dispatch action
        e.g.
        {
            "FileBackend": true,
            "MailBackend": true
        }
        """
        self._verify_signature()

        # TODO: Send this to an async task manager instead
        dispatch = self._dispatch(request)

        return jsonify(dispatch)

    def _dispatch(self, request):

        result = {}

        for backend in [FileBackend, MailBackend]:
            result[backend.__name__] = backend(request).dispatch()

        return result

    def _verify_signature(self, raise_exception=True):

        request_body = request.get_data()
        request_signature = request.headers.get('X-Sqreen-Integrity', '')

        if not check_signature(request_signature, request_body):
            logger.warning("Invalid sqreen webhook notification signature")

            if raise_exception:
                raise BadRequest("Invalid signature")
