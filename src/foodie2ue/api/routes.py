from flask import json, make_response
from flask_restful import Api

from .resources import drivers, orders, menu


def connect_routes(app):
    api = Api(app)

    @api.representation('application/json')
    def output_json(data, code, headers=None):
        resp = make_response(json.dumps(data), code)
        resp.headers.extend(headers or {})
        return resp

    # Menu service routes
    api.add_resource(menu.MenuItemsListCreate, '/menuitems')
    api.add_resource(menu.MenuItemResource, '/menuitems/<item_id>')
    api.add_resource(menu.MenuItemAddOnListCreate, '/menuitems/<item_id>/addons')

    api.add_resource(menu.AddOnList, '/addons')
    api.add_resource(menu.AddOnResource, '/addons/<item_id>')

    # Order service routes
    api.add_resource(orders.OrdersCreate, '/orders')
    api.add_resource(orders.OrderResource, '/orders/<int:item_id>')
    api.add_resource(orders.OrdersList, '/orders/<status>')

    # Driver service routes
    api.add_resource(drivers.DriversListCreate, '/drivers')
