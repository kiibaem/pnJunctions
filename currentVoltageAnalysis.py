import loadData as ld
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op

e = 1.602e-19
kB = 1.3806e-23

T = 295.6
T_LN = 79.5
sigmaT = 0.05

epsilon0 = 8.854e-12
epsilonr = 11.68

def f(volts_s, m, c):
     vals = m*volts_s + c
     return vals

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

def part1i(data):
    results = pd.DataFrame(columns = dict.keys(data))
    for i in dict.keys(data):
        volts = data[i][0]
        amps = data[i][1]
        lnamps = np.log(amps)
        lnerrs = [amps[i]**(-1)*ld.currentErr(amps)[i] for i in range(len(amps))]
        volterrs = ld.voltageErr(volts)
        dat_start = min(np.where(amps >= 0.02)[0])
        dat_range = [dat_start,dat_start+20]
        if 'LN' in i:
            T = T_LN
        if dat_range == 0:
            plt.figure()
            plt.plot(volts,lnamps,'o')
            plt.title(i)
            plt.ylabel('Ln(current)')
            plt.xlabel('Voltage (V)')
        else:
            lnamps_s = lnamps[dat_range[0]:dat_range[1]]
            volts_s = volts[dat_range[0]:dat_range[1]]
            lnamperrs_s = lnerrs[dat_range[0]:dat_range[1]]
            volterrs_s = volterrs[dat_range[0]:dat_range[1]]
            plt.figure()
            plt.errorbar(volts_s, lnamps_s,xerr=volterrs_s,yerr=lnamperrs_s,fmt='o')
            fit = op.curve_fit(f, volts_s, lnamps_s, sigma=lnamperrs_s, absolute_sigma=True, check_finite=False)
            line = [fit[0][0]*i+fit[0][1] for i in volts_s]
            plt.plot(volts_s,line,'-')
            plt.title(i)
            plt.ylabel('Ln(current)')
            plt.xlabel('Voltage (V)')
            perr = np.sqrt(np.diag(fit[1]))
            results[i] = pd.Series([n(fit[0][0],T),nerr(fit[0][0],perr[0],T),i0(fit[0][1]),i0err(fit[0][1],perr[1])], index= ['n','n error','I_0','I_0 error'])
    plt.show()
    print(results)

def part2ii(data):
    results = pd.DataFrame(columns = dict.keys(data))
    sqFitVals = []
    for i in dict.keys(data):
        volts = data[i][0][1:]
        capacitance = data[i][1][1:]
        voltErrs = ld.voltageErr(volts)
        capErrs = ld.capacitanceErr(capacitance)

        invCapSq = [i**(-2) for i in capacitance]
        invCapSqErr = [invCapSq[i]**(-3)*capErrs[i] for i in range(len(capErrs))]

        invCapCb = [i**(-3) for i in capacitance]
        invCapCbErr = [invCapCb[i]**(-4)*capErrs[i] for i in range(len(capErrs))]

        fitCube = op.curve_fit(f,volts,invCapCb,sigma=invCapCbErr,absolute_sigma=True,p0=[invCapCb[1],invCapCb[1]])
        cubeLine = [fitCube[0][0]*i+fitCube[0][1] for i in volts]
        cbErr = np.sqrt(np.diag(fitCube[1])[0])

        fitSquare = op.curve_fit(f,volts,invCapSq,sigma=invCapSqErr,absolute_sigma=True,p0=[invCapSq[1],invCapSq[1]])
        squareLine = [fitSquare[0][0]*i+fitSquare[0][1] for i in volts]
        sqErr = np.sqrt(np.diag(fitSquare[1])[0])
        Nval = N(fitSquare[0][0],2e-6)
        Vtval = Vt(fitSquare[0][1],Nval,2e-6)
        results[i] = pd.Series([cbErr,sqErr,Nval,Vtval], index = ['Error on cubic','Error on square', 'Value of N', 'Value of Vt'])
        sqFitVals.append(fitSquare[0])

        plt.figure()
        plt.title(i + 'Cubic approximation')
        plt.errorbar(volts,invCapCb,yerr=invCapCbErr,xerr=voltErrs,fmt='o')
        plt.plot(volts,cubeLine,'-')
        plt.xlabel('Volts (V)')
        plt.ylabel('1/C^3 (C^-3)')

        plt.figure()
        plt.title(i + 'Square approximation')
        plt.errorbar(volts,invCapSq,yerr=invCapSqErr,xerr=voltErrs,fmt='o')
        plt.plot(volts,squareLine,'-')
        plt.xlabel('Volts (V)')
        plt.ylabel('1/C^2 (C^-2)')

    print(results)
    plt.show()
    return sqFitVals

def N(m,A):
    N = 2./((A**(2))*e*epsilon0*epsilonr*m)
    return N

def Vt(c,N,A):
    Vt = (A**2*e*epsilon0*epsilonr*N*c)/2.
    return Vt

#part1i(ld.diode_data)
#part2ii(ld.cap_data)
part2ii(ld.cap_data)
#ld.plotIV(ld.diode_data)
#ld.plotCV(ld.cap_data)