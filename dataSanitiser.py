import json as js
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# with open('c:/Users/Caroline/Documents/Year 3/pnJunctions/pnJunctions/amps.json') as a:
#     amps = js.load(a)['values']

# with open('c:/Users/Caroline/Documents/Year 3/pnJunctions/pnJunctions/volts.json') as v:
#     volts = js.load(v)

amps = pd.read_json('c:/Users/Caroline/Documents/Year 3/pnJunctions/pnJunctions/amps.json')
volts = pd.read_json('c:/Users/Caroline/Documents/Year 3/pnJunctions/pnJunctions/volts.json')

ampAvgList = [np.mean(eval(i)) for i in amps['values']]
voltAvgList = [np.mean(eval(i)) for i in volts['values']]

table = pd.DataFrame({"amps": ampAvgList,"volts": voltAvgList})

plt.plot(table['volts'], np.log(table['amps']),'o')
plt.show()
print(table)