import csv
import numpy as np
import pickle
import sys
import time
import visa

from PyExpLabSys.drivers import tenma

rm = visa.ResourceManager()

amp = rm.open_resource(u'ASRL3::INSTR')
volt = rm.open_resource(u'ASRL4::INSTR')

volt.write(":SYST:REM")
amp.write(":SYST:REM")
volt.write("SAMP:COUN 10")
volt.write("TRIG:SOUR BUS")

amp.write("CONF:CURR:DC DEF")
amp.write("SAMP:COUN 10")
amp.write("TRIG:SOUR BUS")


ps = tenma.Tenma722535("COM6")
print(ps.com("*IDN?"))
print(ps.get_identification())
ps.set_output(False)


# ps.com("OUT0") # This is the hard way, in case their wrappers don't work
# ps.com("ISET1:0.33")
# ps.com("VSET1:0")
# ps.com("OCP1")


volts = []
amps = []
start = input("start: ")
stop = input("stop: ")
step = input("step: ")
s_type = str(input("Semiconductor type:"))

ps.set_voltage(0)
ps.set_current(0.33)
ps.set_overcurrent_protection(True)
ps.set_output(True)

for val in np.arange(start, stop, step):
    ps.set_voltage(val)
    volt.write("INIT")
    amp.write("INIT")
    volt.write("*TRG")
    amp.write("*TRG")
    time.sleep(5)
    volts.append(volt.query("FETC?"))
    amps.append(amp.query("FETC?"))

ps.set_output(False)
ps.close()
amp.close()
volt.close()


with open(str(s_type)+".csv", "w") as csvf:
    wr = csv.writer(csvf, delimiter=",", quotechar="|",
                    quoting=csv.QUOTE_MINIMAL)
    wr.writerow(volts)
    wr.writerow(amps)

with open(str(s_type+"_T"), "wb") as pick:
    pickle.dump(amps, pick)

with open(str(s_type+"V_T"), "wb") as pick:
    pickle.dump(volts, pick)
