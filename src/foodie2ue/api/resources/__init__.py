from flask_restful import Resource

from ...service_layer.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork


class BaseAPIResource(Resource):
    UOWClass: AbstractUnitOfWork = SqlAlchemyUnitOfWork
