from flask import request
from flask_restful import Api, Resource, abort

from ..domain import model
from ..service_layer import menu as menu_service
from ..service_layer.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork


class BaseAPIResource(Resource):
    UOWClass: AbstractUnitOfWork = SqlAlchemyUnitOfWork


class MenuItemsList(BaseAPIResource):

    def get(self):
        with self.UOWClass() as uow:
            items = menu_service.list_menu_items(uow)
            schema = model.MenuItemSchema(many=True)
            return schema.dump(items), 200

    def post(self):
        with self.UOWClass() as uow:
            schema = model.MenuItemSchema()
            menu_item: model.MenuItem = schema.load(request.json)

            (new_menu_item, error) = menu_service.create_new_menu_item(
                menu_item=menu_item,
                uow=uow,
            )
            if error:
                return {'error': error}, 403

            return schema.dump(new_menu_item), 201


class AddOnList(BaseAPIResource):
    """Resource which manages add ons for a single menu item."""

    def __init__(self) -> None:
        super().__init__()
        self.__schema = model.AddOnSchema()
        self.__plural_schema = model.AddOnSchema(many=True)

    @staticmethod
    def _get_item(item_id: int, uow: AbstractUnitOfWork) -> model.MenuItem:
        item = menu_service.get_menu_item(item_id, uow=uow)
        if not item:
            abort(404, message=f"Menu item {item_id} doesn't exist")
        return item

    def get(self, item_id: int):
        """List all of the addons for a given menu item"""
        with self.UOWClass() as uow:
            item: model.MenuItem = self._get_item(item_id, uow)
            return self.__plural_schema.dump(item.addons), 200

    def post(self, item_id: int):
        """Create a new AddOn for a given menu item"""
        with self.UOWClass() as uow:
            menu_item: model.MenuItem = self._get_item(item_id, uow)

            addon_data: model.AddOnSchema = self.__schema.load(request.json)
            addon = menu_service.create_new_addon(addon=addon_data, uow=uow)

            menu_service.add_addon_to_menu_item(menu_item, addon, uow)
            uow.commit()

            return self.__schema.dump(addon), 201


class MenuItemResource(BaseAPIResource):

    def get(self, item_id: int):
        with self.UOWClass() as uow:
            item = menu_service.get_menu_item(item_id, uow=uow)
            if not item:
                abort(404, message=f"Menu item {item_id} doesn't exist")

            schema = model.MenuItemSchema()
            return schema.dump(item), 200


class AddOnResource(BaseAPIResource):

    def get(self, item_id):
        with self.UOWClass() as uow:
            item = menu_service.get_addon(item_id, uow=uow)
            if not item:
                abort(404, message=f"Addon {item_id} doesn't exist")

            schema = model.AddOnSchema()
            return schema.dump(item), 200


def connect_routes():
    from ..api import app
    api = Api(app)

    api.add_resource(MenuItemsList, '/menuitems')
    api.add_resource(MenuItemResource, '/menuitems/<item_id>')
    api.add_resource(AddOnList, '/menuitems/<item_id>/addons')
