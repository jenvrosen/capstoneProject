#API for DB, CRUD operations
from flask import Blueprint, request, jsonify
from datetime import datetime
from .. import db
from ..models.model import User, Course, TakenCourse, Plan, PlanCourse, CoursePrerequisite

dbapi_blueprint = Blueprint('dbapi', __name__)

### Users Crud operations

#/users is an endpoint of a specific path
#methods are actions to take at route (GET POST PUT DELETE)
# Get all users
@dbapi_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# Get a single user by ID
@dbapi_blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict()), 200

# Create a new user
@dbapi_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(
        email=data['email'], 
        hashedpassword=data['hashedpassword'], 
        firstName=data['firstName'], 
        lastName=data['lastName'], 
        studentYear=data['studentYear'],
        isAdmin=data['isAdmin']
        )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# Update a user
@dbapi_blueprint.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.email = data['email']
    user.hashedpassword = data['hashedpassword']
    user.firstName = data.get('firstName', user.firstName)
    user.lastName = data.get('lastName', user.lastName)
    user.studentYear = data.get('studentYear', user.studentYear)
    user.isAdmin = data.get('isAdmin', user.isAdmin)

    db.session.commit()
    return jsonify(user.to_dict()), 200

# Delete a user
@dbapi_blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return ({'message': 'User deleted successfully'}), 204


### Course Crud Operations

# Create a new course
@dbapi_blueprint.route('/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    new_course = Course(
        title=data['title'],
        description=data['description'],
        department=data['department']
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify(new_course.to_dict()), 201

# Get all courses
@dbapi_blueprint.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses]), 200

# Get a specific course by ID
@dbapi_blueprint.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify(course.to_dict()), 200

# Update a course
@dbapi_blueprint.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    course.title = data.get('title', course.title)
    course.description = data.get('description', course.description)
    course.department = data.get('department', course.department)
    course.updated = datetime.utcnow()
    db.session.commit()
    return jsonify(course.to_dict()), 200

# Delete a course
@dbapi_blueprint.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted successfully'}), 204

### 
# Insert TakenCourse, Plan, PlanCourse, CoursePrerequisite operations here
# Make sure route decorator says @dbapi_blueprint.route
###