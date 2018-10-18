import logging

from flask import jsonify
from flask_restful import Resource

logger = logging.getLogger(__name__)


class SqreenWebhook(Resource):

    def post(self):
        """
        Find a way to read header to obtain signature
        """

        return jsonify({"success": True})

    def _verify_signature(self, signature):

        return True
