from sqlalchemy import Column, DateTime, Integer, text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declared_attr

from . import db
from .utils import class_name_to_underscores, utcnow


class BaseModelMixin:

    id = Column(Integer, primary_key=True)

    created = Column(
        DateTime,
        nullable=False,
        server_default=text('NOW()'),
    )
    updated = Column(
        DateTime,
        nullable=False,
        server_default=text('NOW()'),
        onupdate=utcnow,
    )

    @declared_attr
    def __tablename__(cls):
        name = class_name_to_underscores(cls.__name__)
        if not name.endswith('s'):
            name = f'{name}s'
        return name

    def save(self, *, commit=True, _raise=True):
        db.session.add(self)
        if commit:
            self._commit_session(_raise)

    def _commit_session(self, _raise):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            if _raise:
                raise

    # @classmethod
    # def flush(self):
    #     get_session().flush()


# class User(BaseModelMixin, db.Model):
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     phone_number = db.Column(db.String(128))
#     password_hash = db.Column(db.String(128))

#     def __repr__(self):
#         return f'<User {self.username}>'


class MenuItem(BaseModelMixin, db.Model):
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))
    size = db.Column(db.String(32))
    price = db.Column(db.Numeric(precision=4, scale=2))
    # addons = db.relationship('AddOn', backref='menuitem')

    __table_args__ = (db.Index(
        'unique_name_and_size',
        name,
        size,
        unique=True,
    ), )

    def __repr__(self):
        return f'<MenuItem {self.name}>'


class AddOn(BaseModelMixin, db.Model):
    menuitem = db.Column(db.Integer, db.ForeignKey(MenuItem.id), nullable=False)

    name = db.Column(db.String(64))
    description = db.Column(db.String(256))
    price = db.Column(db.Numeric(precision=4, scale=2))

    def __repr__(self):
        return f'<AddOn {self.name}>'
