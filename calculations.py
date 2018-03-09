import numpy as np 
import pandas as pd

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

names = ['GaAs(RT)', 'Ge(RT)', 'Si(RT)']

def n(slopes):
    ns = [(e)/(i*kB*T*1000) for i in slopes]
    return ns

def nerr(slopes,slopeErrs):
    nerrs = [np.sqrt((e/(slopes[i]*kB*T**2*1000))*sigmaT**2 + (e/(slopes[i]**2*kB*T*1000)*slopeErrs[i]**2)) for i in range(len(slopes))]
    return nerrs

def i0(icepts):
    i0s = [np.exp(i) for i in icepts]
    return i0s

def i0err(icepts,iceptErrs):
    i0errs = [np.exp(icepts[i])*iceptErrs[i] for i in range(len(icepts))]
    return i0errs

RTframe = pd.DataFrame({'I_0': pd.Series(i0(icepts), names), 'I_0 err': pd.Series(i0err(icepts,iceptErrs),names),'n': pd.Series(n(slopes), names), 'n err': pd.Series(nerr(slopes,slopeErrs),names)})

print(RTframe)
