# encoding: utf-8
import numpy as np 
import pandas as pd
import scipy.optimize as op
import matplotlib.pyplot as plt
import pickle as pi


e = 1.602e-19
kB = 1.3806e-23

T = 295.6
T_LN = 79.5
sigmaT = 0.05
#SiLN2: 
#SiRT2: 
names = ['SiLN', 'SiRT', 'GaAsLN', 'GaAsRT', 'GeLN', 'GeRT', 'SiLN2', 'SiRT2','GaAsLN2', 'GaAsLN3']
ranges = [[1.01,1.13],[0.04,0.78],[1.51,2.06],[1.02,1.20],[0.78,1.04],[0.37,0.67],[1.0,1.14],[0.48,0.79],[1.45,2.08],[1.47,2.14]]


def data(names):
    results = {}
    for i,j in enumerate(names):
        with open(j, 'rb') as pick:
            results[j] = [pi.load(pick, fix_imports=True)]
        with open(j+'V', 'rb') as pick:
            results[j].append(pi.load(pick,fix_imports=True))
        results[j].append(ranges[i])
        if results[j][1][0] > results[j][1][-1]:
            results[j][0] = results[j][0][::-1]
            results[j][1] = results[j][1][::-1]
    return(results)

# names = ['GaAs(RT)', 'Ge(RT)', 'Si(RT)'] #79.5K -N

def f(volts_s, m, c):
     vals = m*volts_s + c
     return vals

def fitNplot(f, title, amps, volts, T, range=0):
    lnamps = np.log(amps)
    if range == 0:
        plt.figure()
        plt.plot(volts,lnamps,'o')
        plt.title(title)
        plt.ylabel('Ln(current)')
        plt.xlabel('Voltage (V)')
    else:
        lnamps_s = val_range(volts,lnamps,range[0],range[1])[1]
        volts_s = val_range(volts,lnamps,range[0],range[1])[0]
        plt.figure()
        plt.plot(volts_s, lnamps_s, 'o')
        fit = op.curve_fit(f, volts_s, lnamps_s)
        line = [fit[0][0]*i+fit[0][1] for i in volts_s]
        plt.plot(volts_s,line, '-')
        plt.title(title)
        plt.ylabel('Ln(current)')
        plt.xlabel('Voltage (V)')
        perr = np.sqrt(np.diag(fit[1]))
        print("Value of n: %g" % n(fit[0][0],T), "Error on n: %g" % nerr(fit[0][0],perr[0],T), "Value of I_0: %g A" % i0(fit[0][1]), "Error on I_0: %g" % i0err(fit[0][1],perr[1]))

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

def val_range(volts, lnamps, lo=0, hi=0):
    volts_s = []
    lnamps_s = []
    for i,j in enumerate(volts):
        if (j > lo) and (j < hi) and (np.isnan(lnamps[i]) == False):
                volts_s.append(j)
                lnamps_s.append(lnamps[i])
    return [volts_s,lnamps_s]

# Silicon, room temp
def plot(results):
    for i in dict.keys(results):
        plt.figure()
        plt.plot(results[i][1],results[i][0], 'o')
        plt.title(i)
        plt.xlabel('Potential difference (V)')
        plt.ylabel('Current (A)')



def analyse(data):
    for i in dict.keys(data):
        if 'LN' in i:
            print(i)
            fitNplot(f,i,data[i][0],data[i][1], T_LN, data[i][2])
        else:
            print(i)
            fitNplot(f,i,data[i][0],data[i][1], T, data[i][2])

#print(data(names))
analyse(data(names))
#print(pd.DataFrame(data(names)))

# print('Silicon in liquid nitrogen')
# fitNplot(f,SiLN,SiLNV,val_range(SiLNV, 0.99, 1.05),T_LN)
# print('Silicon in liquid nitrogen 2')
# fitNplot(f,SiLN2,SiLN2V,val_range(SiLN2V, 1.25, 1.6),T_LN)

# print('Silicon at room temperature')
# fitNplot(f,SiRT,SiRTV,val_range(SiRTV, 0.3, 0.74),T)

# print('Silicon at room temperature 2')
# fitNplot(f,SiRT2,SiRT2V,val_range(SiRT2V, 0.3, 0.74),T)

# print('GaAs in liquid nitrogen')
# fitNplot(f,GaAsLN,GaAsLNV,val_range(GaAsLNV, 1.48 ,2.1),T_LN)

# print('GaAs at room temperature')
# fitNplot(f,GaAsRT,GaAsRTV,val_range(GaAsRTV, 1.05, 1.18),T)

# print('Ge in liquid nitrogen')
# fitNplot(f,GeLN,GeLNV,val_range(GeLNV, 0.85, 1.03),T_LN)

# print('Ge at room temperature')
# fitNplot(f,GeRT,GeRTV,val_range(GeRTV, 0.40, 0.68),T)


plt.show()