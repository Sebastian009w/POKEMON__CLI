"""API."""
import requests
from PIL import Image
import os
import time
import ascii_magic

URL_API = 'https://pokeapi.co/api/v2/pokemon/'
IMAGE_FILE = 'pokemon.png'


def get_pokemon_data(name: str) -> dict:
    """GET /"""
    try:
        url = f'{URL_API}{name.lower()}'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.HTTPError, ValueError) as error_request:
        print(
            f'error de la solicitud a la ruta: {url}: error: {error_request}')
        return None


def pokemon_image(pokemon__data):
    """image pokemon."""
    try:
        sprites__url = pokemon__data["sprites"]["front_default"]
        response = requests.get(sprites__url, timeout=10)
        with open(IMAGE_FILE, 'wb') as file:
            file.write(response.content)
        os.chmod(IMAGE_FILE, 0o755)
        time.sleep(0.5)
    except (requests.exceptions.RequestException, IOError) as error_image:
        print(f"error al cafgar la imagen {error_image}")


def show_pokemon_ascii(pokemon_data):
    """Magic."""
    try:
        with Image.open(IMAGE_FILE) as image:
            ascii_magic.from_image(IMAGE_FILE).to_terminal(
                columns=120, width_ratio=3)
            print()
            stats_pokemon(pokemon_data)
            print()
    except Exception as error_art:
        print(f"error loading image {error_art}")


def stats_pokemon(pokemon_data):
    """Stats Pokemon"""
    print(f"name: {pokemon_data['name']}")
    print(f"HP: {pokemon_data['stats'][0]['base_stat']}")
    print(f"type: {pokemon_data['types'][0]['type']['name']}")
    for ability in pokemon_data["abilities"]:
        print("", ability["ability"]["name"])


def check_response_pokemon(res, pokemon_name):
    """validate."""
    if res.status_code != 200:
        print(
            f"Oh lo siento el pokemon ingresado no se pudo encontrar:  {pokemon_name}")
        return False
    return True
