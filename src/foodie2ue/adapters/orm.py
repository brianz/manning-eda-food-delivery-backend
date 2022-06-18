from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Table,
    create_engine,
    text,
)
from sqlalchemy.orm import registry, relationship, sessionmaker

from ..config import POSTGRES_DATABASE_URI, POSTGRES_CONNECTION_KWARGS
from ..domain.model import AddOn, MenuItem, Driver
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
    Column("name", String(64), unique=True),
    Column("description", String(256)),
    Column("size", String(32)),
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

menuitem_addons = Table(
    "menuitem_addons",
    mapper_registry.metadata,
    Column("menuitem_id", ForeignKey("menuitems.id"), primary_key=True),
    Column("addon_id", ForeignKey("addons.id"), primary_key=True),
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

    mapper_registry.map_imperatively(Driver, drivers)
