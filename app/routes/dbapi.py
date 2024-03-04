#API for DB, CRUD operations
from flask import Blueprint, request, jsonify
from .. import db
from ..models.model import User, Course, TakenCourse, Plan, PlanCourse, CoursePrerequisite

dbapi_blueprint = Blueprint('dbapi', __name__)

### Users Crud operations

# Get all users
@dbapi_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Get a single user by ID
@dbapi_blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

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
    return jsonify(user.to_dict())

# Delete a user
@dbapi_blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204


### 
# Insert Course, TakenCourse, Plan, PlanCourse operations here
###


### CoursePrerequisite operations
# Get all course prerequisites
@dbapi_blueprint.route('/course_prerequisites', methods=['GET'])
def get_course_prerequisites():
    prerequisites = CoursePrerequisite.query.all()
    return jsonify([prerequisite.to_dict() for prerequisite in prerequisites])

# Get a single course prerequisite by ID
@dbapi_blueprint.route('/course_prerequisites/<int:id>', methods=['GET'])
def get_course_prerequisite(id):
    prerequisite = CoursePrerequisite.query.get_or_404(id)
    return jsonify(prerequisite.to_dict())

# Create a new course prerequisite
@dbapi_blueprint.route('/course_prerequisites', methods=['POST'])
def create_course_prerequisite():
    data = request.json
    prerequisite = CoursePrerequisite(
        courseID=data['courseID'],
        prerequisiteCourseID=data['prerequisiteCourseID']
    )
    db.session.add(prerequisite)
    db.session.commit()
    return jsonify(prerequisite.to_dict()), 201

# Update a course prerequisite
@dbapi_blueprint.route('/course_prerequisites/<int:id>', methods=['PUT'])
def update_course_prerequisite(id):
    prerequisite = CoursePrerequisite.query.get_or_404(id)
    data = request.json
    prerequisite.courseID = data.get('courseID', prerequisite.courseID)
    prerequisite.prerequisiteCourseID = data.get('prerequisiteCourseID', prerequisite.prerequisiteCourseID)
    db.session.commit()
    return jsonify(prerequisite.to_dict())

# Delete a course prerequisite
@dbapi_blueprint.route('/course_prerequisites/<int:id>', methods=['DELETE'])
def delete_course_prerequisite(id):
    prerequisite = CoursePrerequisite.query.get_or_404(id)
    db.session.delete(prerequisite)
    db.session.commit()
    return '', 204

