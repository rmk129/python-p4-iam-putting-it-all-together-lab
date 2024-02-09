#!/usr/bin/env python3

from flask import request, session, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        image_url = request.get_json().get('image_url')
        bio = request.get_json().get('bio')

        if not username or not password:
            return {'error': 'Username and password are required'}, 422

        try:
            user = User(username=username, image_url=image_url, bio=bio)
            user.password_hash = password
            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            response =  {
                'user_id': user.id,
                'username': user.username,
                'image_url': user.image_url,
                'bio': user.bio
            }, 201
            return response
        

        except IntegrityError:
            # Handle any integrity constraint violations (e.g., duplicate username)
            db.session.rollback()
            return {'error': 'Username already exists'}, 422


class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            response =  {
                'id': user.id,
                'username': user.username,
                'image_url': user.image_url,
                'bio': user.bio
            }, 200
            return response
        else:
            return {}, 401

class Login(Resource):
    def post(self):
        user = User.query.filter(
            User.username == request.get_json().get('username')
        ).first()

        if user and user.authenticate(request.get_json().get('password')) == True:
            session['user_id'] = user.id
            response =  {
                'id': user.id,
                'username': user.username,
                'image_url': user.image_url,
                'bio': user.bio
            }, 200
            return response
        else:
            return {}, 401


class Logout(Resource):
    def delete(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            session['user_id'] = None
            return {}, 204
        else:
            return {}, 401

class RecipeIndex(Resource):
    pass

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)