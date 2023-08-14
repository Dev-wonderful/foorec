#!/usr/bin/python3
from flask import Flask, render_template, request, session, jsonify, abort
from models.rating import Rating
from models.user import User
from models.recipe import Recipe
from uuid import uuid4
# from flask_session import Session
import requests
import models
storage = models.storage

app = Flask(__name__)
app.secret_key = str(uuid4())

SPOONACULAR_API_KEY = '8ca7176f9710474688667f16c6faee9e'


def get_recipes(ingredients):
    base_url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        'apiKey': SPOONACULAR_API_KEY,
        'ingredients': ','.join(ingredients),
        'number': 10  # Number of recipes to retrieve
    }

    try:
        response = requests.get(base_url, params=params)
        recipes = response.json()
        return recipes
    except ConnectionError:
        print('Connection Down, Check your Internet Connection')


@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = []

    if request.method == 'POST':
        ingredients = request.form['ingredients'].split(',')
        recipes = get_recipes(ingredients)

    return render_template('index.html', recipes=recipes)


@app.route('/login', methods=['POST'])
def login():
    user_id: str
    username = request.form.get('username')
    password = request.form.get('password')
    print(f'username: {username}, password: {password}')
    user_id = getattr(storage.get_user(username), 'id', None)
    if user_id is None:
        new_user = User(username=username, password=password)
        new_user.save()
        user_id = new_user.id
    session['user_id'] = user_id
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/rating', methods=['GET', 'POST'])
def rating():

    if request.method == 'POST':
        recipe_rating = request.json.get('rating')
        recipe_id = request.json.get('recipe_id')
        recipe_title = request.json.get('recipe_title')
        user_id = session.get('user_id')
        if user_id is None:
            abort(403)
        print(f'id: {recipe_id}, rating: {recipe_rating}, user_id: {user_id}')
        recipe_exist = storage.get(Recipe, recipe_id)
        if recipe_exist is None:
            check_user = getattr(recipe_exist, 'user_id')
            if check_user == user_id:
                return jsonify({'success': True}), 200
            save_recipe = Recipe(id=recipe_id, title=recipe_title,
                                 user_id='spoonacular')
            save_recipe.save()
        new_rating = Rating(rating=recipe_rating,
                            user_id=user_id,
                            recipe_id=recipe_id)
        new_rating.save()
        return jsonify({'success': True}), 200


if __name__ == '__main__':
    app.run(debug=True)
