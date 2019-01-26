import numpy as np
import array
import math

#constants
PA = 0
VA = 1
WV = 2
OH = 3
KY = 4
total = 5

#coordinate Dictionary, format-latitude,longitude

coordinates = { PA : [41.1003153,-79.8481507], VA : [37.9864035,-81.6645646], WV : [38.9029755,-82.4252759], OH : [40.3477892,-84.9127508], KY : [37.805356,-88.0118901] }
def distance(state1,state2):
    return math.sqrt(
        (coordinates[state1][0] - coordinates[state2][0])**2 + ((math.cos((coordinates[state1][0]+coordinates[state2][0])/2)*(coordinates[state1][1]-coordinates[state2][1]))**2))

def movementFunction(state1,state2):
    if state1 != state2 :
        return 1/(10*distance(state1,state2))
    return 0

def PAfit(i):

    return 338.2*math.exp(-0.4172*i)

def VAfit(i):

    return 8716*math.exp(-0.2331*i)

def WVfit(i):

    return  3451*math.exp(-0.3566*i)

def OHfit(i):

    return  840*math.exp(-0.8487*i)

def KYfit(i):

    return  19340*math.exp(-0.3837*i)

def totalfit(i):

    return  11754.48*math.exp(-0.3655*i)+62.676*math.exp(0.09*i)

def exponentialFit(state,i):
    switcher = {
        PA : PAfit,
    VA : VAfit,
    WV : WVfit,
    OH : OHfit,
    KY : KYfit,
    total : totalfit
    }

    return (switcher[state](i) + switcher[state](i+1))/2 

def main():
    alpha = np.zeros((5,5),dtype = float)
    for state1 in range(5):
        for state2 in range(5):
            alpha[state1][state2] = movementFunction(state1,state2) 
    beta = { PA : 0.55, VA : 0.55, WV : 0.55, OH : 0.55, KY : 0.55, total : 0.55 }
    gamma = { PA : 0.01, VA : 0.01, WV : 0.01, OH : 0.01, KY : 0.01, total : 0.01 }
    OW = { PA : [237], VA : [6440], WV : [2613], OH : [371], KY : [13428], total : [23089] }
    HW = { PA : [9744], VA : [35022], WV : [6055], OH : [70628], KY : [16160], total : [217609] } 
    RH = { PA : [0], VA : [0], WV : [0], OH : [0], KY : [0], total : [0] }

    k = 0.01 
    q = 0.02
    r = 0.0
    state = PA
    for i in range(7):
        OW[state].append(OW[state][i] + exponentialFit(state,i) + np.random.normal(0, k*OW[state][i])-beta[state]*OW[state][i])
        HW[state].append(HW[state][i] + beta[state]*OW[state][i]- gamma[state]*HW[state][i]+np.random.normal(0,q*HW[state][i]))
        RH[state].append(RH[state][i] + gamma[state]*HW[state][i] - np.random.normal(0,r*RH[state][i]))
    print(OW[state])
    print(HW[state])
    print(RH[state])

exponentialFit(PA,5)
