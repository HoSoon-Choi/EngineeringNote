import numpy as np
from matplotlib import pyplot as plt

waterTable = [['0', '9.99844E-07', '4216.1076', '1.75241E-09', '0.000568708', '1.75268219'], ['4.444444444', '9.99844E-07', '4203.5472', '1.54652E-09', '0.000578054', '1.546765976'], ['10', '9.99844E-07', '4195.1736', '1.30234E-09', '0.000587053', '1.302539769'], ['15.55555556', '9.99203E-07', '4186.8', '1.12518E-09', '0.000597092', '1.126077664'], ['21.11111111', '9.98082E-07', '4182.6132', '9.76752E-10', '0.000605745', '0.978629422'], ['26.66666667', '9.968E-07', '4178.4264', '8.47476E-10', '0.000612668', '0.85019651'], ['32.22222222', '9.94878E-07', '4178.4264', '7.6608E-10', '0.000621321', '0.770024079'], ['37.77777778', '9.93116E-07', '4178.4264', '6.79896E-10', '0.000628763', '0.684608847'], ['43.33333333', '9.91194E-07', '4182.6132', '6.03288E-10', '0.000635167', '0.60864785'], ['48.88888889', '9.88791E-07', '4182.6132', '5.45832E-10', '0.00064209', '0.552019509'], ['54.44444444', '9.85748E-07', '4182.6132', '5.0274E-10', '0.000647282', '0.510008788'], ['60', '9.83345E-07', '4182.6132', '4.59648E-10', '0.000654205', '0.467433089'], ['65.55555556', '9.80302E-07', '4186.8', '4.26132E-10', '0.000658704', '0.434694792'], ['71.11111111', '9.77258E-07', '4190.9868', '3.97404E-10', '0.000662858', '0.406652007'], ['76.66666667', '9.73734E-07', '4195.1736', '3.68676E-10', '0.00066805', '0.37862077'], ['82.22222222', '9.7021E-07', '4199.3604', '3.44736E-10', '0.000671512', '0.355320918'], ['87.77777778', '9.66686E-07', '4203.5472', '3.25584E-10', '0.000674973', '0.336804194'], ['93.33333333', '9.62682E-07', '4207.734', '2.9925E-10', '0.000677742', '0.310850377']]

npTable = np.array(waterTable)
npTable = npTable.astype(np.float64)
npTable = npTable.transpose()
tableName = 'Water'

iDensity = 1
iCapacity = 2
iViscosity = 3
iConductivity = 4
iDViscosity = 5

thickness = 2
density = 1.1015e-6
thermalConductivity = 0.00024
heatCapacity = 1900
meltTemperature = 300.0
wallTemperature = 100.0
coolantTemperature = 35.0
# channelWallTemperature = 35.0
ejectionTemperature = 127
thermalConductance = 0.03
moldThermalConductivity = 0.03
channelDiameter = 8.0
lengthToChannelCenter = 15.0
flowRateCoolant = 5.0
waterTemperatureDelta = 5.0

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

def properties(temperature):

    jindex, fraction = jAndFraction(temperature)

    density = interPolation(iDensity, jindex, fraction)
    viscosity = interPolation(iViscosity, jindex, fraction)
    capacity = interPolation(iCapacity, jindex, fraction)
    conductivity = interPolation(iConductivity, jindex, fraction)
    prandtl = capacity * (viscosity * 1000) / conductivity

    return density, viscosity, capacity, conductivity, prandtl

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

def plotHeatEq(thickness, density, thermalConductivity, heatCapacity, meltTemperature, wallTemperature, timeMax, numTime, numX, numFourier, title):

    alpha=thermalConductivity/(heatCapacity*density)
    Ti=meltTemperature-wallTemperature
    time = np.linspace(0, timeMax, numTime)
    x = np.linspace(0, thickness, numX)
    plt.figure('Heat Equation', figsize=(10, 6))
    legend=[]
    for t in time:
        temperatureProd = temperature(t, thickness, alpha, Ti, x, numFourier) + wallTemperature
        plt.plot(x,temperatureProd, marker='')
        legend.append('Time = ' + str(t) + ' sec')
    plt.xlabel('Thickness(mm)')
    plt.ylabel('Temperature(deg.C)')
    plt.title(title)
    plt.grid()
    plt.legend(legend)
    plt.tight_layout()
    plt.show()
    
