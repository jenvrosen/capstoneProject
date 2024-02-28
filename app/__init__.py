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
