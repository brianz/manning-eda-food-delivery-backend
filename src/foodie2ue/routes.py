from pprint import pp

from flask import request
from flask_restful import Api, Resource

from .domain import model
from .service_layer.menu import create_new_menu_item, list_menu_items
from .service_layer.unit_of_work import SqlAlchemyUnitOfWork


class MenuItemsList(Resource):

    def get(self):
        items = list_menu_items(uow=SqlAlchemyUnitOfWork())
        schema = model.MenuItemSchema(many=True)
        return schema.dump(items), 200

    def post(self):
        data = request.get_json()

        menu_item_schema = model.MenuItemSchema()
        menu_item: model.MenuItem = menu_item_schema.load(request.json)
        # pp(menu_item)

        create_new_menu_item(menu_item=menu_item, uow=SqlAlchemyUnitOfWork())

        return data, 201


def connect_routes():
    from .flask_api import app
    api = Api(app)

    api.add_resource(MenuItemsList, '/menu')
