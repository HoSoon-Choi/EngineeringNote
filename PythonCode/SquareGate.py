import numpy as np
from matplotlib import pyplot as plt

def squareGate(thickness, width, flowRate):
    shearRate = 6 * flowRate / (width * thickness ** 2)
    return shearRate

meltTemperature = 230+273.15

thickness = np.linspace(0.5, 2, 100)
plt.figure('Shear rate for gate thickness change',figsize=(10, 6))
plt.plot(thickness, squareGate(thickness, 10, 200e3), marker='')
plt.xlabel('Gate thickness(mm)')
plt.ylabel('Shear rate(1/s)')
plt.title('Shear rate for gate thickness change')
plt.grid()
plt.tight_layout()
plt.show()
