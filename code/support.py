import requests
from settings import *


def get_coords(adress):
    params = {
        'geocode': adress,
        'apikey': GEOCODER_API_KEY,
        'format': 'json'
    }
    response = requests.get(GEOCODER_API_SERVER, params=params)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        return ','.join(toponym_coodrinates.split())
