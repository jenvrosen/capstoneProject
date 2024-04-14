from flask import Blueprint, request, jsonify, request, url_for, session
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from .. import db
from ..models.model import User, Course, TakenCourse, Plan, PlanCourse, CoursePrerequisite
import pyrebase

home_blueprint = Blueprint('home', __name__)

print("OpenAi-API INTIALIZED")

load_dotenv()

client = OpenAI() # Had to add api_key=' *our api key* ' in parenthensis to get code to run but had to remove it or it wouldent let me push

@home_blueprint.route('/home/openai', methods=['POST'])
def sendPrompt():
    data = request.json
    prompt = data.get('prompt')
    user_id = session.get('user_id')  # Get the user ID from the session !!!!!!!

    print("OpenAI-API connected: ") # Test User ID !!!!!!!
    print(user_id)

    # passID = some_function_that_requires_user_id(prompt, user_id) #Connect user ID to routes of fucntions where needed as such

    output = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "You are a counselor for the University of California, Merced. You will provide users with a personalized course plan in a list format based on their course history and preferences (if specified).\n\nYou should only pull courses from the provided 'Course Catalog.txt'."},
            {"role": "user", "content": prompt}
            
        ],
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    result = output.choices[0].message.content
    return result