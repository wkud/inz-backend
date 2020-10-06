from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from inz.config import DevelopmentConfig

# config
app = Flask('inz')
app.config.from_object(DevelopmentConfig())

api = Api(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from inz.endpoints import auth_endpoints  # noqa: E402, F401
