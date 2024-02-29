#API for DB, CRUD operations
from flask import Blueprint, request, jsonify
from .. import db
from ..models.model import User

dbapi_blueprint = Blueprint('dbapi', __name__)

# Get all users
@dbapi_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Get a single user by ID
@dbapi_blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# Create a new user
@dbapi_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(
        email=data['email'], 
        hashedpassword=data['hashedpassword'], 
        firstName=data['firstName'], 
        lastName=data['lastName'], 
        studentYear=data['studentYear'],
        isAdmin=data.get('isAdmin', False)
        )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# Update a user
@dbapi_blueprint.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.email = data['email']
    user.hashedpassword = data['hashedpassword']
    ...
    db.session.commit()
    return jsonify(user.to_dict())

# Delete a user
@dbapi_blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
