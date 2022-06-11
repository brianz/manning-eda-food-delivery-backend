from pprint import pp

from flask import request
from flask_restful import Api, Resource

from .domain import model


class MenuItemsList(Resource):

    # def get(self):
    #     items = MenuItem.query.all()
    #     return items

    def post(self):
        data = request.get_json()
        # new_item = model.MenuItem(**data)
        # new_item.save()

        # session = get_session()
        # repo = SqlAlchemyRepository(session)
        menu_item = model.MenuItem.load(request.json)
        pp(menu_item)

        return data, 201


def connect_routes():
    from . import app
    api = Api(app)

    api.add_resource(MenuItemsList, '/menu')
