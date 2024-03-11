from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['text']

        output = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
              {"role": "system", "content": "You are a counselor for the University of California, Merced. You will provide users with a personalized course plan in a list format based on their course history and preferences (if specified).\n\nYou should only pull courses from the provided 'Course Catalog.txt'."},
              {"role": "user", "content": prompt}
              
           ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        result = output.choices[0].message
        return render_template('index.html', result=result)
    return render_template('index.html')


if __name__ == "__app__":
    app.run()