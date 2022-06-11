from marshmallow import Schema, ValidationError, fields

from ..utils import utcnow


# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")


class MenuItemSchema(Schema):
    id = fields.Int(dump_only=True)
    created = fields.DateTime(dump_default=utcnow)
    updated = fields.DateTime(dump_default=utcnow, dump_only=True)
    name = fields.Str()
    description = fields.Str()
    size = fields.Str()
    price = fields.Number(as_string=True)

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


# class QuoteSchema(Schema):
#     id = fields.Int(dump_only=True)
#     author = fields.Nested(AuthorSchema, validate=must_not_be_blank)
#     content = fields.Str(required=True, validate=must_not_be_blank)
#     posted_at = fields.DateTime(dump_only=True)

#     # Allow client to pass author's full name in request body
#     # e.g. {"author': 'Tim Peters"} rather than {"first": "Tim", "last": "Peters"}
#     @pre_load
#     def process_author(self, data, **kwargs):
#         author_name = data.get("author")
#         if author_name:
#             first, last = author_name.split(" ")
#             author_dict = dict(first=first, last=last)
#         else:
#             author_dict = {}
#         data["author"] = author_dict
#         return data

MenuItem: MenuItemSchema = MenuItemSchema()
MenuItems: MenuItemSchema = MenuItemSchema(many=True)

# quote_schema = QuoteSchema()
# quotes_schema = QuoteSchema(many=True, only=("id", "content"))
