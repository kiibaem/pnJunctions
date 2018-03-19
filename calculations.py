# encoding: utf-8
import numpy as np 
import pandas as pd
import scipy.optimize as op
import scipy.stats as st
import matplotlib.pyplot as plt
import pickle as pi


e = 1.602e-19
kB = 1.3806e-23

T = 295.6
T_LN = 79.5
sigmaT = 0.05
 
diode_names = ['SiLN', 'SiRT', 'GaAsLN', 'GaAsRT', 'GeLN', 'GeRT', 'SiLN2', 'SiRT2','GaAsLN2', 'GaAsLN3']
diode_ranges = [[1.01,1.13],[0.04,0.78],[1.51,2.06],[1.02,1.20],[0.78,1.04],[0.37,0.67],[1.0,1.14],[0.48,0.79],[1.45,2.08],[1.47,2.14]]
LED_names = ['LEDREDRT','LEDREDRT2','LEDREDRT3','LEDREDRT4','LEDYELLOWRT','LEDYELLOWRT2','LEDYELLOWRT3','LEDREDRT5','LEDGREENRT']
#LED_ranges = [0,0,0,0,0,0,[1.76,1.9],[1.78,1.96],[1.84,1.97]]
volterr = 5e-4
amperr = 5e-4



def data(names):
    results = {}
    if type(names)==str:
        names = [names]
    for i,j in enumerate(names):
        with open(j, 'rb') as pick:
            results[j] = [pi.load(pick, fix_imports=True)]
        with open(j+'V', 'rb') as pick:
            results[j].append(pi.load(pick,fix_imports=True))
        if results[j][1][0] > results[j][1][-1]:
            results[j][0] = results[j][0][::-1]
            results[j][1] = results[j][1][::-1]
    return(results)

# names = ['GaAs(RT)', 'Ge(RT)', 'Si(RT)'] #79.5K -N

def f(volts_s, m, c):
     vals = m*volts_s + c
     return vals

def fitNplot(f, title, amps, volts, volterr, T, range=0):
    lnamps = np.log(amps)
    lnerrs = [i**(-1)*5e-4 for i in amps]
    
    if range == 0:
        plt.figure()
        plt.plot(volts,lnamps,'o')
        plt.title(title)
        plt.ylabel('Ln(current)')
        plt.xlabel('Voltage (V)')
    else:
        lnamps_s = lnamps[range[0]:range[1]]
        volts_s = volts[range[0]:range[1]]
        lnamperrs_s = ranges[2]
        plt.figure()
        plt.errorbar(volts_s, lnamps_s,xerr=volterr,yerr=lnamperrs_s,fmt='o')
        fit = op.curve_fit(f, volts_s, lnamps_s, sigma=lnamperrs_s, absolute_sigma=True)
        line = [fit[0][0]*i+fit[0][1] for i in volts_s]
        plt.plot(volts_s,line,'-')
        plt.title(title)
        plt.ylabel('Ln(current)')
        plt.xlabel('Voltage (V)')
        perr = np.sqrt(np.diag(fit[1]))
        return [n(fit[0][0],T),nerr(fit[0][0],perr[0],T),i0(fit[0][1]),i0err(fit[0][1],perr[1])]

def n(slope,T):
    ns = (e)/(slope*kB*T)
    return ns

def nerr(slope,slopeErr,T):
    nerrs = np.sqrt((e/(slope*kB*T**2))*sigmaT**2 + (e/(slope**2*kB*T)*slopeErr**2))
    return nerrs

def i0(icept):
    i0s = np.exp(icept)
    return i0s

def i0err(icept,iceptErr):
    i0errs = np.exp(icept)*iceptErr
    return i0errs

def val_range(volts, lnamps, lnamperrs, lo=0, hi=0):
    volts_s = []
    lnamps_s = []
    lnamperrs_s = []
    for i,j in enumerate(volts):
        if (j > lo) and (j < hi) and (np.isnan(lnamps[i]) == False) and (np.isinf(lnamps[i]) == False):
                volts_s.append(j)
                lnamps_s.append(lnamps[i])
                lnamperrs_s.append(lnamperrs[i])
    return [volts_s,lnamps_s,lnamperrs_s]


def plot(results,amperr,volterr):
    for i in dict.keys(results):
        plt.figure()
        plt.errorbar(results[i][1],results[i][0],yerr=amperr,xerr=volterr,fmt='o')
        plt.title(i)
        plt.xlabel('Potential difference (V)')
        plt.ylabel('Current (A)')



def analyse(data,range,volterr):
    for i in dict.keys(data):
        if 'LN' in i:
            dat = fitNplot(f,i,data[i][0],data[i][1],volterr, T_LN, range)
            resultsTable[i] = pd.Series(dat,['n', 'n Error', 'I_0 (A)', 'I_0 Error (A)'])
        else:
            dat = fitNplot(f,i,data[i][0],data[i][1],volterr, T,  range)
            resultsTable[i] = pd.Series(dat,['n', 'n Error', 'I_0 (A)', 'I_0 Error (A)'])
            
def autorange(data):
    volts = data[1]
    amps = data[0]
    correlations = np.zeros((len(volts),len(volts)+1),dtype=float)
    for i in range(0,len(volts)):
        for j in range(len(volts),0,-1):
            if len(volts[i:j]) >= len(volts)%5:
                val = st.pearsonr(volts[i:j],amps[i:j])[0]
                if np.isnan(val) == True:
                    val= 0.
                    correlations[i,j] = val
    print(correlations)
    max = np.argwhere(correlations == np.max(correlations))
    return np.max(correlations)

LED_data = data(LED_names[-3:])
# LED_ranges = [autorange(LED_data[i]) for i in LED_names]
LED_ranges=[]
for i in LED_names[-3:]:
    print(i)
    LED_ranges.append(autorange(LED_data[i]))
print(LED_ranges)
#resultsTable = pd.DataFrame(columns=diode_names)
#resultsTable1 = pd.DataFrame(columns=LED_names)
#analyse(data(diode_names,diode_ranges,volterr))
analyse(LED_data,volterr,LED_ranges)
#plot(data(diode_names,diode_ranges),amperr,volterr)
#print(resultsTable)



plt.show()