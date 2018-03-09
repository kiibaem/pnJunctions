import numpy as np 
import pandas as pd

e = 1.602e-19
kB = 1.3806e-23
T = 295.6



#In order: GaAs, Ge, Si
slopes = [0.01504, 0.02397, 0.02004]
icepts = [-16.63342, -6.32938, -12.59333]
names = ['GaAs(RT)', 'Ge(RT)', 'Si(RT)']

def n(slopes):
    ns = [(e)/(i*kB*T*1000) for i in slopes]
    return ns

def i0(icepts):
    i0s = [np.exp(i) for i in icepts]
    return i0s

RTframe = pd.DataFrame({'I_0': pd.Series(i0(icepts), names), 'n': pd.Series(n(slopes), names)})

print(RTframe)
print(e/(kB*T*1000), 1./26.)