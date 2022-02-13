import numpy as np
from matplotlib import pyplot as plt


clearance = 0.1
thermalConductivity = 0.00018
heatCapacity = 1800
density = 0.96971e-6
MeltTemperature = 230.0
WallTemperature = 50.0
TransitionTemperature = 97.26
deltaP = 300e6
timeStepSize = 0.0001
numFourier = 50
n = 0.2354
Tau = 72350
D1 = 2.21489e12
D2 = 378.15
D3 = 0
A1 = 28.79
A2const = 51.6


def frozen(transitionTemperature, wallTemperature, timeList, clearance, alpha, Ti, numFourier):
    frozenLayer = []
    for time in timeList:
        xMin = 0
        xMax = clearance / 2
        x = (xMin + xMax) / 2
        temperatureTol = 10
        n = 0
        while temperatureTol > 0.00001 and n <= 30:
            temperatureX = temperature(time, clearance, alpha, Ti, x, numFourier) + wallTemperature
            if temperatureX < transitionTemperature:
                xMin = x
                x = (xMin + xMax) / 2
            else:
                xMax = x
                x = (xMin + xMax) / 2
            temperatureTol = abs(temperatureX - transitionTemperature)
            n += 1
        frozenLayer.append(x)
    return frozenLayer

def avgTemperature(time, thickness, alpha, Ti, numFourier):
    Temp0 = 0
    i = 0
    for i in range(numFourier):
        n=2*i+1
        Temp=(4*Ti/(n*(np.pi))**2)*(1-np.cos(n*(np.pi)))*np.exp(-n**2*(np.pi)**2*alpha*time/(thickness**2))
        Temp=Temp+Temp0
        Temp0=Temp
    return Temp

def temperature(time, thickness, alpha, Ti, x, numFourier):
    if type(x) == np.ndarray:
        numX = len(x)
        Temp0 = np.zeros(numX)
    else:
        Temp0 = 0
    i = 0
    for i in range(numFourier):
        n=2*i+1
        Temp=(4*Ti/(n*(np.pi)))*np.sin(n*(np.pi)*x/thickness)*np.exp(-n**2*(np.pi)**2*alpha*time/(thickness**2))
        Temp=Temp+Temp0
        Temp0=Temp
    return Temp

def plotFlash(x, y, labelY, title):
    plt.figure(title, figsize=(10, 6))
    plt.plot(x,y, marker='')
    plt.xlabel('Time(sec)')
    plt.ylabel(labelY)
    plt.title(title)
    plt.grid()
    plt.tight_layout()
    plt.show()

def calculate():
    def Mu(T, gamma):
        Mu0=D1*np.exp(-(A1*(T-Tg))/(A2+(T-Tg)))
        Mu=Mu0/(1+(((Mu0*gamma)/Tau)**pexp))
        return Mu

    meltTemperature = MeltTemperature
    wallTemperature = WallTemperature
    transitionTemperature = TransitionTemperature
    A2 = A2const

    P=50e6
    A2=A2+D3*P
    Tg=D2+D3*P
    pexp=1-n
    alpha = thermalConductivity / (density * heatCapacity)
    meltTemperature = meltTemperature + 273.15
    wallTemperature = wallTemperature + 273.15
    Ti = meltTemperature - wallTemperature
    transitionTemperature = transitionTemperature + 273.15

    timeToFrozen = clearance ** 2 / (np.pi ** 2 * alpha) * np.log(4*(meltTemperature - wallTemperature)/(np.pi * (transitionTemperature - wallTemperature)))
    numTime = int(timeToFrozen / timeStepSize)
    timeList = np.linspace(0, timeToFrozen, numTime)

    frozenLayerList = frozen(transitionTemperature, wallTemperature, timeList, clearance, alpha, Ti, numFourier)
    frozenLayerList = np.array(frozenLayerList)
    meltLayerList = clearance / 2 - frozenLayerList
    avgTemperatureList = avgTemperature(timeList, clearance, alpha, Ti, numFourier) + wallTemperature

    dt = timeList[1] - timeList[0]
    i = 0
    flashLength = 0
    flashLengthList = []
    uAvgList = []
    for time in timeList:
        meltLayer = (meltLayerList[i + 1] + meltLayerList[i]) / 2
        avgTemp = (avgTemperatureList[i + 1] + avgTemperatureList[i]) / 2
        pressure = deltaP * (time + dt / 2)

        dgamma = 1
        number = 0
        gamma_low = 0
        gamma_up = 50000

        while abs(dgamma) > 0.001 and number < 30:
            gamma = (gamma_low + gamma_up) / 2
            MuCrossWlf = Mu(avgTemp, gamma)
            uAvg = gamma * meltLayer / 3
            gamma0 = pressure * meltLayer / ((flashLength + uAvg * dt / 2) * MuCrossWlf)
            dgamma = gamma - gamma0
            if dgamma > 0:
                gamma_up = gamma
            else:
                gamma_low = gamma
            number += 1
        flashLength = flashLength + uAvg * dt
        flashLengthList.append(flashLength)
        uAvgList.append(uAvg)
        i += 1
        if i > len(timeList) - 2:
            break
    flashLengthList.append(flashLength)
    uAvgList.append(uAvg)

    plotFlash(timeList, frozenLayerList, 'Frozen layer(mm)', 'Frozen layer(mm) '  + ' (Gap = ' + str(clearance) + 'mm, dp/dt = ' + str(deltaP*1e-6) + 'MPa/s)')
    plotFlash(timeList, uAvgList, 'Average flash velocity(mm/s)', 'Average flash velocity(mm/s) ' + ' (Gap = ' + str(clearance) + 'mm, dp/dt = ' + str(deltaP*1e-6) + 'MPa/s)')
    plotFlash(timeList, flashLengthList, 'Flash length(mm)', 'Flash length(mm) ' + ' (Gap = ' + str(clearance) + 'mm, dp/dt = ' + str(deltaP*1e-6) + 'MPa/s)')

calculate()
