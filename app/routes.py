from flask_restful import Api, Resource

from . import app

api = Api(app)


class HelloWorld(Resource):

    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')
