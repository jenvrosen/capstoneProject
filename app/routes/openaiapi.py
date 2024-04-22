from flask import Blueprint, request, jsonify, request, url_for, session
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from .. import db
from app.models.model import Course, CoursePrerequisite
from ..models.model import User, Course, TakenCourse, Plan, PlanCourse, CoursePrerequisite
import pyrebase

home_blueprint = Blueprint('home', __name__)

print("OpenAi-API INTIALIZED")

load_dotenv()

client = OpenAI(api_key="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") # Had to add api_key=' *our api key* ' in parenthensis to get code to run but had to remove it or it wouldent let me push


def format_courses(courses):
    formatted_courses = []
    for course in courses:
        formatted_course = f"{course.title}\n{course.description}"
        formatted_courses.append(formatted_course)
    return "\n\n".join(formatted_courses)


def format_prompt(id, prompt):
    user = User.query.filter_by(userID=id).first()
    academic_year = None

    if user.studentYear == 1:
        academic_year = '1st Year - Freshman'
    elif user.studentYear == 2:
        academic_year = '2nd Year - Sophomore'
    elif user.studentYear == 3:
        academic_year = '3rd Year - Junior'
    elif user.studentYear == 4:
        academic_year = '4th Year - Senior'
    else:
        academic_year = '5th+ Year'

    course_history = TakenCourse.query.filter_by(userID=id).all()
    formatted_course_history =  "\n".join([course.courseName for course in course_history])

    return f"{prompt}\n\nI am a {academic_year}.\n\nI have taken these courses:\n{formatted_course_history}"


@home_blueprint.route('/home/openai', methods=['POST'])
def sendPrompt():
    data = request.json
    prompt = data.get('prompt')
    user_id = session.get('user_id')  # Get the user ID from the session !!!!!!!

    print("OpenAI-API connected: ") # Test User ID !!!!!!!
    print(user_id)

    courses = format_courses(Course.query.all())
    print(courses)
    # prerequisites = CoursePrerequisite.query.all()  # Fetch all prerequisites
    
    formatted_prompt = format_prompt(user_id, prompt)
    print(formatted_prompt)

    # passID = some_function_that_requires_user_id(prompt, user_id) #Connect user ID to routes of fucntions where needed as such

    output = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": f"You are a counselor for the University of California, Merced. As a counselor, you will provide the user academic and career guidance charactericstic of your role. When the user asks you to recommend courses or provide a course plan, you will provide a personalized course plan based on their course history and preferences (if specified) containing course recommendations up until their 4th year in university. This course plan should be in a list format, ordered by semester.\n\n When providing a course plan, you should only select courses that exist within the provided course catalog. If prerequisites are not met, make sure to include those in the plan as well. Do not recommend courses that you have already provided in a prior course plan.\n\n Course Catalog\n{courses}"},
            {"role": "user", "content": formatted_prompt}
            
        ],
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    result = output.choices[0].message.content
    return result