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

names = ['SiLN', 'SiRT', 'GaAsLN', 'GaAsRT', 'GeLN', 'GeRT', 'SiLN2', 'SiRT2', 'GaAsLN3']

def data(names):
    results = {}
    for i in names:
        with open(i, 'rb') as pick:
            results[i] = [pi.load(pick)]
        with open(i+'V', 'rb') as pick:
            results[i].append(pi.load(pick))
    return(results)

# names = ['GaAs(RT)', 'Ge(RT)', 'Si(RT)'] #79.5K -N

def f(volts_s, m, c):
     vals = m*volts_s + c
     return vals

def fitNplot(f,amps,volts,T):
    lnamps = np.log(amps)
    lnamps_s = []
    volts_s = []
    for i,j in enumerate(lnamps):
        if np.isnan(j) == False:
            lnamps_s.append(j)
            volts_s.append(volts[i])
    for i in lnamps:
        if i != i+1:
            for j in volts:
                parm = np.polyfit([j,j+1],[i,i+1],1)[1]
                if (parm > 1.9) and (parm < 2.1):
                    #if np.polyfit([j,j+1],[i,i+1],1)[1] < 2.1:
                    lnamps_s.append(i), volts_s.append(j)

    print(lnamps_s, volts_s)
    plt.figure()
    plt.plot(volts_s, lnamps_s, 'o')
    fit = op.curve_fit(f, volts_s, lnamps_s, check_finite = False)
    line = [fit[0][0]*i+fit[0][1] for i in volts_s]
    plt.plot(volts_s,line, '-')
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

def val_range(volts, lo=0, hi=0):
    lo_i = 0
    hi_i = 0
    for i,j in enumerate(volts):
        if j < lo:
            lo_i = i
        if j < hi:
            hi_i = i
    return [lo_i,hi_i]

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
            fitNplot(f,data[i][0],data[i][1], T_LN)
        else:
            fitNplot(f,data[i][0],data[i][1], T)

plot(data(names))
analyse(data(names))
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