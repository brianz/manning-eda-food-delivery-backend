from flask import request
from flask_restful import Api, Resource, abort, reqparse

from . import app, db
from .models import AddOn, MenuItem

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')


class MenuItemsList(Resource):

    def get(self):
        items = MenuItem.query.all()
        return items

    def post(self):
        data = request.get_json()
        new_item = MenuItem(**data)
        new_item.save()

        return data, 201
        # args = parser.parse_args()
        # print(args.items())
        # todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        # todo_id = 'todo%i' % todo_id
        # TODOS[todo_id] = {'task': args['task']}
        # return TODOS[todo_id], 201


api.add_resource(MenuItemsList, '/menu')
