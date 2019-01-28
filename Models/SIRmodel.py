import numpy as np
import array
import math
import os, sys
ROOT_WDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT_WDIR)
from Classes.county import *
import matplotlib.pyplot as plt
#from sympy import *

#constants
PA = 0
VA = 1
WV = 2
OH = 3
KY = 4
total = 5

class State:
    def __init__(self,name,lat,lng ):
        self.m_name = name
        self.m_code = STATE_CODES[name]
        self.m_lat = lat
        self.m_lng = lng
        self.m_drugList ={}
        self.countyList = {}


#coordinate Dictionary, format-latitude,longitude
coordinates = { PA : [41.1003153,-79.8481507], VA : [37.9864035,-81.6645646], WV : [38.9029755,-82.4252759], OH : [40.3477892,-84.9127508], KY : [37.805356,-88.0118901] }
def distance(state1,state2):
    return math.sqrt(
        (coordinates[state1][0] - coordinates[state2][0])**2 + ((math.cos((coordinates[state1][0]+coordinates[state2][0])/2)*(coordinates[state1][1]-coordinates[state2][1]))**2))

def movementFunction(state1,state2):
    if state1 != state2 :
        return 1/(10*distance(state1,state2))
    return 0

def generalHarmonic(a0,a1,a2,freq):
    return (lambda x : a0 + a1 * math.cos(freq*x) + a2 * math.sin(freq*x)
    )

def PAfit(x):
    Fa0 = 15110 
    Fa1 = 250.9 
    Fa2 = -3858 
    Ffreq = 0.8332
    
    Ga0  = 0.1922 
    Ga1 = -0.0306 
    Ga2 = -0.0527 
    Gfreq = 0.7091
    return(generalHarmonic(Fa0,Fa1,Fa2,Ffreq)(x)  - generalHarmonic(Fa0,Fa1,Fa2,Ffreq)(x) * generalHarmonic(Ga0,Ga1,Ga2,Gfreq)(x))/generalHarmonic(Ga0,Ga1,Ga2,Gfreq)(x) 
  
def VAfit(x):
    Fa0 = 2976 
    Fa1 = -692.4 
    Fa2 = -948 
    Ffreq = 0.6168
    
    Ga0 = 0.0863 
    Ga1 = -0.0089 
    Ga2 = -0.041 
    Gfreq = 0.6975
    
    return(generalHarmonic(Fa0,Fa1,Fa2,Ffreq)(x)  - generalHarmonic(Fa0,Fa1,Fa2,Ffreq)(x) * generalHarmonic(Ga0,Ga1,Ga2,Gfreq)(x))/generalHarmonic(Ga0,Ga1,Ga2,Gfreq)(x) 
  
def WVfit(x):
    Fa0 = 1253
    Fa1 =  -152.9 
    Fa2 = -374.9 
    Ffreq = 0.9638
    Ga0 = 0.1652 
    Ga1 = -0.0562 
    Ga2 = -0.0344 
    Gfreq = 0.5944
    return(generalHarmonic(Fa0,Fa1,Fa2,Ffreq)(x)  - generalHarmonic(Fa0,Fa1,Fa2,Ffreq)(x) * generalHarmonic(Ga0,Ga1,Ga2,Gfreq)(x))/generalHarmonic(Ga0,Ga1,Ga2,Gfreq)(x) 
  
def OHfit(x):
    Fa0 = 16400 
    Fa1 = -4706 
    Fa2 = -4537 
    Ffreq = 0.6858

    Ga0 = 0.1698 
    Ga1 = -0.0354 
    Ga2 = -0.0226 
    Gfreq = 0.743
    return(generalHarmonic(Fa0,Fa1,Fa2,Ffreq)(x)  - generalHarmonic(Fa0,Fa1,Fa2,Ffreq)(x) * generalHarmonic(Ga0,Ga1,Ga2,Gfreq)(x))/generalHarmonic(Ga0,Ga1,Ga2,Gfreq)(x)
  
def KYfit(x):
    Fa0 = 2310 
    Fa1 = -2149 
    Fa2 = -52.4
    Ffreq = 0.5557

    Ga0 = 0.0895 
    Ga1 = -0.0779 
    Ga2  = -0.0165
    Gfreq = 0.5935
    return(generalHarmonic(Fa0,Fa1,Fa2,Ffreq)(x)  - generalHarmonic(Fa0,Fa1,Fa2,Ffreq)(x) * generalHarmonic(Ga0,Ga1,Ga2,Gfreq)(x))/generalHarmonic(Ga0,Ga1,Ga2,Gfreq)(x)
  
def totalfit(x):
    Fa0 = 4000#38000
    Fa1 = 4000#7503
    Fa2 = 2000#11070
    Ffreq = 0.7192

    Ga0 = 0.156
    Ga1 = 0.0296
    Ga2 = 0.0418
    Gfreq = 0.7314
    y = (generalHarmonic(Fa0,Fa1,Fa2,Ffreq)(x)  - generalHarmonic(Fa0,Fa1,Fa2,Ffreq)(x) * generalHarmonic(Ga0,Ga1,Ga2,Gfreq)(x))/generalHarmonic(Ga0,Ga1,Ga2,Gfreq)(x) 
  
    return y

