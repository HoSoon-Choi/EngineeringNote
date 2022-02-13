import numpy as np
from matplotlib import pyplot as plt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

waterTable = [['0', '9.99844E-07', '4216.1076', '1.75241E-09', '0.000568708', '1.75268219'], ['4.444444444', '9.99844E-07', '4203.5472', '1.54652E-09', '0.000578054', '1.546765976'], ['10', '9.99844E-07', '4195.1736', '1.30234E-09', '0.000587053', '1.302539769'], ['15.55555556', '9.99203E-07', '4186.8', '1.12518E-09', '0.000597092', '1.126077664'], ['21.11111111', '9.98082E-07', '4182.6132', '9.76752E-10', '0.000605745', '0.978629422'], ['26.66666667', '9.968E-07', '4178.4264', '8.47476E-10', '0.000612668', '0.85019651'], ['32.22222222', '9.94878E-07', '4178.4264', '7.6608E-10', '0.000621321', '0.770024079'], ['37.77777778', '9.93116E-07', '4178.4264', '6.79896E-10', '0.000628763', '0.684608847'], ['43.33333333', '9.91194E-07', '4182.6132', '6.03288E-10', '0.000635167', '0.60864785'], ['48.88888889', '9.88791E-07', '4182.6132', '5.45832E-10', '0.00064209', '0.552019509'], ['54.44444444', '9.85748E-07', '4182.6132', '5.0274E-10', '0.000647282', '0.510008788'], ['60', '9.83345E-07', '4182.6132', '4.59648E-10', '0.000654205', '0.467433089'], ['65.55555556', '9.80302E-07', '4186.8', '4.26132E-10', '0.000658704', '0.434694792'], ['71.11111111', '9.77258E-07', '4190.9868', '3.97404E-10', '0.000662858', '0.406652007'], ['76.66666667', '9.73734E-07', '4195.1736', '3.68676E-10', '0.00066805', '0.37862077'], ['82.22222222', '9.7021E-07', '4199.3604', '3.44736E-10', '0.000671512', '0.355320918'], ['87.77777778', '9.66686E-07', '4203.5472', '3.25584E-10', '0.000674973', '0.336804194'], ['93.33333333', '9.62682E-07', '4207.734', '2.9925E-10', '0.000677742', '0.310850377']]

npTable = np.array(waterTable)
npTable = npTable.astype(np.float64)
npTable = npTable.transpose()
tableName = 'Water'

iDensity = 1
iConductivity = 4
iCapacity = 2
iViscosity = 3
iDViscosity = 5

sizeX = 6.35
sizeY = 4.5

temperature = 25
channelDia = 10
minFlowRate = 1
maxFlowRate = 10
numX = 100

def temperatureDependentProperties(npTable, tableName):

    figDensity = plt.figure(figsize=(sizeX,sizeY))
    densityAx = figDensity.subplots()
    densityAx.plot(npTable[0], npTable[1])
    densityAx.set(xlabel = 'Temperature(°C)', ylabel = 'Density(Kg/mm³)', title = 'Density - ' + tableName + ' (Kg/mm³)')
    densityAx.grid()
    figDensity.tight_layout()
    figDensity.canvas.manager.window.move(0, 0)

    figthermalConductivity = plt.figure(figsize=(sizeX,sizeY))
    thermalConductivityAx = figthermalConductivity.subplots()
    thermalConductivityAx.plot(npTable[0], npTable[4])
    thermalConductivityAx.set(xlabel = 'Temperature(°C)', ylabel = 'Thermal Conductivity(W/mm·°K)', title = 'Thermal Conductivity - ' + tableName + ' (W/mm·°K)')
    thermalConductivityAx.grid()
    figthermalConductivity.tight_layout()
    figthermalConductivity.canvas.manager.window.move(640, 0)

    figHeatCapacity = plt.figure(figsize=(sizeX,sizeY))
    heatCapacityAx = figHeatCapacity.subplots()
    heatCapacityAx.plot(npTable[0], npTable[2])
    heatCapacityAx.set(xlabel = 'Temperature(°C)', ylabel = 'Heat Capacity(J/Kg·°K)', title = 'Heat Capacity - ' + tableName + ' (J/Kg·°K)')
    heatCapacityAx.grid()
    figHeatCapacity.tight_layout()
    figHeatCapacity.canvas.manager.window.move(1280, 0)

    figViscosity = plt.figure(figsize=(sizeX,sizeY))
    viscosityAx = figViscosity.subplots()
    viscosityAx.plot(npTable[0], npTable[3])
    viscosityAx.set(xlabel = 'Temperature(°C)', ylabel = 'Viscosity(N·sec/mm²)', title = 'Viscosity - ' + tableName + ' (N·sec/mm²)')
    viscosityAx.grid()
    figViscosity.tight_layout()
    figViscosity.canvas.manager.window.move(0, 520)

    figDynamicViscosity = plt.figure(figsize=(sizeX,sizeY))
    dynamicViscosityAx = figDynamicViscosity.subplots()
    dynamicViscosityAx.plot(npTable[0], npTable[5])
    dynamicViscosityAx.set(xlabel = 'Temperature(°C)', ylabel = 'Dynamic Viscosity(mm²/sec)', title = 'Dynamic Viscosity - ' + tableName + ' (mm²/sec)')
    dynamicViscosityAx.grid()
    figDynamicViscosity.tight_layout()
    figDynamicViscosity.canvas.manager.window.move(640, 520)
