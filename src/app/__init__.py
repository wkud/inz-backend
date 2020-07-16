from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from app.config import ProductionConfig


# config
app = Flask('inz')
app.config.from_object(ProductionConfig())

api = Api(app)
db = SQLAlchemy(app)

from app.endpoints import user_controller