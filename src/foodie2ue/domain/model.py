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
        print(kwargs)
        self.id = kwargs.get('id')
        self.created = kwargs.get('created')
        self.updated = kwargs.get('updated')
        self.name = kwargs['name']
        self.description = kwargs['description']
        self.size = kwargs.get('size')
        self.price = kwargs['price']

    def __repr__(self):
        return f"<MenuItem {self.name}>"


class AddOn:

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.description = kwargs.get('description', '')
        self.size = kwargs.get('size', '')
        self.price = kwargs['price']
        self.menuitem_id = kwargs['menuitem_id']


class AddOnSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    size = fields.Str()
    price = fields.Number(as_string=True)
    menuitem_id = fields.Int()

    @post_load
    def make_item(self, data, **kwargs):
        return AddOn(**data)


class MenuItemSchema(Schema):
    id = fields.Int(dump_only=True)
    created = fields.DateTime(dump_default=utcnow)
    updated = fields.DateTime(dump_default=utcnow, dump_only=True)
    name = fields.Str()
    description = fields.Str()
    size = fields.Str()
    price = fields.Number(as_string=True)
    addons = fields.List(fields.Nested(AddOnSchema))

    @post_load
    def make_item(self, data, **kwargs):
        return MenuItem(**data)


class Driver:

    def __init__(self, **kwargs):
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.phone_number = kwargs['phone_number']


class BaseSchema(Schema):
    id = fields.Int(dump_only=True)
    created = fields.DateTime(dump_default=utcnow)
    updated = fields.DateTime(dump_default=utcnow, dump_only=True)


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


# MenuItem: MenuItemSchema = MenuItemSchema()
# MenuItems: MenuItemSchema = MenuItemSchema(many=True)

# AddOn: AddOnSchema = AddOnSchema()
# AddOns: AddOnSchema = AddOnSchema(many=True)

# quote_schema = QuoteSchema()
# quotes_schema = QuoteSchema(many=True, only=("id", "content"))
