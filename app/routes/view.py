#Routes of app that render HTML templates
from flask import Blueprint, render_template, redirect, url_for, session, request
from app.models.model import Course, CoursePrerequisite
from .. import db
from app.models.model import User, TakenCourse
from .decorators import admin_required, login_required
import pyrebase

view_blueprint = Blueprint('view', __name__)

config = {  # This is the information needed to connect to the firebase server


    'apiKey': "AIzaSyAaaVNdt8QoyJfRmxAc5ogd5IFncTXRuao",
    'authDomain': "cse120-group323.firebaseapp.com",
    'projectId': "cse120-group323",
    'storageBucket': "cse120-group323.appspot.com",
    'messagingSenderId': "356547945279",
    'appId': "1:356547945279:web:f876baec35884f4fb0698a",
    'measurementId': "G-F6LHBSHYYE",
    'databaseURL':''


}

firebase = pyrebase.initialize_app(config) #Used to intialize firebase connection
auth = firebase.auth()

# info = auth.get_account_info(user['idToken']) # Used to print user info in the console
# print("OPENAI-API CONNECTED: ")
# print(info)

# Render login page
@view_blueprint.route('/', methods=['POST', 'GET'])
def login():
    if 'user' in session:
        return redirect(url_for('view.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            # Retrieve user_id and store it in the session
            info = auth.get_account_info(user['idToken'])
            user_id = info['users'][0]['localId']
            session['user_id'] = user_id  # Store user_id in the session
            print("User ID:", user_id)
            return redirect(url_for('view.home'))
        except:
            return 'Failed to login'
    return render_template('login.html', hideNavigation=True)


@view_blueprint.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        try:
            # Check if the user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return 'User already exists'
            
            # Create a new user record
            new_user = User(
                email=email,
                firstName=first_name,
                lastName=last_name,
                studentYear=1,  # Set default student year, adjust as needed
                isAdmin=False   # Set default admin status, adjust as needed
            )
            
            # Add the Firebase UserID to the User record
            user = auth.create_user_with_email_and_password(email, password)
            firebase_user_id = user['localId']
            new_user.userID = firebase_user_id
            
            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            
            # Log in the user after successful signup
            session['user'] = email
            session['user_id'] = firebase_user_id
            
            return redirect(url_for('view.home'))
        except Exception as e:
            print(e)
            return 'Failed to sign up'
    return render_template('signup.html', hideNavigation=True)

# Render the Administrator page
@view_blueprint.route('/admin_page')
@login_required
@admin_required
def admin():
    courses = Course.query.all()  # Fetch all courses
    prerequisites = CoursePrerequisite.query.all()  # Fetch all prerequisites
    return render_template('admin.html', courses=courses, prerequisites=prerequisites, hideNavigation=False)



# Render the Profile page
@view_blueprint.route('/myprofile')
@login_required
def my_profile():
    user_id = session.get('user_id')  # Retrieve Firebase userID from session
    if not user_id:
        # Handle case where user is not logged in
        return redirect(url_for('auth.login'))  # Redirect to login page or handle appropriately

    # Fetch the user's taken courses and course history from the database
    taken_courses = TakenCourse.query.filter_by(userID=user_id).all()
    course_history = []  # You need to fetch this data from wherever it is stored in your database

    print("Taken courses:", taken_courses)  # Debug print

    # Pass the taken courses and course history data to the template
    return render_template('myprofile.html', taken_courses=taken_courses, courseHistory=course_history, hideNavigation=False)




# #Render the Search results page
@view_blueprint.route('/search_results')
@login_required
def search_courses():
    search_term = request.args.get('search', '')
    matching_courses = Course.query.filter(Course.title.like(f'%{search_term}%')).all()
    return render_template('search_results.html', courses=matching_courses, search_term=search_term)

# #Render page for Assigning prereqs
@view_blueprint.route('/assign_prerequisite')
@login_required
def assign_prerequisite():
    courses = Course.query.all()  # Fetch all courses to select from
    return render_template('assign_prerequisite.html', courses=courses)


# #Render the Create course page
@view_blueprint.route('/create_course')
@login_required
def create_course():
    return render_template('create_course.html')





#Render the Edit course page
@view_blueprint.route('/edit_course/<int:course_id>')
def edit_course(course_id):
    course = Course.query.get_or_404(course_id) 
    return render_template('edit_course.html', course=course)  


# Render the Home page
@view_blueprint.route('/home')
def home():
    user_id = session.get('user_id')  # Retrieve user_id from session
    print("User ID:", user_id)
    return render_template('home.html', hideNavigation=False) 



# Logout
@view_blueprint.route('/signout')
def sign_out():
    session.pop('user', None)
    session.pop('user_id', None)  # Clear user_id from session
    return redirect(url_for('view.login'))