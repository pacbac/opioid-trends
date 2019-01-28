import numpy as np
import array
import math
import os, sys
ROOT_WDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT_WDIR)
import matplotlib.pyplot as plt

#constants to each state
PA = 0
VA = 1
WV = 2
OH = 3
KY = 4
total = 5

#dictionary holds coordinates for each state
#coordinate Dictionary, format-latitude,longitude
coordinates = { PA : [41.1003153,-79.8481507], VA : [37.9864035,-81.6645646], WV : [38.9029755,-82.4252759], OH : [40.3477892,-84.9127508], KY : [37.805356,-88.0118901] }

#distance function to calculate distance between states
def distance(state1,state2):
    return math.sqrt(
        (coordinates[state1][0] - coordinates[state2][0])**2 + ((math.cos((coordinates[state1][0]+coordinates[state2][0])/2)*(coordinates[state1][1]-coordinates[state2][1]))**2))

#movement function used to model population transfer between states
def movementFunction(state1,state2):
    if state1 != state2 :
        return 1/(10*distance(state1,state2))
    return 0

#A general template of a harmonic functionn
def generalHarmonic(a0,a1,a2,freq):
    return (lambda x : a0 + a1 * math.cos(freq*x) + a2 * math.sin(freq*x)
    )

#various functions describing fourier functions for each state
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

#function takes state and returns a fourier fuction cooresponding to the state
def FitData(st):
    switcher = {
    PA : PAfit,
    VA : VAfit,
    WV : WVfit,
    OH : OHfit,
    KY : KYfit,
    total : totalfit
    }
    return (lambda i : (switcher[st](i) - switcher[st](i-1)) )

#alpha is a matrix that stores movement coefficient between two states
alpha = np.zeros((6,6),dtype = float)
for state1 in range(5):
    for state2 in range(5):
        alpha[state1][state2] = movementFunction(state1,state2) 
alpha[5,:] = np.zeros((1,6),dtype = float)
alpha[:,5] = np.zeros((1,6), dtype = float)

#dictionaries store probability variables for eachstate
beta = { PA : 0.05, VA : 0.05, WV : 0.06, OH : 0.06, KY : 0.06, total : 0.05 }
gamma = { PA : 0.06, VA : 0.09, WV : 0.06, OH : 0.09, KY : 0.09, total : 0.09 }

#dictionary holds Number of Heroine cases for each state
#each state initialized with first 6 years of data as provided
HW = {  
    VA : [2298,1193,1709,4396,3132,3583,4261],
    OH :  [9301	,11004	,14633	,18340	,20590	,23347,20877],
    KY:	[629	,899	,2320	,4175	,4362	,4045	,3716],
    PA:	[12102,11741,13086,14745,18454,18964,17559],
    WV:	[902,949,1175,1857,1516,1135,1168],
    total:	[25232,25786, 32923, 43513,	48054, 51074, 47581]
    }
    
    
#dictionary holds Number of Opiod cases for each state
#each state initialized with first 6 years of data as provided
OW = {  
    VA:	[39164,27776,30542,43298,29133,24236,29278],
    OH:	[61698,60278,70782,75407,80833,85803,94399],
    KY:	[28959,27386,25182,22645,22715,21766,22814],
    PA:	[77879,75052,65491,57351,58864,56387,54817],
    WV:	[7766,8361,8254,7205,5410,4210,4237],
    total:	[215466,198853, 200251, 205906, 196955, 192402, 205545] }
 
#dictionary holds the number of people recoverd
#initialized as per model
RH = { PA : [0,0,0,0,0,0,0], VA : [0,0,0,0,0,0,0], WV : [0,0,0,0,0,0,0], OH : [0,0,0,0,0,0,0], KY : [0,0,0,0,0,0,0], total : [0,0,0,0,0,0,0] }

#Dictionary holding constants used to produce White Noise
k = {
    PA : 0.005,
    VA : 0.005,
    WV : 0.005 ,
    OH : 0.005,
    KY : 0.005,
    total : 0.005
    }
q =  {
    PA : 0.02,
    VA : 0.02,
    WV : 0.02 ,
    OH : 0.02,
    KY : 0.02,
    total : 0.02}
    
r =  {
    PA : 0.01,
    VA : 0.01,
    WV : 0.01,
    OH : 0.01,
    KY : 0.01,
    total : 0.01}
    

def sumAlphaColumn(state, yr):
    sum = 0.0
    for st2 in beta:
        if st2 != total:
            sum = sum + alpha[st2][state] * gamma[st2] * HW[st2][yr]
    return sum
def sumAlphaRow(state, yr):
    sum = 0.0
    for st2 in beta:
        if st2 != total:
            sum = sum + alpha[state][st2] * gamma[st2] * HW[st2][yr]
    return sum
def dotType(state):
    switcher = {
    PA : ['b.','k.'],
    VA : ['gv','bv'],
    WV : ['r8','g8'],
    OH : ['ch','rh'],
    KY : ['m*','c*'],
    total : ['y+','r+']
    
    }
    return switcher[state]
def codeToString(stat):
    r =  {
    PA : 'PA',
    VA : 'VA',
    WV : 'WV',
    OH : 'OH',
    KY : 'KY',
    total : 'ALL'}
    return r[stat]
def getString(state):
    switcher = {
     VA : '\n'.join((r'',
    r'Fit of Heroin:',
    r'f(t)=2976-692.4cos(0.6168t)−948sin(0.6168t)',
    r'',
    r'Fit of Percentage:',
    r'g(t)=0.0863-0.0089cos(0.6975t)-0.041sin⁡(0.6975t)'
    )
    ) ,
    PA :'',
    WV : '',
    OH : '',
    KY : '',
    total : ''    }
    return switcher[state]

#function plots results for all states and the net result
def allPlot():
    rng = 50
    #loo
    back = len(OW[PA])-1
    for i in range(back,rng):
        for st in beta:

            #differential equations used to model Opiod users (OW) and Heroin Users (HW)
            OW[st].append(
                 (OW[st][i] + FitData(st)(i) + np.random.normal(0, k[st]*math.fabs(OW[st][i]))-beta[st]*OW[st][i-back]**2/(1+OW[st][i-back]+HW[st][i - back]))) 
            
            HW[st].append((HW[st][i] + sumAlphaColumn(st,i)
            + beta[st]*OW[st][i-back]**2/(1+OW[st][i-back]+HW[st][i - back])- gamma[st]*HW[st][i-back]+np.random.normal(0,q[st]*math.fabs(HW[st][i]))))
            
            RH[st].append((RH[st][i] - sumAlphaRow(st,i)) 
            + gamma[st]*HW[st][i-back] - np.random.normal(0,r[st]*math.fabs(RH[st][i]))) 
        
            for j in range(0,len(OW[st])):
                if OW[st][j] < 0:
                    OW[st][j] = 0
            for j in range(0,len(HW[st])):
                if HW[st][j] < 0:
                    HW[st][j] = 0   
    
    
    #plot functionality
    fig,ax = plt.subplots()
    for sat in beta: 
        plt.plot(range(rng),HW[sat][:-1],dotType(sat)[1],label=codeToString(sat)+" Heroine Users")
    legend = ax.legend(loc='upper right', shadow=True, fontsize='x-large')

    plt.show()
    
allPlot()

