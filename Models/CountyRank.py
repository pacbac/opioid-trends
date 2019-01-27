#import scripts\searchDrugCounty
#assume directory mcm-2019
import os, sys
ROOT_WDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT_WDIR)
from Classes.county import *
import math

getAllCounties()
#findScores corresponding to a drug. Returs a dictionary that maps cnty to its score (DOESN'T CONTAIN ALL COUNTIES)
def findScores(drug):
    
    counties = []
    year = County.yearDrugBegan(allCounties,drug) #to consider only counties that had earliest outbreaks
    
    for e in County.countiesUseDrug(allCounties,drug): #consider only counties that used the drug:
        if year in e.m_drugList[drug]:
            counties.append(e)
    score = {}
    for cnty in counties:
        score[cnty] = getScore(counties,cnty,drug,year)
    return score

#get Score for a single county
def getScore(all,cnty, drug,year):
    otherCounties = []
    for e in all:
        if e != cnty:
            otherCounties.append(e)
    if otherCounties:
        return sumSpatialFactors(cnty,drug,year,otherCounties) + sumTime(cnty,drug)
       
    #if only one county then we assign 0            
    return 0.0

def sumSpatialFactors(cnty,drug,year,otherCounties):
   return County.sumPop(metaFunc(cnty,drug,year),drug,year,otherCounties)
def sumTime(cnty,drug):
    n = 0
    sum = 0.0
    dlt = 0.8
    for e in cnty.m_drugList[drug]:
         sum = sum + (dlt**n)*math.log(cnty.m_drugList[drug][e])
         n = n + 1
    return sum


#meta function that returns a function such that sumpop can be evaluated for each cnty
def metaFunc(cnty,drug,year):
    return lambda x : math.log(
    (
        (cnty.drugCases(drug,year)) / 
        (x.drugCases(drug,year)) + 1
    ) **(1/(1+ 25 * cnty.distanceTo(x)))
)

def findStateOrigin(state,drug):
    scores = findScores(drug)
    stateScores = {}
    for e in scores:
        if e.m_state == state:
            stateScores[e] = scores[e]
    greatFive = sorted(stateScores.items(),  key=(lambda x : x[1])) [-5:]
        
    

findStateOrigin("PA","Codeine")


