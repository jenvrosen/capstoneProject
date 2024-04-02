#__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Set the secret key to enable session support and secure cookies


# Initialize the Flask application
app = Flask(__name__)


# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Initialize the database with the app configuration
db = SQLAlchemy(app)

# Importing models to ensure they are known to SQLAlchemy
from app.models.model import User, Course, TakenCourse, Plan, PlanCourse, CoursePrerequisite

# Importing DB routes/blueprints
from .routes.dbapi import dbapi_blueprint
app.register_blueprint(dbapi_blueprint, url_prefix='/dbapi')

from .routes.openaiapi import home_blueprint
app.register_blueprint(home_blueprint)

# Importing front end routes/blueprints
from app.routes.view import view_blueprint