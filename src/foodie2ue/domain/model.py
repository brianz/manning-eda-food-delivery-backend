from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from marshmallow import Schema, fields, post_load, validate

from .tax_rates import get_tax_rate_by_zip
from ..constants import DELIVERY_STATUSES, ORDER_STATUSES, DRIVER_STATUSES
from ..utils import utcnow


class MenuItem:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.created = kwargs.get('created')
        self.updated = kwargs.get('updated')
        self.name: str = kwargs.get('name', '')
        self.description: str = kwargs.get('description', '')
        self.size = kwargs.get('size')
        self.price = kwargs.get('price')
        self.addons: List[AddOn] = kwargs.get('addons', [])

    def __repr__(self):
        return f"<MenuItem {self.id} - {self.name}>"


class AddOn:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs['name']
        self.description = kwargs.get('description', '')
        self.size = kwargs.get('size', '')
        self.price = kwargs['price']

    def __repr__(self):
        return f"<AddOn {self.id} - {self.name}>"


class MenuItemAddOn:

    def __init__(self, **kwargs):
        self.menuitem_id = kwargs['menuitem_id']
        self.addon_id = kwargs['addon_id']


class Order:

    def __init__(self, **kwargs) -> None:
        self.id: Optional[int] = kwargs.get('id')
        self.created: str = kwargs.get('created')
        self.updated: str = kwargs.get('updated')
        self.items: List[dict] = kwargs['items']

        _customer = kwargs['customer']
        self.customer_first_name: str = _customer['first_name']
        self.customer_last_name: str = _customer['last_name']
        self.customer_phone_number: str = _customer['phone_number']
        self.customer_email: str = _customer['email']
        self.customer_address: str = _customer['address']
        self.customer_city: str = _customer['city']
        self.customer_state: str = _customer['state']
        self.customer_zip: str = _customer['zip']

        self.tax: float = kwargs.get('tax', Decimal('0.0'))
        self.delivery_fee: float = kwargs.get('delivery_fee', Decimal('0.0'))
        self.subtotal: float = kwargs.get('subtotal', Decimal('0.0'))

        self._order_items: List[Order] = []
        self._addons: List[AddOn] = []

    def __repr__(self):
        return f"<Order {self.id} - {self.customer_first_name} {self.customer_last_name}>"

    @property
    def total(self) -> float:
        if not self.tax:
            self.tax = get_tax_rate_by_zip(self.customer_zip)
        return self.subtotal + self.tax + self.delivery_fee

    def add_item_to_order(self, item: MenuItem):
        self._order_items.append(item)
        self.subtotal += item.price

    def add_addon_to_order(self, item: AddOn):
        self._addons.append(item)
        self.subtotal += item.price


class Driver:

    def __init__(self, **kwargs):
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.phone_number = kwargs['phone_number']
        self.status = kwargs['status']


class DeliveryEvent:

    def __init__(self, **kwargs):
        self.id: int = kwargs.get('id')
        self.order_id: int = kwargs['order_id']
        self.driver_id: int = kwargs['driver_id']
        self.created: datetime = kwargs.get('created')
        self.updated: datetime = kwargs.get('updated')
        self.status: List[str] = kwargs['status']


# Schemas


class BaseSchema(Schema):
    id = fields.Int(dump_only=True)
    created = fields.DateTime(dump_default=utcnow)
    updated = fields.DateTime(dump_default=utcnow, dump_only=True)


class AddOnSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    size = fields.Str()
    price = fields.Number(as_string=True, required=True)

    @post_load
    def make_item(self, data, **kwargs):
        return AddOn(**data)


class MenuItemSchema(BaseSchema):
    name = fields.Str(required=True)
    description = fields.Str()
    size = fields.Str()
    price = fields.Number(as_string=True, required=True)
    addons = fields.List(fields.Nested(AddOnSchema))

    @post_load
    def make_item(self, data, **kwargs):
        return MenuItem(**data)


class CustomerSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    email = fields.Email(required=True)
    address = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    zip = fields.Str(required=True)


class OrderAddOnSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)


class OrderItemSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    size = fields.Str()
    addons = fields.List(fields.Nested(OrderAddOnSchema))


class OrderSchema(BaseSchema):
    customer = fields.Nested(CustomerSchema, required=True)
    items = fields.List(
        fields.Nested(OrderItemSchema),
        required=True,
        validate=validate.Length(min=1, error="Items must be added to an order"),
    )
    tax = fields.Number(as_string=True)
    delivery_fee = fields.Number(as_string=True)
    status = fields.Str()
    subtotal = fields.Number(as_string=True)
    total = fields.Number(as_string=True, dump_only=True)

    @post_load
    def make_item(self, data: dict, **kwargs):
        return Order(**data)


class UpdateOrderSchema(Schema):
    status = fields.Str(required=True, validate=validate.OneOf(ORDER_STATUSES))


class DriverSchema(BaseSchema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(DRIVER_STATUSES))

    @post_load
    def make_item(self, data, **kwargs):
        return Driver(**data)


class DeliveryEventSchema(BaseSchema):
    order_id = fields.Int()
    driver_id = fields.Int()
    status = fields.Str(required=True, validate=validate.OneOf(DELIVERY_STATUSES))

    # addons = fields.List(fields.Nested(AddOnSchema))

    @post_load
    def make_item(self, data, **kwargs):
        return DeliveryEvent(**data)

    # class Meta:
    #     unknown = marshmallow.EXCLUDE

    # def __repr__(self):
    #     return f"<Batch {self.reference}>"

    # def __eq__(self, other):
    #     if not isinstance(other, Batch):
    #         return False
    #     return other.reference == self.reference

    # def __hash__(self):
    #     return hash(self.reference)

    # def __gt__(self, other):
    #     if self.eta is None:
    #         return False
    #     if other.eta is None:
    #         return True
    #     return self.eta > other.eta

    # def allocate(self, line: OrderLine):
    #     if self.can_allocate(line):
    #         self._allocations.add(line)

    # def deallocate(self, line: OrderLine):
    #     if line in self._allocations:
    #         self._allocations.remove(line)

    # @property
    # def allocated_quantity(self) -> int:
    #     return sum(line.qty for line in self._allocations)
