import pickle
import numpy
import matplotlib.pyplot as plt

files1 = ['LEDREDRT','LEDREDRT2','LEDREDRT3','LEDREDRT4','LEDREDRT5','LEDYELLOWRT','LEDYELLOWRT2','LEDYELLOWRT3','LEDGREENRT']

for FILE in files1:

    with open(FILE, "rb") as pick:
        amps = pickle.load(pick)

    with open(FILE + "V", "rb") as pick:
        volts = pickle.load(pick)


    #am = numpy.mean(amps, axis=1)

    #vm = numpy.mean(volts, axis=1)
    plt.figure()
    plt.xkcd()
    plt.title(FILE)
    plt.xlabel('Volts (V)')
    plt.ylabel('Current (A)')
    plt.plot(volts, amps, 'b-')
    # plt.savefig(FILE +".png")
plt.show()
