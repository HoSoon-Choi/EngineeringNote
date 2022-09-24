# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 15:56:29 2021

@author: Administrator
"""

import numpy as np
from matplotlib import pyplot as plt

def plotTait(taitValueList, meltTemperature):
    def specificVolume(pressure):
        Tt=b5+b6*pressure
        T0 = np.linspace(Tmin, Tt-5, numOfT)
        v00 = b1s + b2s*(T0 - b5)
        Bt0 = b3s*np.exp(-b4s*(T0-b5))
        vt0 = b7*np.exp((b8*(T0-b5))-b9*pressure)
        T1 = np.linspace(Tt, Tmax, numOfT)
        v01 = b1m + b2m*(T1 - b5)
        Bt1 = b3m*np.exp(-b4m*(T1-b5))
        vt1 = 0*T1
        T = np.hstack((T0,T1))
        v0 = np.hstack((v00,v01))
        Bt = np.hstack((Bt0,Bt1))
        vt = np.hstack((vt0,vt1))
        v = v0*(1-0.0894*np.log(1+pressure/Bt))+vt
        return T, v

    # plt.style.use('ggplot')
    plt.figure('Modified 2-states Tait pvT',figsize=(10, 6))

    b5=taitValueList[0]
    b6=taitValueList[1]
    b1m=taitValueList[2]
    b2m=taitValueList[3]
    b3m=taitValueList[4]
    b4m=taitValueList[5]
    b1s=taitValueList[6]
    b2s=taitValueList[7]
    b3s=taitValueList[8]
    b4s=taitValueList[9]
    b7=taitValueList[10]
    b8=taitValueList[11]
    b9=taitValueList[12]

    incP =20e6
    Pmax = 150e6
    P=np.arange(0,Pmax+incP,incP)



    Tmax=float(meltTemperature) + 50
    Tmin=25

    Tmax=Tmax+273.15
    Tmin=Tmin+273.15

    numOfT=20

    legend=[]
    for pressure in P:
        T, v = specificVolume(pressure)
        plt.plot(T-273.15, v*1000, marker='')
        legend.append('Pressure = ' + str(pressure/1e6) + ' MPa')

    # print(T)
    # print(v*1000)

    plt.xlabel('Temperature(deg.C)')
    plt.ylabel('Specific Volume(cm^3/g)')
    plt.title('Modified 2 states Tait pvT')
    plt.grid()
    plt.legend(legend)
    plt.tight_layout()
    plt.show()

# valueList=[370.44, 2.93e-07, 0.0009492, 6.18e-07, 1.71629e+08, 0.00417, 0.0009492, 2.63e-07, 2.55823e+08, 0.003715, 0, 0, 0]
# valueList=[406.58, 1.54e-07, 0.001261, 9.69e-07, 1.00193e+08, 0.004471, 0.001106, 5.48e-07, 2.30357e+08, 0.00406, 0.0001548, 0.1028, 3.38e-08]
# valueList=[457.15, 2.15e-07, 0.0008158, 4.297e-07, 2.15685e+08, 0.003674, 0.0007807, 3.222e-07, 3.00277e+08, 0.003115, 3.506e-05, 0.1281, 2.958e-08]
# valueList=[443.15, 7.8e-08, 0.001122, 8.049e-07, 8.90856e+07, 0.005472, 0.001029, 4.384e-07, 1.56282e+08, 0.005191, 9.311e-05, 0.04078, 7.513e-09]
valueList=[365.47, 2.33e-07, 0.0009688, 6.14e-07, 2.03682e+08, 0.005266, 0.000969, 3.03e-07, 2.5453e+08, 0.004351, 0, 0, 0]
meltTemp=280

plotTait(valueList, meltTemp)