def F(t):
    a0 = 38000
    a1 = 7503
    a2 = 11070
    freq = 0.7192
    return  generalHarmonic(a0,a1,a2,freq)(t)

def G(t):
    a0 = 0.156
    a1 = 0.0296
    a2 = 0.0418
    freq = 0.7314
    return  generalHarmonic(a0,a1,a2,freq)(t)
def FitData(state):
    switcher = {
    PA : PAfit,
    VA : VAfit,
    WV : WVfit,
    OH : OHfit,
    KY : KYfit,
    total : totalfit
    }
    return (lambda i : (switcher[state](i) - switcher[state](i-1)) )

alpha = np.zeros((6,6),dtype = float)
for state1 in range(5):
    for state2 in range(5):
        alpha[state1][state2] = movementFunction(state1,state2) 
alpha[5,:] = np.zeros((1,6),dtype = float)
alpha[:,5] = np.zeros((1,6), dtype = float)
beta = { PA : 0.55, VA : 0.06, WV : 0.55, OH : 0.55, KY : 0.55, total : 0.06 }
gamma = { PA : 0.01, VA : 0.09, WV : 0.01, OH : 0.01, KY : 0.01, total : 0.09 }

def statePlot(state):

    HW = {  
    VA : [2298,1193,1709,4396,3132,3583,4261],
    OH :  [9301	,11004	,14633	,18340	,20590	,23347,20877],
    KY:	[629	,899	,2320	,4175	,4362	,4045	,3716],
    PA:	[12102,11741,13086,14745,18454,18964,17559],
    WV:	[902,949,1175,1857,1516,1135,1168],
    total:	[25232,25786, 32923, 43513,	48054, 51074, 47581]
    }
    
    
    
    OW = {  
    VA:	[39164,27776,30542,43298,29133,24236,29278],
    OH:	[61698,60278,70782,75407,80833,85803,94399],
    KY:	[28959,27386,25182,22645,22715,21766,22814],
    PA:	[77879,75052,65491,57351,58864,56387,54817],
    WV:	[7766,8361,8254,7205,5410,4210,4237],
    total:	[215466,198853, 200251, 205906, 196955, 192402, 205545] }
 

    RH = { PA : [0,0,0,0,0,0,0], VA : [0,0,0,0,0,0,0], WV : [0,0,0,0,0,0,0], OH : [0,0,0,0,0,0,0], KY : [0,0,0,0,0,0,0], total : [0,0,0,0,0,0,0] }

    k = {
    PA : 0,
    VA : 0,
    WV : 0 ,
    OH : 0,
    KY : 0,
    total : 0.005
    }#0.005
    q =  {
    PA : 0,
    VA : 0,
    WV : 0 ,
    OH : 0,
    KY : 0,
    total : 0.02}
    #0.02
    r =  {
    PA : 0,
    VA : 0,
    WV : 0 ,
    OH : 0,
    KY : 0,
    total : 0.01}
    #0.01
  
    rng = 50
    back = len(OW[state])-1
    for i in range(back,rng ):
        OW[state].append(
            (OW[state][i] + FitData(state)(i) + np.random.normal(0, k[state]*math.fabs(OW[state][i]))-beta[state]*OW[state][i-back]**2/(OW[state][i-back]+HW[state][i - back])))
        HW[state].append((HW[state][i] #+  np.matmul(np.ones(6),alpha[state,:].T)
         + beta[state]*OW[state][i-back]**2/(OW[state][i-back]+HW[state][i - back])- gamma[state]*HW[state][i-back]+np.random.normal(0,q[state]*math.fabs(HW[state][i]))))
        
        RH[state].append((RH[state][i] #- np.matmul(np.ones(6),alpha[state,:].T) 
        + gamma[state]*HW[state][i-back] - np.random.normal(0,r[state]*math.fabs(RH[state][i])))) 
    
    for i in range(0,len(OW[state])):
        if OW[state][i] < 0:
            OW[state][i] = 0#
        OW[state][i] = OW[state][i]
    
    for i in range(0,len(HW[state])):
        if HW[state][i] < 0:
            HW[state][i] = 0
        HW[state][i] = HW[state][i]
   
   
    #plot functionality
    fig,ax = plt.subplots()
    textstr = '\n'.join((r'$\beta=%.2f$' % (beta[state], ),
    r'$\gamma=%.2f$' % (gamma[state], ),
    r'$\mathrm{k}=%.2f$' % (k[state],),
    r'$\mathrm{q}=%.2f$' % (q[state],),
    r'$\mathrm{r}=%.2f$' % (r[state],),
    )
    )
    
    txtstr2 = '\n'.join((r'',
    r'Fit of Heroin:',
    r'f(t)=38000−7503cos(0.7192t)−11070sin(0.7182t)',
    r'',
    r'Fit of Percentage:',
    r'g(t)=0.156−0.0296cos(0.7314t)−0.0418sin⁡(0.7314t)'
    )
    )

    props = dict(boxstyle='round', alpha=0.5)
    ax.text(0.85, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
    ax.text(0.60,0.70, txtstr2, transform=ax.transAxes, 
    fontsize=14,verticalalignment='top', bbox=props)
    plt.plot(range(rng+1),OW[state],'b.',label="Opiod Users")
    plt.plot(range(rng+1),HW[state],'r.',label="Heroine Users")
    legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')

    plt.show()
    
statePlot(VA)