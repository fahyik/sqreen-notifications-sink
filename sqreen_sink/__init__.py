import os

from flask import Flask

from .config import DevelopmentConfig, ProductionConfig
from .utils import exception_handler


def create_app(config_filename=None):

    # INIT
    # ------------------------------------------------------
    app = Flask(__name__)

    env = os.environ.get('FLASK_SETTINGS_ENV', default="development")

    if env == "development":
        app.config.from_object(DevelopmentConfig)
    elif env == "production":
        app.config.from_object(ProductionConfig)
    else:
        raise Exception("FLASK_SETTINGS_ENV not properly configured")

    # EXCEPTION HANDLER
    # ------------------------------------------------------
    @app.errorhandler(Exception)
    def on_exception(exception):
        return exception_handler(exception)

    # REGISTER ROUTES
    # ------------------------------------------------------
    from .api.routes import api
    api.init(app)

    return app
