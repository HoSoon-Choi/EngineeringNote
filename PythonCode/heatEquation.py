# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 15:56:29 2021

@author: Administrator
"""

import numpy as np
from matplotlib import pyplot as plt

def temperature(t):
    Temp0=np.zeros(numX)
    i=0
    for i in range(m):
        n=2*i+1
        Temp=(4*Ti/(n*(np.pi)))*np.sin(n*(np.pi)*x/thickness)*np.exp(-n**2*(np.pi)**2*alpha*t/(thickness**2))
        Temp=Temp+Temp0
        Temp0=Temp
    return Temp

# plt.style.use('ggplot')
plt.figure('Heat Equation', figsize=(10, 6))

rho=1.1015
k=0.00024
cp=1.9
alpha=k/(cp*rho/1000)
thickness=2.5
Tm=300
Tw=100
# Te=88

Ti=Tm-Tw
timeMax = 12.392
numTime = 10
# time = np.arange(0, timeMax + 1.5, 1.5)
time = np.linspace(0, timeMax, numTime)
numX = 300
m=300


x = np.linspace(0, thickness, numX)

legend=[]
for t in time:
    temperatureProd = temperature(t) + Tw
    plt.plot(x,temperatureProd, marker='')
    legend.append('Time = ' + str(t) + ' sec')


plt.xlabel('Thickness(mm)')
plt.ylabel('Temperature(deg.C)')
plt.title('Heat Equation')
plt.grid()
plt.legend(legend)
plt.tight_layout()
plt.show()