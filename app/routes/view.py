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

#Render log in page
@view_blueprint.route('/', methods=['POST','GET'])
def login():
    if('user' in session):
        return redirect(url_for('view.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        # print(email)
        password = request.form.get('password')
        # print(password)
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            session['user'] = email
            return redirect(url_for('view.home'))
        except:
            return 'Failed to login'
    return render_template('login.html', hideNavigation=True)

@view_blueprint.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = email
            return redirect(url_for('view.home'))  # Redirect to home after successful sign up
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
    return render_template('home.html', hideNavigation=False) 

@view_blueprint.route('/signout')
def sign_out():
    session.pop('user', None)  # Clear the 'user' session data
    return redirect(url_for('view.login'))  # Redirect to login page after sign out