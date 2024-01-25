# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.config import Config
from flask_jwt_extended import JWTManager
import secrets


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# register urls
from app.urls import user_urls, product_urls, auth_urls

# migrations
from flask_migrate import Migrate

# db = SQLAlchemy(app)
migrate = Migrate(app, db)

import os
from dotenv import load_dotenv
load_dotenv()
# app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)
