from flask_restful import Api

from .resources import SqreenWebhook


api = Api()

# register resources (has to be done before registering the api extension itself)
api.add_resource(SqreenWebhook, '/sqreen/notify/')
