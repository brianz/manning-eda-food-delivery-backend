from flask import Flask

from .routes import connect_routes

from ..adapters import orm

orm.start_mappers()

app = Flask(__name__, template_folder="../templates")
app.config.from_prefixed_env()

connect_routes(app)
