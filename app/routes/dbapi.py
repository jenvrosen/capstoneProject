#dbapi.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from .. import db
from ..models.model import User, Course, TakenCourse, Plan, PlanCourse, CoursePrerequisite

dbapi_blueprint = Blueprint('dbapi', __name__)



### --- Users Crud operations --- ###



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
        #hashedpassword=data['hashedpassword'], 
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



###  --- Course Crud Operations --- ###



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

#### --- TEST --- ####
@dbapi_blueprint.route('/courses/search', methods=['GET'])
def search_courses():
    search_term = request.args.get('search', '')
    matching_courses = Course.query.filter(Course.title.like(f'%{search_term}%')).all()
    return jsonify([course.to_dict() for course in matching_courses]), 200


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



### --- Taken Course CRUD Operations --- ###



# Create a new taken course
@dbapi_blueprint.route('/taken-courses', methods=['POST'])
def add_taken_course():
    data = request.get_json()
    new_taken_course = TakenCourse(
        userID=data['userID'],
        courseID=data['courseID'],
        semesterTaken=data['semesterTaken']
    )
    db.session.add(new_taken_course)
    db.session.commit()
    return jsonify(new_taken_course.to_dict()), 201

# Get all taken courses
@dbapi_blueprint.route('/taken-courses', methods=['GET'])
def get_taken_courses():
    taken_courses = TakenCourse.query.all()
    return jsonify([taken_course.to_dict() for taken_course in taken_courses]), 200

# Get Taken course by ID
@dbapi_blueprint.route('/taken-courses/<int:taken_course_id>', methods=['GET'])
def get_taken_course(taken_course_id):
    taken_course = TakenCourse.query.get_or_404(taken_course_id)
    return jsonify(taken_course.to_dict()), 200

# Update taken course
@dbapi_blueprint.route('/taken-courses/<int:taken_course_id>', methods=['PUT'])
def update_taken_course(taken_course_id):
    taken_course = TakenCourse.query.get_or_404(taken_course_id)
    data = request.json
    taken_course.userID = data.get('userID', taken_course.userID)
    taken_course.courseID = data.get('courseID', taken_course.courseID)
    taken_course.semesterTaken = data.get('semesterTaken', taken_course.semesterTaken)
    db.session.commit()
    return jsonify(taken_course.to_dict()), 200

# Delete taken course
@dbapi_blueprint.route('/taken-courses/<int:taken_course_id>', methods=['DELETE'])
def delete_taken_course(taken_course_id):
    taken_course = TakenCourse.query.get_or_404(taken_course_id)
    db.session.delete(taken_course)
    db.session.commit()
    return jsonify({'message': 'TakenCourse deleted successfully'}), 204



### --- Plan CRUD Operations --- ###



# Create a new plan
@dbapi_blueprint.route('/plans', methods=['POST'])
def add_plan():
    data = request.get_json()

    if 'courses' not in data or not data['courses'].strip():
        return jsonify({'error': 'Courses cannot be empty'}), 400

    new_plan = Plan(
        userID=data['userID'],
        planName=data['planName'],
        courses=data['courses']
    )
    db.session.add(new_plan)
    db.session.commit()
    return jsonify(new_plan.to_dict()), 201

# Get all plans
@dbapi_blueprint.route('/plans', methods=['GET'])
def get_plans():
    plans = Plan.query.all()
    return jsonify([plan.to_dict() for plan in plans]), 200

# Get plan by ID
@dbapi_blueprint.route('/plans/<int:id>', methods=['GET'])
def get_plan(id):
    plan = Plan.query.get_or_404(id)
    return jsonify(plan.to_dict()), 200

# Update plan
@dbapi_blueprint.route('/plans/<int:id>', methods=['PUT'])
def update_plan(id):
    plan = Plan.query.get_or_404(id)
    data = request.json
    if 'courses' not in data or not data['courses'].strip():
        return jsonify({'error': 'Courses cannot be empty'}), 400

    plan.planName = data['planName']
    plan.courses = data['courses']
    db.session.commit()
    return jsonify(plan.to_dict()), 200

# Delete Plan
@dbapi_blueprint.route('/plans/<int:id>', methods=['DELETE'])
def delete_plan(id):
    plan = Plan.query.get_or_404(id)
    db.session.delete(plan)
    db.session.commit()
    return jsonify({'message': 'Plan deleted successfully'}), 204



