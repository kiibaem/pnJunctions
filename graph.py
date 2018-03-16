import pickle
import numpy
import matplotlib.pyplot as plt


FILE = input("Enter base file name")

with open(FILE, "rb") as pick:
    amps = pickle.load(pick)

with open(FILE + "V", "rb") as pick:
    volts = pickle.load(pick)


am = numpy.mean(amps, axis=1)

vm = numpy.mean(volts, axis=1)

plt.plot(vm, am, 'bo')
plt.savefig("GaAsRT.png")
plt.show()
