import os
import json

POSTGRES_DATABASE_URI = os.environ['FLASK_SQLALCHEMY_DATABASE_URI']
POSTGRES_CONNECTION_KWARGS = {
    'echo': json.loads(os.environ.get('FLASK_SQLALCHEMY_DATABASE_ECHO', 'true')),
}
