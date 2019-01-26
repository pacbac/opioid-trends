import math


class County: 
    drugList = {}
    lat = 0.0
    lng = 0.0
    def distanceTo(self,otherCounty):
         return math.sqrt(
        ((self.lat - otherCounty.lat)**2 + 
        ((math.cos((self.lat - otherCounty.lat)/2)*
        (self.lng-otherCounty.lng)**2))) )
    

    