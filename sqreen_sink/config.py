import os


class BaseConfig(object):

    # FLASK MAIL
    MAIL_SERVER = os.environ.get('MAIL_SERVER', default='smtp.gmail.com')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', default='fahyik.sqreen@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # SQREEN
    SQREEN_WEBHOOK_SECRET = os.environ.get('SQREEN_WEBHOOK_SECRET', default='9ao[fUtt2/Z9Y6oekQggZhpaKggKtZzN')


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):

    DEBUG = True


class ProductionConfig(BaseConfig):

    DEBUG = False
    # This needs to be set in order to trigger the error handlers when running
    # on gunicorn
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
