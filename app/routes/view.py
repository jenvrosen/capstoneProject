#view.py
#Routes of app that render HTML templates
from flask import Blueprint, render_template, redirect, url_for, request
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

#Render the Search results page
@view_blueprint.route('/search_results')
def search_courses():
    search_term = request.args.get('search', '')
    matching_courses = Course.query.filter(Course.title.like(f'%{search_term}%')).all()
    return render_template('search_results.html', courses=matching_courses, search_term=search_term)

#Render page for Assigning prereqs
@view_blueprint.route('/assign_prerequisite')
def assign_prerequisite():
    courses = Course.query.all()  # Fetch all courses to select from
    return render_template('assign_prerequisite.html', courses=courses)


#Render the Create course page
@view_blueprint.route('/create_course')
def create_course():
    return render_template('create_course.html')


#Render the Edit course page
@view_blueprint.route('/edit_course/<int:course_id>')
def edit_course(course_id):
    course = Course.query.get_or_404(course_id) 
    return render_template('edit_course.html', course=course)  

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