#    plt.tight_layout()
#    plt.show()

def jAndFraction(temperature):
    j = 0
    deltaT = None
    for tableTemperature in npTable[0]:
        if tableTemperature < temperature:
            tableTemperature0 = tableTemperature
            j += 1
            pass
        else:
            deltaT = temperature - tableTemperature0
            intervalT = tableTemperature - tableTemperature0
            fraction = deltaT / intervalT
            j -= 1
            break
        
    return j, fraction

def interPolation(index, jindex, fraction):
    interpolationValue = npTable[index][jindex] + (npTable[index][jindex + 1] - npTable[index][jindex]) * fraction
    return interpolationValue

# temperatureDependentProperties(npTable, tableName)

jindex, fraction = jAndFraction(temperature)

density = interPolation(iDensity, jindex, fraction)
viscosity = interPolation(iViscosity, jindex, fraction)
capacity = interPolation(iCapacity, jindex, fraction)
conductivity = interPolation(iConductivity, jindex, fraction)

x = np.linspace(minFlowRate, maxFlowRate, numX)
yReynold = density * (x * 1000000 * 4 / (60 * np.pi * channelDia**2)) * channelDia / (viscosity * 1000)
prandtl = capacity * (viscosity * 1000) / conductivity
yNusselt = 0.023 * yReynold ** 0.8 * prandtl ** 0.4
yHTC = conductivity * yNusselt / channelDia

y = yReynold
figReynoldNumber = plt.figure(figsize=(sizeX,sizeY))
reynoldNumberAx = figReynoldNumber.subplots()
reynoldNumberAx.plot(x, y)
reynoldNumberAx.set(xlabel = 'Flow Rate(liter/min)', ylabel = 'Reynold Number', title = 'Reynold Number (temperature = ' + str(temperature) + '°C, channel dia. = ' + str(channelDia) + 'mm)')
reynoldNumberAx.grid()
figReynoldNumber.tight_layout()
# figReynoldNumber.canvas.manager.window.move(640, 520)

y = yNusselt
figNusseltNumber = plt.figure(figsize=(sizeX,sizeY))
nusseltNumberAx = figNusseltNumber.subplots()
nusseltNumberAx.plot(x, y)
nusseltNumberAx.set(xlabel = 'Flow Rate(liter/min)', ylabel = 'Nusselt Number', title = 'Nusselt Number (temperature = ' + str(temperature) + '°C, channel dia. = ' + str(channelDia) + 'mm)')
nusseltNumberAx.grid()
figNusseltNumber.tight_layout()
# figReynoldNumber.canvas.manager.window.move(640, 520)

y = yHTC
figHTC = plt.figure(figsize=(sizeX,sizeY))
hTCAx = figHTC.subplots()
hTCAx.plot(x, y)
hTCAx.set(xlabel = 'Flow Rate(liter/min)', ylabel = 'Heat Transfer Coefficient(W/mm²·°K)', title = 'HTC(W/mm²·°K) - Dittus-Boelter for (Re > 10,000)')
hTCAx.grid()
figHTC.tight_layout()
# figReynoldNumber.canvas.manager.window.move(640, 520)
plt.show()