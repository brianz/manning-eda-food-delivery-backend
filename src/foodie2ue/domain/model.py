from decimal import Decimal
from typing import List, Optional
from marshmallow import Schema, ValidationError, fields, post_load

from ..utils import utcnow


class InvalidItemException(Exception):
    pass


# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")


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


# Schemas


class BaseSchema(Schema):
    id = fields.Int(dump_only=True)
    created = fields.DateTime(dump_default=utcnow)
    updated = fields.DateTime(dump_default=utcnow, dump_only=True)


class AddOnSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    size = fields.Str()
    price = fields.Number(as_string=True)

    @post_load
    def make_item(self, data, **kwargs):
        return AddOn(**data)


class MenuItemSchema(BaseSchema):
    name = fields.Str()
    description = fields.Str()
    size = fields.Str()
    price = fields.Number(as_string=True)
    addons = fields.List(fields.Nested(AddOnSchema))

    @post_load
    def make_item(self, data, **kwargs):
        return MenuItem(**data)


class CustomerSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    phone_number = fields.Str()
    email = fields.Str()
    address = fields.Str()
    city = fields.Str()
    state = fields.Str()
    zip = fields.Str()


class OrderAddOnSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class OrderItemSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    addons = fields.List(fields.Nested(OrderAddOnSchema))


class OrderSchema(BaseSchema):
    customer = fields.Nested(CustomerSchema)
    items = fields.List(fields.Nested(OrderItemSchema))
    tax = fields.Number(as_string=True)
    delivery_fee = fields.Number(as_string=True)
    subtotal = fields.Number(as_string=True)

    @post_load
    def make_item(self, data: dict, **kwargs):
        return Order(**data)


class DriverSchema(BaseSchema):
    first_name = fields.Str()
    last_name = fields.Str()
    phone_number = fields.Str()

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