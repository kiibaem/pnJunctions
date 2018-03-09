import visa
import time
import sys
from PyExpLabSys.drivers import tenma

rm = visa.ResourceManager()

amp = rm.open_resource(u'ASRL3::INSTR')
volt = rm.open_resource( u'ASRL4::INSTR')

volt.write(":SYST:REM")
amp.write(":SYST:REM")
volt.write("SAMP:COUN 10")
volt.write("TRIG:SOUR BUS")

amp.write("CONF:CURR:DC DEF")
amp.write("SAMP:COUN 10")
amp.write("TRIG:SOUR BUS")


ps = tenma.Tenma722535("COM6")
ps.out("OUT0")

volts=[]
amps=[]
while True:
    inp = raw_input("command:")
    print(inp)
    if inp != "q":
        volt.write("INIT")
        amp.write("INIT")
        volt.write("*TRG")
        amp.write("*TRG")
        time.sleep(7)
        volts.append(volt.query("FETC?"))
        amps.append(amp.query("FETC?"))
        
    else:
        sys.exit()
