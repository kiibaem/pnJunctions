import csv
# import matplotlib.pyplot as plt
import numpy as np
import pickle

# Constant to make it easier to work on a single dataset at a time
#FILE=str(input("Enter file base name:"))
files1 = ['LEDREDRT','LEDREDRT2','LEDREDRT3','LEDREDRT4','LEDREDRT5','LEDYELLOWRT','LEDYELLOWRT2','LEDYELLOWRT3','LEDGREENRT']
files2 = ['blackSiCap', 'redSiCap']

for FILE in files2:
    # Open up the raw DMM data
    with open(FILE+"_T", "rb") as pick:
        amps = pickle.load(pick)
        if type(amps) == list:
            amps = np.array(amps)
            PROCESSED = True

    with open(FILE+"V_T", "rb") as pick:
        volts = pickle.load(pick)
        if type(volts) == list:
            volts = np.array(volts)

    # This may need a little work, but this is where we clean up the formatting
    # of the DMM data and get it back into np arrays
    if not PROCESSED:
        a1 = [i[:-2] for i in amps]
        a2 = [i.split(",") for i in a1]
        amps = np.array(a2, dtype=float)

        v1 = [i[:-2] for i in volts]
        v2 = [i.split(",") for i in v1]
        volts = np.array(v2, dtype=float)

    # Take the mean of each set of repeats
    am = np.mean(amps, axis=1)
    vm = np.mean(volts, axis=1)

    # Save it back to file so we can work with it again
    with open(FILE, "wb") as pick:
        pickle.dump(am, pick)

    with open(FILE+"V", "wb") as pick:
        pickle.dump(vm, pick)

    #plt.plot(vm, am, 'bo')
    #plt.show()

def savetocsv():
    with open(FILE + ".csv", "w") as csvf:
        wr = csv.writer(csvf)
        for row in amps:
            wr.writerow(row)

    with open(FILE+"V.csv", "w") as csvf:
        wr = csv.writer(csvf)
        for row in volts:
            wr.writerow(row)
    
    return