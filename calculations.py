import numpy as np 
import pandas as pd
import scipy.optimize as op
import dataSanitiser as ds
import matplotlib.pyplot as plt

e = 1.602e-19
kB = 1.3806e-23

T = 295.6
sigmaT = 0.05

GaAsDat = pd.read_csv('c:/Users/Caroline/Documents/Year 3/pnJunctions/pnJunctions/GaAsRTdat.csv')
GeDat = pd.read_csv('c:/Users/Caroline/Documents/Year 3/pnJunctions/pnJunctions/GeRTdat.csv')
SiDat = pd.read_csv('c:/Users/Caroline/Documents/Year 3/pnJunctions/pnJunctions/SiRTdat.csv')
#print(GaAsDat, GeDat, SiDat)

#In order: GaAs, Ge, Si (room temp values)
slopes = [0.02153, 0.03148, 0.01981] #0.01504,0.02397,0.02004
slopeErrs = [2.92e-4, 0.00168, 3.557e-4]

icepts = [-16.63342, -6.32938, -12.59333]
iceptErrs = [0.30161, 0.18847, 0.20177]

names = ['GaAs(RT)', 'Ge(RT)', 'Si(RT)'] #79.5K -N

def f(volts_s, m, c):
    vals = m*volts_s + c
    return vals

def fitNplot(f,amps,volts,range):
    lnamps = np.log(amps)
    lnamps_s = lnamps[range[0]:range[1]]
    volts_s = volts[range[0]:range[1]]
    fit = op.curve_fit(f, volts_s, lnamps_s)
    line = [fit[0][0]*i+fit[0][1] for i in volts_s]
    plt.plot(volts_s, lnamps_s, 'o')
    plt.plot(volts_s,line, '-')
    perr = np.sqrt(np.diag(fit[1]))
    val_err = nerr(fit[0][0],perr[0])
    print("Value of n: %g" % n(fit[0][0]), "Error on n: %g" % val_err, "Value of I_0: %g A" % i0(fit[0][1]), "Error on I_0: %g" % i0err(fit[0][1],perr[1]))

def n(slope):
    ns = (e)/(slope*kB*T)
    return ns

def nerr(slope,slopeErr):
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

#RTframe = pd.DataFrame({'I_0': pd.Series(i0(icepts), names), 'I_0 err': pd.Series(i0err(icepts,iceptErrs),names),'n': pd.Series(n(slopes), names), 'n err': pd.Series(nerr(slopes,slopeErrs),names)})

fitNplot(f,ds.ampAvgList,ds.voltAvgList,val_range(ds.voltAvgList, 0.66, 1.1)) 
plt.show()