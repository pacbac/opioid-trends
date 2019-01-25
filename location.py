import requests
import json
import urllib.parse
url = "https://maps.googleapis.com/maps/api/geocode/json?"
address = "City Hall, New York, NY"
response = requests.get(url + address)
if(response.ok):

 
    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jData = json.loads(response.content)
else:
    print("Response not Ok")