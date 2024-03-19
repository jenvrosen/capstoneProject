#Routes of app that render HTML templates
from flask import Blueprint, render_template, redirect, url_for
from app.models.model import Course, CoursePrerequisite

view_blueprint = Blueprint('view', __name__)

#Render log in page
@view_blueprint.route('/')
def login():
    return render_template('login.html', hideNavigation=True)

# Render the Administrator page
@view_blueprint.route('/signup')
def signup():
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
    # Add sign out logic here
    return redirect(url_for('view.login')) 
