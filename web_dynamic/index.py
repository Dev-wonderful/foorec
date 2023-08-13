#!/usr/bin/python3
from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

SPOONACULAR_API_KEY = '8ca7176f9710474688667f16c6faee9e'


def get_recipes(ingredients):
    base_url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        'apiKey': SPOONACULAR_API_KEY,
        'ingredients': ','.join(ingredients),
        'number': 10  # Number of recipes to retrieve
    }

    response = requests.get(base_url, params=params)
    recipes = response.json()
    return recipes


@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = []

    if request.method == 'POST':
        ingredients = request.form['ingredients'].split(',')
        recipes = get_recipes(ingredients)

    return render_template('index.html', recipes=recipes)


if __name__ == '__main__':
    app.run(debug=True)