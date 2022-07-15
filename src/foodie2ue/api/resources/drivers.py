from flask import request, abort
from marshmallow import ValidationError

from . import BaseAPIResource

from ...domain import model
from ...service_layer import driver as driver_service


class DriversListCreate(BaseAPIResource):

    def __init__(self) -> None:
        super().__init__()
        self.__schema = model.DriverSchema()
        self.__plural_schema = model.DriverSchema(many=True)

    def get(self):
        """List all drivers"""
        with self.UOWClass() as uow:
            items = driver_service.list_drivers(uow)
            return self.__plural_schema.dump(items), 200

    def post(self):
        """Create a new driver"""
        with self.UOWClass() as uow:
            try:
                driver: model.Driver = self.__schema.load(request.json)
            except ValidationError as error:
                abort(400, message="Invalid driver payload", details=error.messages)

            (new_driver, error) = driver_service.create_driver(
                driver=driver,
                uow=uow,
            )
            if error:
                return {'message': str(error), 'details': error.details}, 400

            return self.__schema.dump(new_driver), 201
