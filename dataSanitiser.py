import json as js

with open('c:/Users/Caroline/Documents/Year 3/pnJunctions/pnJunctions/amps.json', 'r') as a:
    amps = js.load(a)

with open('c:/Users/Caroline/Documents/Year 3/pnJunctions/pnJunctions/volts.json', 'r') as v:
    volts = js.load(v)

amps = [i.strip("\r\n") for i in amps]
amps = [i.strip("u'") for i in amps]

print(amps)