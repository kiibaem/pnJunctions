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

with open('SiLN') as pick:
    SiLN = pi.load(pick)
with open('SiLNV') as pick:
    SiLNV = pi.load(pick)
with open('SiRT') as pick:
    SiRT = pi.load(pick)
with open('SiRTV') as pick:
    SiRTV = pi.load(pick)


#In order: GaAs, Ge, Si (room temp values)

names = ['GaAs(RT)', 'Ge(RT)', 'Si(RT)'] #79.5K -N

def f(volts_s, m, c):
    vals = m*volts_s + c
    return vals

def fitNplot(f,amps,volts,range,T):
    lnamps = np.log(amps)
    lnamps_s = lnamps[range[0]:range[1]]
    volts_s = volts[range[0]:range[1]]
    fit = op.curve_fit(f, volts_s, lnamps_s)
    line = [fit[0][0]*i+fit[0][1] for i in volts_s]
    plt.figure()
    plt.plot(volts_s, lnamps_s, 'o')
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

def val_range(volts, lo, hi):
    lo_i = 0
    hi_i = 0
    for i,j in enumerate(volts):
        if j < lo:
            lo_i = i
        if j < hi:
            hi_i = i
    return [lo_i,hi_i]

# Silicon, room temp
plt.figure()
plt.plot(SiRT, SiRTV, 'o')

# Silicon, 79K
plt.figure()
plt.plot(SiLN, SiLNV, 'o')

fitNplot(f,SiLN,SiLNV,val_range(SiLNV, 0.66, 1.1),T_LN)
fitNplot(f,SiRT,SiRTV,val_range(SiLNV, 0.66, 1.1),T) 
#fitNplot(f,SiLN,SiLNV,val_range(SiLNV, 0.66, 1.1)) 
plt.show()