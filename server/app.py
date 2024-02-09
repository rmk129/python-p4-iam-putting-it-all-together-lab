#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
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
    def get(self):
        recipes = []
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            for recipe in Recipe.query.all():
                if user.id == recipe.user_id:
                    add_recipe = {
                        'title': recipe.title,
                        'instructions': recipe.instructions,
                        'minutes_to_complete': recipe.minutes_to_complete
                    }
                    recipes.append(add_recipe)
            
            # recipes.append(user)
            return make_response(recipes, 200)
        else:
            return {}, 401
        

    def post(self):
        # Check if the user is logged in
        if not session.get('user_id'):
            return {'error': 'Unauthorized'}, 401

        # Get the logged in user
        user = User.query.filter(User.id == session.get('user_id')).first()

        # Get the request JSON data
        data = request.get_json()


        # Create a new recipe
        try:
            new_recipe = Recipe(
                title=data['title'],
                instructions=data['instructions'],
                minutes_to_complete=data['minutes_to_complete'],
                user_id=user.id
            )

            db.session.add(new_recipe)
            db.session.commit()

            # Return the response
            response_data = {
                'title': new_recipe.title,
                'instructions': new_recipe.instructions,
                'minutes_to_complete': new_recipe.minutes_to_complete,
                'user': {
                    'username': user.username,
                    'bio': user.bio,
                    'image_url': user.image_url
                }
            }

            return response_data, 201
        
        except IntegrityError:
            # Handle any integrity constraint violations (e.g., duplicate username)
            db.session.rollback()
            return {'error': 'Username already exists'}, 422



    





api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)