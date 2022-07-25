from flask import request
from flask_restful import abort
from marshmallow import ValidationError

from . import BaseAPIResource

from ...domain import model
from ...service_layer import menu as menu_service
from ...service_layer.unit_of_work import AbstractUnitOfWork


class OrdersCreate(BaseAPIResource):

    def __init__(self) -> None:
        self.__schema = model.OrderSchema()

    def post(self):
        """Create a new Order.

        This is the big one which is the result of a user placing a new order on our website or
        mobile app. Many things need to occur behind the scenes which is wrapped up in the menu
        service's `create_new_order`.

        Returns:
            tuple: (dictionary representation of a new order or error, integer http code)
        """
        with self.UOWClass() as uow:
            try:
                order: model.Order = self.__schema.load(request.json)
            except ValidationError as error:
                abort(400, message="Invalid order payload", details=error.messages)

            new_order, error = menu_service.create_new_order(
                order=order,
                uow=uow,
            )
            if error:
                return {'message': str(error), 'details': error.details}, 400

            return self.__schema.dump(new_order), 201


class OrdersList(BaseAPIResource):

    def __init__(self) -> None:
        super().__init__()
        self.__schema = model.OrderSchema(many=True)

    def get(self, status):
        with self.UOWClass() as uow:
            if status == 'new':
                items = menu_service.list_new_orders(uow)
            elif status == 'ready':
                items = menu_service.list_ready_for_pickup_orders(uow)
            else:
                abort(400, message=f"Invalid status {status}")

            return self.__schema.dump(items), 200


class OrderResource(BaseAPIResource):

    def __init__(self) -> None:
        super().__init__()
        self.__schema = model.OrderSchema()

    @staticmethod
    def _get_item(item_id: int, uow: AbstractUnitOfWork) -> model.Order:
        item = menu_service.get_order(item_id, uow=uow)
        if not item:
            abort(404, message=f"Order {item_id} doesn't exist", details={})
        return item

    def get(self, item_id: int):
        """Get a single Order item

        Args:
            item_id (int): The order id

        Returns:
            dict: The dictionary representation of an Order
        """
        with self.UOWClass() as uow:
            item = self._get_item(item_id, uow)
            return self.__schema.dump(item), 200

    def put(self, item_id: int):
        """Update a single order

        Args:
            item_id (int): The order id

        Returns:
            dict: The dictionary representation of an Order
        """
        with self.UOWClass() as uow:
            item = self._get_item(item_id, uow)

            schema = model.UpdateOrderSchema()
            try:
                data = schema.load(request.json)
            except ValidationError as error:
                abort(400, message="Invalid payload to update order", details=error.messages)

            item, error = menu_service.update_order_status(item, data['status'], uow=uow)
            if error:
                return {'message': str(error), 'details': error.details}, 400

            return self.__schema.dump(item), 200
