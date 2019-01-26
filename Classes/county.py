import math
import os, sys
ROOT_WDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT_WDIR)
from scripts.searchDrugCounty import search

import csv

class County: 
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

    def inputDrugList(self,dL):
        return


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
print(search(allCounties[0].m_state,allCounties[0].m_name , "Oxycodone"))
          

    

    