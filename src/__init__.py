from config import Config
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .orm import start_mappers
from .routes import connect_routes

# from adapters.repository import SqlAlchemyRepository

start_mappers()

app = Flask(__name__)
app.config.from_object(Config)

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# from . import models
# from .routes import api
get_session = sessionmaker(bind=create_engine(app.config['SQLALCHEMY_DATABASE_URI']))

connect_routes()