### --- Plan Course CRUD Operations --- ###



# Create a new plan course
@dbapi_blueprint.route('/plan-courses', methods=['POST'])
def add_plan_course():
    data = request.get_json()
    new_plan_course = PlanCourse(
        planID=data['planID'],
        courseID=data['courseID'],
        semesterRecommended=data['semesterRecommended']
    )
    db.session.add(new_plan_course)
    db.session.commit()
    return jsonify(new_plan_course.to_dict()), 201

# Get all plan courses
@dbapi_blueprint.route('/plan-courses', methods=['GET'])
def get_plan_courses():
    plan_courses = PlanCourse.query.all()
    return jsonify([plan_course.to_dict() for plan_course in plan_courses]), 200

# Get plan course by ID
@dbapi_blueprint.route('/plan-courses/<int:id>', methods=['GET'])
def get_plan_course(id):
    plan_course = PlanCourse.query.get_or_404(id)
    return jsonify(plan_course.to_dict()), 200

# Update plan course
@dbapi_blueprint.route('/plan-courses/<int:id>', methods=['PUT'])
def update_plan_course(id):
    plan_course = PlanCourse.query.get_or_404(id)
    data = request.json
    plan_course.semesterRecommended = data['semesterRecommended']
    db.session.commit()
    return jsonify(plan_course.to_dict()), 200

# Delete plan course
@dbapi_blueprint.route('/plan-courses/<int:id>', methods=['DELETE'])
def delete_plan_course(id):
    plan_course = PlanCourse.query.get_or_404(id)
    db.session.delete(plan_course)
    db.session.commit()
    return jsonify({'message': 'PlanCourse deleted successfully'}), 204



### --- Course Prerequisites CRUD operations --- ###



# Create a new course prerequisite
#@dbapi_blueprint.route('/course-prerequisites', methods=['POST'])
#def add_course_prerequisite():
#    data = request.get_json()
#    new_course_prerequisite = CoursePrerequisite(
#        courseID=data['courseID'],
#        prerequisiteCourseID=data['prerequisiteCourseID']
#    )
#    db.session.add(new_course_prerequisite)
#    db.session.commit()
#    return jsonify(new_course_prerequisite.to_dict()), 201
@dbapi_blueprint.route('/course-prerequisites', methods=['POST'])
def add_course_prerequisite():
    data = request.get_json()
    course = Course.query.get(data['courseID'])
    prerequisite_course = Course.query.get(data['prerequisiteCourseID'])

    if not course or not prerequisite_course:
        return jsonify({'error': 'Course or prerequisite course not found'}), 404

    new_course_prerequisite = CoursePrerequisite(
        courseID=course.courseID,
        prerequisiteCourseID=prerequisite_course.courseID
    )
    db.session.add(new_course_prerequisite)
    db.session.commit()
    return jsonify(new_course_prerequisite.to_dict()), 201


# Get all course prerequisites
@dbapi_blueprint.route('/course-prerequisites', methods=['GET'])
def get_course_prerequisites():
    course_prerequisites = CoursePrerequisite.query.all()
    return jsonify([course_prerequisite.to_dict() for course_prerequisite in course_prerequisites]), 200

# Get course prerequisite by ID
@dbapi_blueprint.route('/courseprerequisites/<int:id>', methods=['GET'])
def get_course_prerequisite(id):
    course_prerequisite = CoursePrerequisite.query.get_or_404(id)
    return jsonify(course_prerequisite.to_dict()), 200

# Update course prerequisite
@dbapi_blueprint.route('/courseprerequisites/<int:id>', methods=['PUT'])
def update_course_prerequisite(id):
    course_prerequisite = CoursePrerequisite.query.get_or_404(id)
    data = request.json
    course_prerequisite.prerequisiteCourseID = data['prerequisiteCourseID']
    db.session.commit()
    return jsonify(course_prerequisite.to_dict()), 200

# Delete course prerequisite
@dbapi_blueprint.route('/courseprerequisites/<int:id>', methods=['DELETE'])
def delete_course_prerequisite(id):
    course_prerequisite = CoursePrerequisite.query.get_or_404(id)
    db.session.delete(course_prerequisite)
    db.session.commit()
    return jsonify({'message': 'CoursePrerequisite deleted successfully'}), 204