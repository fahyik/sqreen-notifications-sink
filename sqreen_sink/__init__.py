import os
from logging.config import dictConfig

from flask import jsonify, Flask
from flask_mail import Mail

from .config import DevelopmentConfig, ProductionConfig, LOGGING
from .exceptions import exception_handler


__version__ = "0.0.1"

mail = Mail()


def create_app(config=None):

    # INIT
    # ------------------------------------------------------
    app = Flask(__name__)

    env = os.environ.get('FLASK_ENV', default="development")

    if config is not None:
        app.config.from_object(config)
    elif env == "development":
        app.config.from_object(DevelopmentConfig)
    elif env == "production":
        app.config.from_object(ProductionConfig)
    else:
        raise Exception("FLASK_ENV not properly configured")

    # LOGGING
    # ------------------------------------------------------
    dictConfig(LOGGING)

    # FLASK MAIL
    # ------------------------------------------------------
    mail.init_app(app)

    # ROOT
    @app.route("/")
    def root():
        return jsonify({
            "app": __name__,
            "version": __version__
        })

    # EXCEPTION HANDLER
    # ------------------------------------------------------
    @app.errorhandler(Exception)
    def on_exception(exception):
        return exception_handler(exception)

    # REGISTER ROUTES
    # ------------------------------------------------------
    from .api.routes import api
    api.init_app(app)

    return app
