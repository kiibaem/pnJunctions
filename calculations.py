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

with open('SiLN', 'rb') as pick:
    SiLN = pi.load(pick)
with open('SiLNV', 'rb') as pick:
    SiLNV = pi.load(pick)

with open('SiLN2', 'rb') as pick:
    SiLN2 = pi.load(pick)
with open('SiLN2V', 'rb') as pick:
    SiLN2V = pi.load(pick)

with open('SiRT', 'rb') as pick:
    SiRT = pi.load(pick)
with open('SiRTV', 'rb') as pick:
    SiRTV = pi.load(pick)

with open('GaAsLN', 'rb') as pick:
    GaAsLN = pi.load(pick)
with open('GaAsLNV', 'rb') as pick:
    GaAsLNV = pi.load(pick)

with open('GaAsRT', 'rb') as pick:
    GaAsRT = pi.load(pick)
with open('GaAsRTV', 'rb') as pick:
    GaAsRTV = pi.load(pick)

with open('GeLN', 'rb') as pick:
    GeLN = pi.load(pick)
with open('GeLNV', 'rb') as pick:
    GeLNV = pi.load(pick)

with open('GeRT', 'rb') as pick:
    GeRT = pi.load(pick)
with open('GeRTV', 'rb') as pick:
    GeRTV = pi.load(pick)


#In order: GaAs, Ge, Si (room temp values)

names = ['GaAs(RT)', 'Ge(RT)', 'Si(RT)'] #79.5K -N

def f(volts_s, m, c):
    vals = m*volts_s + c
    return vals

def fitNplot(f,amps,volts,range,T):
    lnamps = np.log(amps)
    lnamps_s = lnamps[range[0]:range[1]]
    volts_s = volts[range[0]:range[1]]
    plt.figure()
    plt.plot(volts_s, lnamps_s, 'o')
    # fit = op.curve_fit(f, volts_s, lnamps_s)
    # line = [fit[0][0]*i+fit[0][1] for i in volts_s]
    # plt.plot(volts_s,line, '-')
    # perr = np.sqrt(np.diag(fit[1]))
    # print("Value of n: %g" % n(fit[0][0],T), "Error on n: %g" % nerr(fit[0][0],perr[0],T), "Value of I_0: %g A" % i0(fit[0][1]), "Error on I_0: %g" % i0err(fit[0][1],perr[1]))

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
plt.figure()
plt.plot(SiRTV, SiRT, 'o')
plt.title('Si at room temperature')

# Silicon, 79K
plt.figure()
plt.plot(SiLNV, SiLN, 'o')
plt.title('Si in liquid nitrogen')

plt.figure()
plt.plot(SiLN2V, SiLN2, 'o')
plt.title('Si in liquid nitrogen')

# GaAs, 79K
plt.figure()
plt.plot(GaAsLNV, GaAsLN, 'o')
plt.title('GaAs in liquid nitrogen')

# GaAs, RT
plt.figure()
plt.plot(GaAsRTV, GaAsRT, 'o')
plt.title('GaAs at room temperature')

# Ge, 79K
plt.figure()
plt.plot(GeLNV, GeLN, 'o')
plt.title('Ge in liquid nitrogen')

# Ge, room temp
plt.figure()
plt.plot(GeRTV, GeRT, 'o')
plt.title('Ge at room temperature')

print('Silicon in liquid nitrogen')
fitNplot(f,SiLN,SiLNV,val_range(SiLNV, 0.99, 1.05),T_LN)
print('Silicon in liquid nitrogen 2')
fitNplot(f,SiLN2,SiLN2V,val_range(SiLN2V, 1.25, 1.6),T_LN)

print('Silicon at room temperature')
fitNplot(f,SiRT,SiRTV,val_range(SiRTV, 0.3, 0.74),T)

print('GaAs in liquid nitrogen')
fitNplot(f,GaAsLN,GaAsLNV,val_range(GaAsLNV, 1.48 ,2.1),T_LN)

print('GaAs at room temperature')
fitNplot(f,GaAsRT,GaAsRTV,val_range(GaAsRTV, 1.05, 1.18),T)

print('Ge in liquid nitrogen')
fitNplot(f,GeLN,GeLNV,val_range(GeLNV, 0.85, 1.03),T_LN)

print('Ge at room temperature')
fitNplot(f,GeRT,GeRTV,val_range(GeRTV, 0.40, 0.68),T)


plt.show()