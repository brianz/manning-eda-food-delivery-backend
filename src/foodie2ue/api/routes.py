import sched
from flask import request
from flask_restful import Api, Resource, abort

from ..domain import model
from ..service_layer import menu as menu_service
from ..service_layer.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork

# from marshmallow import ValidationError

# def abort_if_doesnt_exist(todo_id):
#     if todo_id not in TODOS:
#         abort(404, message="Todo {} doesn't exist".format(todo_id))


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
            menu_item_schema = model.MenuItemSchema()
            menu_item: model.MenuItem = menu_item_schema.load(request.json)

            (new_menu_item, error) = menu_service.create_new_menu_item(
                menu_item=menu_item,
                uow=uow,
            )
            if not error:
                return new_menu_item, 201

            return {'error': error}, 403


class AddOnList(BaseAPIResource):

    def get(self):
        with self.UOWClass() as uow:
            items = menu_service.list_addons(uow)
            schema = model.AddOnSchema(many=True)
            return schema.dump(items), 200

    def post(self):
        with self.UOWClass() as uow:
            schema = model.AddOnSchema()
            addon: model.AddOnSchema = schema.load(request.json)

            (new_addon, error) = menu_service.create_new_addon(addon=addon, uow=uow)
            if not error:
                return new_addon, 201

            return {'error': error}, 403


class MenuItemResource(BaseAPIResource):

    def get(self, item_id):
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

    # def delete(self, todo_id):
    #     abort_if_todo_doesnt_exist(todo_id)
    #     del TODOS[todo_id]
    #     return '', 204

    # def put(self, todo_id):
    #     args = parser.parse_args()
    #     task = {'task': args['task']}
    #     TODOS[todo_id] = task
    #     return task, 201


def connect_routes():
    from ..api import app
    api = Api(app)

    api.add_resource(MenuItemsList, '/menuitems')
    api.add_resource(MenuItemResource, '/menuitems/<item_id>')

    api.add_resource(AddOnList, '/addons')
