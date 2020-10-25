from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from inz.config import DevelopmentConfig
from flask_cors import CORS

# config
app = Flask('inz')
app.config.from_object(DevelopmentConfig())

CORS(app)
api = Api(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from inz.endpoints import auth_endpoints  # noqa: E402, F401
from inz.endpoints import ocr_endpoints  # noqa: E402, F401
from inz.endpoints import expense_endpoints  # noqa: E402, F401
