#__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

# Importing front end routes/blueprints
from app.routes.view import view_blueprint
app.register_blueprint(view_blueprint)