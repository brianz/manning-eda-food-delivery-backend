from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Table,
    create_engine,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import registry, relationship, sessionmaker

from ..config import POSTGRES_DATABASE_URI, POSTGRES_CONNECTION_KWARGS
from ..domain.model import AddOn, MenuItem, Driver, Order
from ..utils import utcnow

get_session = sessionmaker(bind=create_engine(POSTGRES_DATABASE_URI, **POSTGRES_CONNECTION_KWARGS))

mapper_registry = registry()

# Menu items: burgers, cheeseburgers, fries, etc.
menuitems = Table(
    "menuitems",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("created", DateTime, nullable=False, server_default=text('NOW()')),
    Column("updated", DateTime, nullable=False, server_default=text('NOW()'), onupdate=utcnow),
    Column("name", String(64), nullable=False),
    Column("description", String(256)),
    Column("size", String(32), nullable=False, default=''),
    Column("price", Numeric(precision=4, scale=2), nullable=False),
    Index('unique_name_and_size', 'name', 'size', unique=True),
)

# add on items for menu items
addons = Table(
    "addons",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("created", DateTime, nullable=False, server_default=text('NOW()')),
    Column("updated", DateTime, nullable=False, server_default=text('NOW()'), onupdate=utcnow),
    Column("name", String(64), unique=True),
    Column("description", String(256)),
    Column("price", Numeric(precision=4, scale=2), nullable=False),
)

# Intermediate table for menu items/addon
menuitem_addons = Table(
    "menuitem_addons",
    mapper_registry.metadata,
    Column("menuitem_id", ForeignKey("menuitems.id"), primary_key=True),
    Column("addon_id", ForeignKey("addons.id"), primary_key=True),
)

orders = Table(
    "orders",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("created", DateTime, nullable=False, server_default=text('NOW()')),
    Column("updated", DateTime, nullable=False, server_default=text('NOW()'), onupdate=utcnow),
    Column("eta", DateTime),
    Column(
        "status",
        Enum(
            'NEW',
            'PREPARING',
            'READY_FOR_PICKUP',
            'ENROUTE',
            'DELIVERED',
            name='order_status_enum',
        ),
        default='NEW',
    ),
    Column("customer_first_name", String(64), nullable=False),
    Column("customer_last_name", String(64), nullable=False),
    Column("customer_phone_number", String(16), nullable=False),
    Column("customer_email", String(32), nullable=False),
    Column("customer_address", String(64), nullable=False),
    Column("customer_city", String(64), nullable=False),
    Column("customer_state", String(16), nullable=False),
    Column("customer_zip", String(16), nullable=False),
    Column("items", JSONB, nullable=False),
    Column("tax", Numeric(precision=6, scale=2), nullable=False),
    Column("delivery_fee", Numeric(precision=6, scale=2), nullable=False),
    Column("subtotal", Numeric(precision=8, scale=2), nullable=False),
)

drivers = Table(
    "drivers",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("created", DateTime, nullable=False, server_default=text('NOW()')),
    Column("updated", DateTime, nullable=False, server_default=text('NOW()'), onupdate=utcnow),
    Column("first_name", String(64), nullable=False),
    Column("last_name", String(64), nullable=False),
    Column("phone_number", String(16), unique=True, nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(
        MenuItem,
        menuitems,
        properties={
            'addons': relationship(
                AddOn,
                backref='menuitem',
                order_by=addons.c.id,
                secondary="menuitem_addons",
            ),
        },
    )
    mapper_registry.map_imperatively(AddOn, addons)
    mapper_registry.map_imperatively(Order, orders)
    mapper_registry.map_imperatively(Driver, drivers)
