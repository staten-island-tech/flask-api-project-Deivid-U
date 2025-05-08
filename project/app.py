from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=150")
    data = response.json()
    pokemon_list = data['results']
    
    pokemons = []
    
    for pokemon in pokemon_list:
        url = pokemon['url']
        parts = url.strip("/").split("/")
        id = parts[-1]
        
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
        
        pokemons.append({
            'name': pokemon['name'].capitalize(),
            'id': id,
            'image': image_url
        })
    
    return render_template("index.html", pokemons=pokemons)

@app.route("/pokemon/<int:id>")
def pokemon_detail(id):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    data = response.json()
    
    types = [t['type']['name'] for t in data['types']]
    height = data.get('height')
    weight = data.get('weight')
    name = data.get('name').capitalize()
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
    
    stat_names = [stat['stat']['name'] for stat in data['stats']]
    stat_values = [stat['base_stat'] for stat in data['stats']]
    
    return render_template("pokemon.html", pokemon={
        'name': name,
        'id': id,
        'image': image_url,
        'types': types,
        'height': height,
        'weight': weight,
        'stat_names': stat_names,
        'stat_values': stat_values
    })

if __name__ == '__main__':
    app.run(debug=True)