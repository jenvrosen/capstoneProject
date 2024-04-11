from flask import Blueprint, request, jsonify, request
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from .. import db
from ..models.model import User, Course, TakenCourse, Plan, PlanCourse, CoursePrerequisite

home_blueprint = Blueprint('home', __name__)

load_dotenv()

client = OpenAI()
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> parent of 8ae84e3 (Merged Firebase functionality)
=======
>>>>>>> parent of 8ae84e3 (Merged Firebase functionality)

@home_blueprint.route('/home/openai', methods=['POST'])
def sendPrompt():
    data = request.json
    prompt = data.get('prompt')

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