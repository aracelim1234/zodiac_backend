# from flask.helpers import flash
# from flask.wrappers import Response
from app import db
from app.models.user import User
from flask import Blueprint, json, request, make_response, jsonify, render_template, url_for
# from datetime import datetime
from dotenv import load_dotenv
# import os
# import requests
from flask_login import login_user, logout_user, login_required, current_user
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, ValidationError
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

    if request_body['first name'] is '' or request_body['last name'] is '' or request_body['birthday'] is '' or request_body['username'] is '' or request_body['password'] is '':
        return jsonify({'Error': 'Enter info for all fields.'}), 400

    first_name = request_body['first name']
    last_name = request_body['last name']
    birthday = request_body['birthday']
    username = request_body['username'].lower()
    # email = request_body['email']
    password1 = request_body['password']
    # password2 = request_body['password2']

    # if password1 != password2: 
    #     return jsonify({'Error': 'Passowrds do not match'}), 400


    username_exists = User.query.filter_by(username=username).first()

    if username_exists is None: 
        new_user = User(first_name=first_name, last_name=last_name, birthday=birthday, username=username, password=generate_password_hash(password1, method='sha256'))
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

@users_bp.route('/login', methods = ['GET', 'POST'])
def login():
    d = {}

    request_body = request.get_json()

    username = request_body['username']
    password = request_body['password']

    user = User.query.filter_by(username=username).first()

    if user is None: 
        return jsonify({'Error': 'Username does not exist'}), 400
    else:
        if check_password_hash(user.password, password):
            # login_user(user, remember=True)
            return jsonify({'Success': 'You are now logged in'}), 200
        else:
            return jsonify({'Error': 'Password is incorrect'}), 400

@users_bp.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    login_user()
    return jsonify({'Success': 'You are now logged out'})