# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 15:56:29 2021

@author: Administrator
"""

import numpy as np
from matplotlib import pyplot as plt

def crossWlf(crossWlfValueList, meltTemperature):

    def Mu(T, gamma):
        Mu0=D1*np.exp(-(A1*(T-Tg))/(A2+(T-Tg)))
        Mu=Mu0/(1+(((Mu0*gamma)/Tau)**pexp))
        return Mu
        
    print(crossWlfValueList)
    n = crossWlfValueList[0]
    Tau = crossWlfValueList[1]
    D1 = crossWlfValueList[2]
    D2 = crossWlfValueList[3]
    D3 = crossWlfValueList[4]
    A1 = crossWlfValueList[5]
    A2 = crossWlfValueList[6]
    P = 50e6
    A2 = A2 + D3*P
    Tg = D2 + D3*P
    pexp = 1 - n
    Tmax = float(meltTemperature) + 273.15
    Tmin = float(meltTemperature) + 273.15
    incT = 10
    incGamma = 10
    T = np.arange(Tmin, Tmax + incT, incT)
    gamma=np.arange(0,5e4+incGamma,incGamma)
    legend=[]
    plt.figure('Cross WLF Viscosity', figsize=(10, 6))
    for temperature in T:
        plt.plot(gamma, Mu(temperature,gamma), marker='')
        legend.append('T = ' + str(temperature - 273.15) + ' deg.C')

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Shear rate(1/s)')
    plt.ylabel('Viscosity(Pa.s)')
    plt.title('Cross WLF Viscosity')
    plt.grid()
    plt.legend(legend)
    plt.tight_layout()
    plt.show()
    print('OK')
    return

valueList=[0.2354, 72350, 2.21489e12, 378.15, 0, 28.79, 51.6]
meltTemp=230
# valueList=[0.2718, 26260, 4.44489e+14, 263.15, 0, 32.71, 51.6]
# meltTemp=240
# valueList=[0.3309, 139000, 9.97264e+18, 323.15, 0, 46.56, 51.6]
# meltTemp=290
crossWlf(valueList, meltTemp)
