import os
import requests
import json
import urllib.parse
from decouple import config
import pandas as pd

DATA_DIR = f'{os.getcwd()}/2019_MCMProblemC_DATA/ACS_10_5YR_DP02/ACS_10_5YR_DP02_with_ann.csv'
COUNTY_COL_IND = 3

data = pd.read_csv(DATA_DIR)

def getLatLng(countyStr):
    API_KEY = config('API_KEY')
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (countyStr, API_KEY)
    response = requests.get(url)
    if(response.ok):
        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        jData = json.loads(response.content)

        # potential errors in extracting data from json structure
        geometry = jData['results'][0]['geometry']
        # get lat and lng bounds for the city from the json response
        latN = geometry['viewport']['northeast']['lat']
        lngN = geometry['viewport']['northeast']['lng']
        latS = geometry['viewport']['southwest']['lat']
        lngS = geometry['viewport']['southwest']['lng']
        return (latN + latS)/2, (lngN + lngS)/2
    else:
        raise Exception("Response not Ok")

def main():
    totalRows = data.shape[0] - 1
    newData = pd.DataFrame(columns=['County', 'Latitude', 'Longitude'])
    curPercentage = -1
    for row in data.itertuples():
        i = row[0]
        if i == 0: 
            continue # first elem of row is its index
        county = row[COUNTY_COL_IND]
        dataRow = list((county,) + getLatLng(county))
        newData.loc[i] = dataRow
        percentage = int(float(i/totalRows) * 100)
        if percentage > curPercentage:
            curPercentage = percentage 
            print(f'{curPercentage}% complete')
        
    newData.to_csv("generated_data/latlng.csv", encoding='utf-8')
    print("Saved to latlng.csv")

if __name__ == "__main__":
    main()