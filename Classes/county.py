import math
import os, sys
ROOT_WDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT_WDIR)
from scripts.searchDrugCounty import search
import csv

""" Contains the properties and abilities of a county object"""
class County: 
    """
    m_name: the county name in ALL CAPS
    m_state: the state the county is in in state code format, Ex. 'KY', 'PA', etc
    m_drugList: drug list
    m_lat = county latitude
    m_lng = county longitude
    """
    def __init__(self, nm,st,lt,ln):
        self.m_name = nm
        self.m_state = st
        self.m_drugList = {}
        self.m_lat = lt
        self.m_lng = ln

    """
    Finds the distance between two county objects
    """
    def distanceTo(self,otherCounty):
         return math.sqrt(
        ((self.m_lat - otherCounty.m_lat)**2 + 
        ((math.cos((self.m_lat - otherCounty.m_lat)/2)*
        (self.m_lng-otherCounty.m_lng)**2))) )

    def inputDrugList(self,dL):
        return

    def __str__(self):
        return " ".join((self.m_name, self.m_state, "Lat:", self.m_lat, "Lng:", self.m_lng))



STATE_CODES = {
    'Virginia' : 'VA',
    'Ohio' : 'OH',
    'Kentucky' : 'KY',
    'Pennsylvania' : 'PA',
    'West Virginia' : 'WV'
}

allCounties = []
with open(ROOT_WDIR +"/generated_data/latlng.csv") as cnties,open(ROOT_WDIR +"/generated_data/DrugList.csv") as drugs:
      countyReader = csv.DictReader(cnties)
      drugsReader = csv.reader(drugs)
      for cnty in countyReader:
        [name,state] = cnty['County'].split(', ')
        name = str(name).upper()
        state = STATE_CODES[state]
        allCounties.append(County(name,state,cnty['Latitude'],cnty['Longitude']))
        for drug in drugsReader:
            thisCounty = allCounties[-1]
            allCounties[-1].m_drugList[drug[0]] = search(thisCounty.m_state,thisCounty.m_name,drug[0])
          

    

    