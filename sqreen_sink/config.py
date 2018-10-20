import os


class BaseConfig(object):

    # FLASK CONFIG

    # FLASK MAIL
    MAIL_SERVER = os.environ.get('MAIL_SERVER', default='smtp.gmail.com')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SERVER', default="do_not_reply@sqreen_sink.com")
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', default='fahyik.sqreen@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', default='password')

    # SQREEN
    SQREEN_WEBHOOK_SECRET = os.environ.get('SQREEN_WEBHOOK_SECRET', default='1234')


class TestingConfig(BaseConfig):
    TESTING = True


class DevelopmentConfig(BaseConfig):

    pass


class ProductionConfig(BaseConfig):
    # This needs to be set in order to trigger the error handlers
    PROPAGATE_EXCEPTIONS = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(process)d %(thread)d %(module)s %(name)s %(lineno)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'loggers': {
        'gunicorn.access': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'gunicorn.error': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'sqreen_sink': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        }
    },
}
