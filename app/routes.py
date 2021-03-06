from app import db
from app.models.user import User
from flask import Blueprint, json, request, make_response, jsonify, render_template, url_for
from dotenv import load_dotenv
from flask_login import login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint("users", __name__)
load_dotenv()

@users_bp.route('/users', methods = ['GET'])
def all_users():


    users = User.query.all()
    users_response = []

    if users is None:
        return 404

    for user in users:
        users_response.append(user.to_json_user())

    return jsonify(users_response), 200

@users_bp.route('/users', methods = ['POST'])
def register():

    request_body = request.get_json()

    if request_body['first name'] == '' or request_body['last name'] == '' or request_body['birthday'] == '' or request_body['about me'] == '' or request_body['username'] == '' or request_body['password1'] == '' or request_body['password2'] == '':
        return jsonify({'Error': 'Enter info for all fields.'}), 400
    
    first_name = request_body['first name']
    last_name = request_body['last name']
    birthday = request_body['birthday']
    about_me = request_body['about me']
    username = request_body['username'].lower()
    # email = request_body['email']
    password1 = request_body['password1']
    password2 = request_body['password2']

    if password1 != password2: 
        return jsonify({'Error': 'Passwords do not match'}), 400


    username_exists = User.query.filter_by(username=username).first()

    if username_exists is None: 
        new_user = User(first_name=first_name, last_name=last_name, birthday=birthday, about_me=about_me, username=username, password1=generate_password_hash(password1, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        # login_user(new_user, remember=True)

        return jsonify(new_user.to_json_user()), 201
    else: 
        return jsonify({'Error': f'Username {username} already exists.'})

@users_bp.route('/users/<user_id>', methods = ['GET'])
def handle_user(user_id):
    

    user = User.query.get(user_id)

    if user is None:
        return jsonify({'Error': 'User not found.'}), 400

    else: 
        return jsonify(user.to_json_user()), 200

@users_bp.route('/users/<user_id>', methods = ['DELETE'])
def delete_user(user_id):
    
    user = User.query.get(user_id)

    if user is None:
        return jsonify({'Error': 'User not found'}), 400
    
    else: 
        db.session.delete(user)
        db.session.commit()
        return jsonify({'Success': f'User {user_id} deleted'}), 200

@users_bp.route('/users', methods = ['DELETE'])
def delete_all_users():

    users = User.query.all()
    users_response = []

    if users is None:
        return 404

    for user in users:
        db.session.delete(user)
        db.session.commit()

    return jsonify({'Success': 'All users deleted'}), 200

@users_bp.route('/login', methods = ['POST'])
def login():
    d = {}

    request_body = request.get_json()

    username = request_body['username']
    password = request_body['password1']

    user = User.query.filter_by(username=username).first()

    if user is None: 
        return jsonify({'Error': 'Username does not exist'}), 400
    else:
        if check_password_hash(user.password1, password):
            # login_user(user, remember=True)
            return jsonify({'Success': 'You are now logged in'}), 200
        else:
            return jsonify({'Error': 'Password is incorrect'}), 400

@users_bp.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    login_user()
    return jsonify({'Success': 'You are now logged out'})