from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    adminRole = db.Column(db.Boolean, default=False)
    studentYear = db.Column(db.Integer) 
    interest = db.Column(db.String(120))

# Course Model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    courseNumber = db.Column(db.String(20), nullable=False)
    prerequisites = db.Column(db.String(100))
    term = db.Column(db.String(50))
    editTimestamp = db.Column(db.DateTime)

# TakenCourses Model
class TakenCourses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #Many-to-One relationship with User model
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #Many-to-One relationship with Course model
    courseID = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

# JSONfile Model
class JSONfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(100), nullable=False)
    fileContent = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime)

# Plans Model
class Plans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #Many-to-One relationship with User
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planContent = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

# CoursesInPlans Model
class CoursesInPlans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #Many-to-One relationship with Plans
    planID = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    #Many-to-One relationship with Course
    courseID = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

db.create_all()


