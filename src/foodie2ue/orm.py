from sqlalchemy import (Column, DateTime, ForeignKey, Integer, Numeric, String, Table, text)
from sqlalchemy.orm import registry, relationship

from .domain.model import MenuItem, MenuItemSchema
from .utils import utcnow

mapper_registry = registry()

# metadata = MetaData()

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
)

menuitems_addon = Table(
    "menuitem_addons",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("created", DateTime, nullable=False, server_default=text('NOW()')),
    Column("updated", DateTime, nullable=False, server_default=text('NOW()'), onupdate=utcnow),
    Column("name", String(64), unique=True),
    Column("description", String(256)),
    Column("price", Numeric(precision=4, scale=2), nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(MenuItemSchema, menuitems)

    # mapper_registry.map_imperatively(
    #     User,
    #     user,
    #     properties={'addons': relationship(MenuAddOn, backref='menuitem', order_by=menuitem.c.id)})