def HTC(temperature, channelDia, qcoolant):

    density, viscosity, capacity, conductivity, prandtl = properties(temperature)

    yReynold = density * (qcoolant * 1000000 * 4 / (60 * np.pi * channelDia**2)) * channelDia / (viscosity * 1000)
    yNusselt = 0.023 * yReynold ** 0.8 * prandtl ** 0.4
    yHTC = conductivity * yNusselt / channelDia
    return yHTC, capacity, density



def calculate():

    kp = thermalConductivity
    cp = heatCapacity
    rho = density
    Tm = meltTemperature
    Tw = wallTemperature
    Te = ejectionTemperature
    h = thermalConductance
    km = moldThermalConductivity
    dia = channelDiameter
    lToCenter = lengthToChannelCenter
    Tc = coolantTemperature
    # Tc = channelWallTemperature
    qcoolant = flowRateCoolant
    Tdelta = waterTemperatureDelta
    htc, heatCapacityWater, densityWater = HTC(Tc, dia, qcoolant)

    alpha = kp / (cp * rho)
    taverage = thickness ** 2 / (np.pi ** 2 * alpha) * np.log(8*(Tm - Tw)/(np.pi ** 2 * (Te - Tw)))
    qaverage = rho * cp * (Tm - Te ) * thickness / (2 * taverage)
    TwmAverage = Tw - qaverage / h
    TcwAverage = Tc + qaverage / htc
    AratioAverage = qaverage * lToCenter / (km * (TwmAverage - TcwAverage))
    channelPitchAverage = np.pi * dia / AratioAverage
    areaAverage = heatCapacityWater * densityWater * qcoolant * (1e6 / 60) * Tdelta / qaverage

    tcenter = thickness ** 2 / (np.pi ** 2 * alpha) * np.log(4*(Tm - Tw)/(np.pi * (Te - Tw)))
    TCenterAvg = 8 * (Tm - Tw) * thickness / np.pi ** 2 * np.exp(-np.pi**2 * alpha * tcenter / thickness ** 2)
    qcenter = rho * cp * (Tm - TCenterAvg ) * thickness / (2 * tcenter)
    TwmCenter = Tw - qcenter / h
    TcwCeneter = Tc + qcenter / htc
    AratioCeneter = qcenter * lToCenter / (km * (TwmCenter - TcwCeneter))
    channelPitchCeneter = np.pi * dia / AratioCeneter
    areaCeneter = heatCapacityWater * densityWater * qcoolant * (1e6 / 60) * Tdelta / qcenter
    numTime = 11
    numX = 300
    numFourier = 300
    title = 'Cooling time for center temperature = '+str(format(tcenter, '.3f'))+'sec'+', '+'Channel pitch = '+str(format(channelPitchCeneter, '.3f'))+'mm'+'\n'+'Channel wall temperature = '+str(format(TcwCeneter, '.3f'))+'Deg.C'+', '+'Heat flux = '+str(format(qcenter, '.6f'))+'W/mm^2'+'\n'+'Area possible in 1 circuit = '+str(format(areaCeneter, '.3f'))+'mm^2'+', '+'HTC = '+str(format(htc, '.6f'))+'W/mm^2 Deg.C'
    plotHeatEq(thickness, density, thermalConductivity, heatCapacity, meltTemperature, wallTemperature, tcenter, numTime, numX, numFourier, title)
    title = 'Cooling time for average temperature = '+str(format(taverage, '.3f'))+'sec'+', '+'Channel pitch = '+str(format(channelPitchAverage, '.3f'))+'mm'+'\n'+'Channel wall temperature = '+str(format(TcwAverage, '.3f'))+'Deg.C'+', '+'Heat flux = '+str(format(qaverage, '.6f'))+'W/mm^2'+'\n'+'Area possible in 1 circuit = '+str(format(areaAverage, '.3f'))+'mm^2'+', '+'HTC = '+str(format(htc, '.6f'))+'W/mm^2 Deg.C'
    plotHeatEq(thickness, density, thermalConductivity, heatCapacity, meltTemperature, wallTemperature, taverage, numTime, numX, numFourier, title)

calculate()

