#The entry point to run your Flask application.from app import app
from app import app

if __name__ == '__main__':
    app.run(debug=True)