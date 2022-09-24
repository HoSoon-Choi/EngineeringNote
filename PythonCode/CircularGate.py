import numpy as np
from matplotlib import pyplot as plt

def circularGate(diameter, flowRate):
    shearRate = 32 * flowRate / (np.pi * diameter ** 3)
    return shearRate

meltTemperature = 230+273.15

diameter1 = np.linspace(2, 6, 100)

plt.figure('Shear rate for gate diameter change',figsize=(10, 6))
plt.plot(diameter1, circularGate(diameter1, 200e3), marker='')
plt.xlabel('Gate diameter(mm)')
plt.ylabel('Shear rate(1/s)')
plt.title('Shear rate for gate diameter change')
plt.grid()
plt.tight_layout()
plt.show()
