import numpy as np
from matplotlib import pyplot as plt

n=0.2354
Tau=72350
D1=2.21489e12
D2=378.15
D3=0
A1=28.79
A2=51.6

P=50e6
A2=A2+D3*P
Tg=D2+D3*P
pexp=1-n

def Mu(T, gamma):
    Mu0=D1*np.exp(-(A1*(T-Tg))/(A2+(T-Tg)))
    Mu=Mu0/(1+(((Mu0*gamma)/Tau)**pexp))
    return Mu

def pressureDrop(diameter, length, flowRate, meltTemperature):
    shearRate = 32 * flowRate / (np.pi * diameter ** 3)
    viscosity = Mu(meltTemperature, shearRate)
    print(viscosity)
    pDropPerLength = 2 * viscosity * shearRate / 8
    pDropTotal = pDropPerLength * length * 1e-6
    return pDropTotal

meltTemperature = 230+273.15

diameter = np.linspace(10, 22, 12)

print(pressureDrop(diameter, 200, 200e3, meltTemperature))
plt.figure('Pressure drop for runner diameter change (runner length=200mm)',figsize=(10, 6))
plt.plot(diameter, pressureDrop(diameter, 200, 200e3, meltTemperature), marker='')
plt.xlabel('Runner diameter(mm)')
plt.ylabel('Pressure drop(MPa)')
plt.title('Pressure drop for runner diameter change (runner length=200mm)')
plt.grid()
plt.tight_layout()
plt.show()
