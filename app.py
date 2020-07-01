import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


dirname = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{dirname}/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask Restful
api = Api(app)

# SQLAlchemy
db = SQLAlchemy(app)

# Migrations
migrate = Migrate(app, db)

from models.location import Location # noqa
from resources.locations import LocationResource, LocationListResource # noqa


api.add_resource(LocationListResource, '/locations/')
api.add_resource(
    LocationResource, '/locations/', '/locations/<int:location_id>/')
