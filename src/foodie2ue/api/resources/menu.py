from flask import request
from flask_restful import abort
from marshmallow import ValidationError

from . import BaseAPIResource

from ...domain import model
from ...service_layer import menu as menu_service
from ...service_layer.unit_of_work import AbstractUnitOfWork


class MenuItemsListCreate(BaseAPIResource):

    def __init__(self) -> None:
        super().__init__()
        self.__schema = model.MenuItemSchema()
        self.__plural_schema = model.MenuItemSchema(many=True)

    def get(self):
        with self.UOWClass() as uow:
            items = menu_service.list_menu_items(uow)
            return self.__plural_schema.dump(items), 200

    def post(self):
        with self.UOWClass() as uow:
            try:
                menu_item: model.MenuItem = self.__schema.load(request.json)
            except ValidationError as error:
                abort(400, message="Invalid menu item payload", details=error.messages)

            (new_menu_item, error) = menu_service.create_new_menu_item(
                menu_item=menu_item,
                uow=uow,
            )
            if error:
                return {'message': str(error), 'details': error.details}, 400

            return self.__schema.dump(new_menu_item), 201


class MenuItemAddOnListCreate(BaseAPIResource):
    """Resource which manages add ons for a single menu item."""

    def __init__(self) -> None:
        super().__init__()
        self.__schema = model.AddOnSchema()
        self.__plural_schema = model.AddOnSchema(many=True)

    @staticmethod
    def _get_item(item_id: int, uow: AbstractUnitOfWork) -> model.MenuItem:
        item = menu_service.get_menu_item(item_id, uow=uow)
        if not item:
            abort(404, message=f"AddOn item {item_id} doesn't exist", details={})
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

            try:
                addon_data: model.AddOnSchema = self.__schema.load(request.json)
            except ValidationError as error:
                abort(400, message="Invalid addon payload", details=error.messages)

            addon = menu_service.create_new_addon(addon=addon_data, uow=uow)

            menu_service.add_addon_to_menu_item(menu_item, addon, uow)
            uow.commit()

            return self.__schema.dump(addon), 201


class MenuItemResource(BaseAPIResource):

    def __init__(self) -> None:
        super().__init__()
        self.__schema = model.MenuItemSchema()

    @staticmethod
    def _get_item(item_id: int, uow) -> model.AddOn:
        item = menu_service.get_menu_item(item_id, uow=uow)
        if not item:
            abort(404, message=f"Menu item {item_id} doesn't exist", details={})
        return item

    def get(self, item_id: int):
        with self.UOWClass() as uow:
            item = self._get_item(item_id, uow=uow)
            return self.__schema.dump(item), 200

    def put(self, item_id):
        with self.UOWClass() as uow:
            item = self._get_item(item_id, uow=uow)

            item, error = menu_service.update_menu_item(item, request.json, uow=uow)
            if error:
                return {'message': str(error), 'details': error.details}, 403

            return self.__schema.dump(item), 201


class AddOnList(BaseAPIResource):

    def __init__(self) -> None:
        super().__init__()
        self.__plural_schema = model.AddOnSchema(many=True)

    def get(self):
        """List all of the addons"""
        with self.UOWClass() as uow:
            addons = menu_service.list_addons(uow)
            return self.__plural_schema.dump(addons), 200


class AddOnResource(BaseAPIResource):

    def __init__(self) -> None:
        super().__init__()
        self.__schema = model.AddOnSchema()

    @staticmethod
    def _get_item(item_id: int, uow) -> model.AddOn:
        item = menu_service.get_addon(item_id, uow=uow)
        if not item:
            abort(404, message=f"AddOn {item_id} doesn't exist", details={})
        return item

    def get(self, item_id: int):
        with self.UOWClass() as uow:
            item = self._get_item(item_id, uow)
            return self.__schema.dump(item), 200

    def put(self, item_id):
        with self.UOWClass() as uow:
            item = self._get_item(item_id, uow)

            item, error = menu_service.update_addon(item, request.json, uow=uow)
            if error:
                return {'message': str(error), 'details': error.details}, 403

            return self.__schema.dump(item), 201
