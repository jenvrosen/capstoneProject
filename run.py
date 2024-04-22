from app import app
from app.routes.view import view_blueprint

# Set the secret key for session support and secure cookies
app.secret_key = 'secret'

app.register_blueprint(view_blueprint, name='view')

if __name__ == '__main__':
    app.run(debug=True)