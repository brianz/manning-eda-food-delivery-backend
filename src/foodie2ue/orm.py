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

from .config import POSTGRES_DATABASE_URI
from .domain.model import AddOn, MenuItem
from .utils import utcnow

get_session = sessionmaker(bind=create_engine(POSTGRES_DATABASE_URI))

mapper_registry = registry()

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
    Index('unique_name_and_size', 'name', 'size', unique=True))

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
    Column('menuitem_id', Integer, ForeignKey('menuitems.id')),
)


def start_mappers():
    mapper_registry.map_imperatively(
        MenuItem,
        menuitems,
        properties={
            'addons': relationship(AddOn, backref='menuitem', order_by=addons.c.id),
        },
    )
    mapper_registry.map_imperatively(AddOn, addons)
