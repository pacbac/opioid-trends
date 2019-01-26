import math
import os, sys
ROOT_WDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT_WDIR)
from scripts.searchDrugCounty import search

import csv

class County: 
    m_name = ""
    m_state = ""
    m_drugList = {}
    m_lat = 0.0
    m_lng = 0.0
    def __init__(self, nm,st,lt,ln):
        self.m_name = nm
        self.m_state = st
        self.m_drugList = {}
        self.m_lat = lt
        self.m_lng = ln

    def distanceTo(self,otherCounty):
         return math.sqrt(
        ((self.m_lat - otherCounty.m_lat)**2 + 
        ((math.cos((self.m_lat - otherCounty.m_lat)/2)*
        (self.m_lng-otherCounty.m_lng)**2))) )



allCounties = []
with open(ROOT_WDIR +"/generated_data/latlng.csv") as cnties:
      countyReader = csv.DictReader(cnties)

      for cnty in countyReader:
        [name,state] = cnty['County'].split(',')
        allCounties.append(County(name,state,cnty['Latitude'],cnty['Longitude']))

    

    