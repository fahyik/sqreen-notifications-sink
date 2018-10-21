import hmac
import hashlib

from flask import current_app


def check_signature(request_signature, request_body):
    """
    see: https://docs.sqreen.io/integrations/webhooks/#signature
    """

    secret_key = current_app.config['SQREEN_WEBHOOK_SECRET']
    secret_key = secret_key.encode('utf-8')

    hasher = hmac.new(secret_key, request_body, hashlib.sha256)
    dig = hasher.hexdigest()

    return hmac.compare_digest(dig, request_signature)
