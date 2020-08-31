import requests
from config import *
from time import sleep

def decimal_from_dms(dms, ref):
    """converts decimal, minute, second GPS information into decimal degrees"""
    
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ('S', 'W'):
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 6)

def get_coordinates(JPGInfo):
    lat = decimal_from_dms(JPGInfo['GPSLatitude'], JPGInfo['GPSLatitudeRef'])
    lon = decimal_from_dms(JPGInfo['GPSLongitude'], JPGInfo['GPSLongitudeRef'])

    return (lat, lon)


def reverse_geocode(coordinates):
    """takes coordinates and returns the zip code as a string, or the appropriate error"""
    
    (lat, lon) = coordinates
    response = requests.get(BASE_URL,
                            params = {
                                "key": API_KEY,
                                "lat": lat,
                                "lon": lon,
                                "format": RESPONSE_FORMAT
                            })
    #I am limited to 10,000 api calls per day, and 2 api calls per second
    sleep(0.5)

    if response.status_code != 200:
        return f"Unable to retreive zip, coordinates: {coordinates}"

    json_response = response.json()
    try:
        return str(json_response["address"]["postcode"])
    except:
        return f"postal code unavailable in api, coordinates: {coordinates}"