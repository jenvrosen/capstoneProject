#dbapi.py
from flask import Blueprint, request, jsonify, redirect, url_for, session
from datetime import datetime
from .. import db
from ..models.model import User, Course, TakenCourse, Plan, PlanCourse, CoursePrerequisite
from datetime import datetime
import pyrebase

dbapi_blueprint = Blueprint('dbapi', __name__)

print("DB-API INTIALIZED")

# I added the user_id implementation in Create user route in USERS section if your looking to reference it

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

    user_id = session.get('user_id')  # Include this in routes that need a user id and utlize "user_id" as such

    print("DB-API connected: ")
    print(user_id)

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
@dbapi_blueprint.route('/users/<string:id>', methods=['PUT'])
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

# Update a user semester
@dbapi_blueprint.route('/users/semester/<string:id>', methods=['PUT'])
def update_user_semester(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.studentYear = data.get('studentYear', user.studentYear)

    db.session.commit()
    return jsonify(user.to_dict()), 200

# Delete a user
@dbapi_blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return ({'message': 'User deleted successfully'}), 204

# Flask route to return user ID for the current session
@dbapi_blueprint.route('/get-user-id')
def get_user_id():
    user_id = session.get('user_id')
    return jsonify({'userID': user_id})

# Get user year
@dbapi_blueprint.route('/users/year/<string:id>', methods=['GET'])
def get_user_year(id):
    user = User.query.get_or_404(id)
    curr_term = user.studentYear

    return str(curr_term), 200  # Convert to string before returning



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

#### --- temp --- #### (Searching using UI)
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
    user_id = session.get('user_id')  # Retrieve user_id from session

    for course_data in data:
        new_taken_course = TakenCourse(
            userID=user_id,
            courseID=course_data['courseID'],
            courseName=course_data['courseName'],  # Add courseName attribute
            semesterTaken=course_data['semesterTaken']
        )

        db.session.add(new_taken_course)

    db.session.commit()

    return jsonify({'message': 'Taken courses added successfully.'}), 201

# Get all taken courses for the logged-in user
@dbapi_blueprint.route('/get-taken-courses', methods=['GET'])
def get_taken_courses():
    user_id = session.get('user_id')  # Retrieve Firebase userID from session
    if not user_id:
        return jsonify({'message': 'User not logged in.'}), 401

    taken_courses = TakenCourse.query.filter_by(userID=user_id).all()
    return jsonify([taken_course.to_dict() for taken_course in taken_courses]), 200

# Get Taken course by ID
@dbapi_blueprint.route('/taken-courses/<int:taken_course_id>', methods=['GET'])
def get_taken_course(taken_course_id):
    taken_course = TakenCourse.query.get_or_404(taken_course_id)
    return jsonify(taken_course.to_dict()), 200


# Update taken course
@dbapi_blueprint.route('/taken-courses', methods=['PUT'])
def update_taken_courses():
    data = request.get_json()
    user_id = session.get('user_id')  # Retrieve Firebase userID from session
    if not user_id:
        return jsonify({'message': 'User not logged in.'}), 401

    # Retrieve or create a user record based on the Firebase userID
    user = User.query.filter_by(userID=user_id).first()
    if not user:
        # Handle case where user record does not exist
        return jsonify({'message': 'User not found.'}), 404

    # Update or create taken courses for the user
    for course_id in data.get('courseIDs', []):
        # Check if the course is already taken by the user
        taken_course = TakenCourse.query.filter_by(userID=user.userID, courseID=course_id).first()
        if taken_course:
            # Update existing taken course
            taken_course.semesterTaken = data.get('semesterTaken')
        else:
            # Create new taken course
            taken_course = TakenCourse(userID=user.userID, courseID=course_id, semesterTaken=data.get('semesterTaken'))
            db.session.add(taken_course)

    db.session.commit()
    return jsonify({'message': 'Taken courses updated successfully.'}), 200

# Delete taken course
@dbapi_blueprint.route('/taken-courses/<int:taken_course_id>', methods=['DELETE'])
def delete_taken_course(taken_course_id):
    taken_course = TakenCourse.query.get_or_404(taken_course_id)
    db.session.delete(taken_course)
    db.session.commit()
    return jsonify({'message': 'TakenCourse deleted successfully'}), 204



### --- Plan CRUD Operations --- ###

@dbapi_blueprint.route('/plans', methods=['POST'])
def create_plan():
    data = request.json
    courses = data.get('courses')
    user_id = session.get('user_id')

    # Get the current date and time
    current_datetime = datetime.now()
    plan_name = current_datetime.strftime('%m-%d-%Y %H:%M')  # Format: YYYY-MM-DD HH:MM:SS

    # Save the plan to the database with the current date and time as the plan name
    plan = Plan(
        userID=user_id,
        planName=plan_name,
        courses=courses
    )
    db.session.add(plan)
    db.session.commit()

    return 'Plan saved successfully', 200

# # Create a new plan
# @dbapi_blueprint.route('/plans', methods=['POST'])
# def create_plan():
#     data = request.json
#     courses = data.get('courses')
#     user_id = session.get('user_id')

#     # Save the plan to the database
#     plan = Plan(
#         userID=user_id,
#         planName='',
#         courses=courses
#     )
#     db.session.add(plan)
#     db.session.commit()

#     return 'Plan saved successfully', 200

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
@dbapi_blueprint.route('/course-prerequisites', methods=['POST'])
def add_course_prerequisite():
    data = request.get_json()
    course_id = data.get('courseID')
    prerequisite_course_id = data.get('prerequisiteCourseID')

    if not course_id or not prerequisite_course_id:
        return jsonify({'error': 'Course ID and prerequisite Course ID are required'}), 400

    # Check if the course and the prerequisite course exist
    course = Course.query.get(course_id)
    prerequisite_course = Course.query.get(prerequisite_course_id)

    if not course or not prerequisite_course:
        return jsonify({'error': 'Course or prerequisite course not found'}), 404

    # Check if this prerequisite is already assigned
    existing_prerequisite = CoursePrerequisite.query.filter_by(courseID=course_id, prerequisiteCourseID=prerequisite_course_id).first()
    if existing_prerequisite:
        return jsonify({'message': 'This prerequisite is already assigned to the course'}), 409

    # If not already assigned, proceed with adding the new prerequisite
    new_course_prerequisite = CoursePrerequisite(courseID=course_id, prerequisiteCourseID=prerequisite_course_id)
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