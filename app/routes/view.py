#Routes of app that render HTML templates
from flask import Blueprint, render_template, redirect, url_for, session, request
from app.models.model import Course, CoursePrerequisite
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
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = email
            # Retrieve user_id and store it in the session
            info = auth.get_account_info(user['idToken'])
            user_id = info['users'][0]['localId']
            session['user_id'] = user_id  # Store user_id in the session
            return redirect(url_for('view.home'))
        except:
            return 'Failed to sign up'
    return render_template('signup.html', hideNavigation=True)



# Render the Administrator page
@view_blueprint.route('/admin')
def admin():
    courses = Course.query.all()  # Fetch all courses
    prerequisites = CoursePrerequisite.query.all()  # Fetch all prerequisites
    return render_template('admin.html', courses=courses, prerequisites=prerequisites, hideNavigation=False)



# Render the Profile page
@view_blueprint.route('/myprofile')
def my_profile():
    return render_template('myprofile.html', hideNavigation=False) 



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