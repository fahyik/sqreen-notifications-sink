import os


class BaseConfig(object):

    # FLASK CONFIG
    # This needs to be set in order to trigger the error handlers
    PROPAGATE_EXCEPTIONS = True


class TestingConfig(BaseConfig):
    TESTING = True


class DevelopmentConfig(BaseConfig):

    pass


class ProductionConfig(BaseConfig):

    pass
