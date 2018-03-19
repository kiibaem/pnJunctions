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
diode_ranges = [[100,200],[100,200],[100,200],[100,200],[100,200],[100,200],[100,200],[100,200],[100,200],[100,200]]
LED_names = ['LEDREDRT', 'LEDREDRT2', 'LEDREDRT3', 'LEDREDRT4', 'LEDYELLOWRT', 'LEDYELLOWRT2', 'LEDYELLOWRT3', 'LEDREDRT5', 'LEDGREENRT']
Si_diode_names = ['blackSiCap', 'redSiCap']

def data(names):
    results = {}
    if type(names)==str:
        names = [names]
    for i,j in enumerate(names):
        with open(j+'V', 'rb') as pick:
            results[j] = [pi.load(pick, fix_imports=True)]
        with open(j, 'rb') as pick:
            results[j].append(pi.load(pick,fix_imports=True))
        if results[j][0][0] > results[j][0][-1]:
            results[j][1] = results[j][1][::-1]
            results[j][0] = results[j][0][::-1]
    return(results)

def currentErr(amps):
    errs = [0.001*i + 0.0001*1 for i in amps]
    return errs

def voltageErr(volts):
    errs = [0.000035*i +0.000005*10 for i in volts]
    return errs

def capacitanceErr(farads):
    errs = [np.sqrt(17)*(2*0.1)*0.01*i for i in farads]
    return errs

def plotIV(data):
    for i in dict.keys(data):
        xerrs = voltageErr(data[i][0])
        yerrs = currentErr(data[i][1])
        plt.figure()
        plt.errorbar(data[i][0],data[i][1],yerr=yerrs,xerr=xerrs,fmt = 'o')
        plt.title(i)
        plt.xlabel('Potential difference (V)')
        plt.ylabel('Current (A)')
    plt.show()

def plotCV(data):
    for i in dict.keys(data):
        xerrs = voltageErr(data[i][0])
        yerrs = capacitanceErr(data[i][1])
        plt.figure()
        plt.errorbar(data[i][0],data[i][1],yerr=yerrs,xerr=xerrs,fmt = 'o')
        plt.title(i)
        plt.xlabel('Potential difference (V)')
        plt.ylabel('Capacitance (F)')
    plt.show()

diode_data = data(diode_names)
LED_data = data(LED_names)
cap_data = data(Si_diode_names)

