from flask import Flask

from .routes import connect_routes

from ..adapters import orm
from ..notifications import setup_mail

orm.start_mappers()

app = Flask(__name__, template_folder="../templates")
app.config.from_prefixed_env()

connect_routes(app)
setup_mail(app)
