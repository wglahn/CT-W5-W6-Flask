from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/entry', methods = ['GET', 'POST'])
def entry():
    if request.method == 'POST':
        name = request.form.get('pokemonname')
        if name:
            url = f"https://pokeapi.co/api/v2/pokemon/{name}"
            response = requests.get(url)
            if response.ok:
                pokemon_dict={
                    "name":response.json()['forms'][0]['name'],
                    "ability":response.json()['abilities'][0]['ability']['name'],
                    "hp":response.json()['stats'][0]['base_stat'],
                    "attack":response.json()['stats'][1]['base_stat'],
                    "defense":response.json()['stats'][2]['base_stat'],
                    "sprite": response.json()['sprites']['front_shiny']
                    }
                return render_template('entry.html.j2', pokemon = pokemon_dict)

            else:
                error_string = f"{name} does not exist. Please try again."
                return render_template('entry.html.j2', error = error_string)
        error_string = f"You must enter a name. Please try again."
        return render_template('entry.html.j2', error = error_string)
    else: # if its a get request
        return render_template('entry.html.j2')