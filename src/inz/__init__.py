from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from app.config import ProductionConfig

# config
app = Flask('inz')
# app.config.from_object(ProductionConfig())
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

api = Api(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from inz.endpoints import auth_endpoints