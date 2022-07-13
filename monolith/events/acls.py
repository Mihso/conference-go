from tempfile import TemporaryFile
from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests
import json

headers = {'Authorization': PEXELS_API_KEY}

headers2 = {'Authorization': OPEN_WEATHER_API_KEY}


def get_photo(city, state):
    
    params = {
        "per_page" : 1,
        "query" : city +" "+ state,
    }

    url = "https://api.pexels.com/v1/search" #?query= + city +","+ state+"per_page=1"
    r = requests.get(url, params = params, headers=headers)
    photo = json.loads(r.content)

    try:
        location_photo = {
            "picture_url": photo["photos"][0]["src"]["original"],#photo["url"],
        }
        return location_photo
    except(KeyError, IndexError): 
        return {"picture_url": None}



def get_weather_data(city, state):
    url2= 'http://api.openweathermap.org/geo/1.0/direct'
    params ={
        "q" : f"{city}, {state}, US",
        "limit" :  1,
        "appid" : OPEN_WEATHER_API_KEY
    }
    r2 = requests.get(url2, params = params, headers = headers2)
    coord = json.loads(r2.content)

    try:
        latitude = coord[0]["lat"]
        longitude = coord[0]["lon"]
    except(KeyError, IndexError):
        return None

    params = {
        "lat" : latitude,
        "lon" : longitude,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial"
    }

    url2 = 'http://api.openweathermap.org/data/2.5/weather'
    response = requests.get(url2, params = params, headers = headers2)
    cooord = json.loads(response.content)

    try:
        return{
            "description": cooord["weather"][0]["description"],
            "temp": cooord["main"]["temp"],
        }
    except(KeyError, IndexError):
        return None