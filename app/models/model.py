from app import app
from datetime import datetime
from .. import db

class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashedpassword = db.Column(db.String(128), nullable=False)
    firstName = db.Column(db.String(64), nullable=False)
    lastName = db.Column(db.String(64), nullable=False)
    studentYear = db.Column(db.Integer, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'userID': self.userID,
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'studentYear': self.studentYear,
            'isAdmin': self.isAdmin
        }

class Course(db.Model):
    courseID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TakenCourse(db.Model):
    takenCourseID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    courseID = db.Column(db.Integer, db.ForeignKey('course.courseID'), nullable=False)
    semesterTaken = db.Column(db.String(255), nullable=False)

class Plan(db.Model):
    planID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    planName = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

class PlanCourse(db.Model):
    planCourseID = db.Column(db.Integer, primary_key=True)
    planID = db.Column(db.Integer, db.ForeignKey('plan.planID'), nullable=False)
    courseID = db.Column(db.Integer, db.ForeignKey('course.courseID'), nullable=False)
    semesterRecommended = db.Column(db.String(255), nullable=False)

class CoursePrerequisite(db.Model):
    prerequisiteID = db.Column(db.Integer, primary_key=True)
    courseID = db.Column(db.Integer, db.ForeignKey('course.courseID'), nullable=False)
    prerequisiteCourseID = db.Column(db.Integer, db.ForeignKey('course.courseID'), nullable=False)

with app.app_context():
    db.create_all()