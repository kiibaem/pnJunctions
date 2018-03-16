import csv
import numpy as np
import pickle
import sys
import time
import visa
import serial
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from PyExpLabSys.drivers import tenma

rm = visa.ResourceManager("@py")

instruments = rm.list_resources()

print("Connected instruments:")
for ind, inst in enumerate(instruments):
    print(str(ind)+") "+inst)

while True:
    ps_num = input("Select power supply: ")
    if ps_num.isdecimal() and int(ps_num) < len(instruments):
        try:
            print(instruments[int(ps_num)][4:-7])
            temp = tenma.Tenma722535(instruments[int(ps_num)][4:-7])
            print(temp.get_identification())

            response = input("Is that correct (Y/N)? ")

            if response.capitalize() == "Y":
                ps = temp
                break

            else:
                print("Please enter a listed number or 'q' to quit")

        except serial.SerialException as e:
            print(e)
            print("Could not establish communication with the device")
            print("Please enter a listed number or 'q' to quit")

    elif ps_num == "q":
        sys.exit()
    else:
        print("Please enter a listed number or 'q' to quit")


while True:
    ps_num = input("Select first DMM: ")
    if ps_num.isdecimal() and int(ps_num) < len(instruments):
        try:
            temp = rm.open_resource(instruments[int(ps_num)])
            print(temp.query("*IDN?"))
            response = input("Is that correct (Y/N)? ")
            if response.capitalize() == "Y":
                    dmm1 = temp
                    break
            else:
                print("Please enter a listed number or 'q' to quit")
        except serial.SerialException:
            print("Could not establish communication with the device")
            print("Please enter a listed number or 'q' to quit")

    elif ps_num == "q":
        sys.exit()
    else:
        print("Please enter a listed number or 'q' to quit")


while True:
    ps_num = input("Select second DMM: ")
    if ps_num.isdecimal() and int(ps_num) < len(instruments):
        try:
            temp = rm.open_resource(instruments[int(ps_num)])
            print(temp.query("*IDN?"))
            response = input("Is that correct (Y/N)? ")
            if response.capitalize() == "Y":
                    dmm2 = temp
                    break
            else:
                print("Please enter a listed number or 'q' to quit")
        except serial.SerialException:
            print("Could not establish communication with the device")
            print("Please enter a listed number or 'q' to quit")

    elif ps_num == "q":
        sys.exit()
    else:
        print("Please enter a listed number or 'q' to quit")

dmm1.write(":SYST:REM")
while True:
    response = input("Is this voltmeter or ammeter (V/A)? ")
    if response.capitalize() == "V":
        volt = dmm1
        amp = dmm2
        break
    elif response.capitalize() == "A":
        volt = dmm2
        amp = dmm1
        break
    elif response == "q":
        sys.exit()
    else:
        print("Please select an option or 'q' to quit")

# amp = rm.open_resource(u'ASRL3::INSTR')
# volt = rm.open_resource(u'ASRL4::INSTR')

volt.write(":SYST:REM")
amp.write(":SYST:REM")
volt.write(":CONF:VOLT:DC 3,3")
volt.write("SAMP:COUN 10")
volt.write("TRIG:SOUR BUS")

amp.write(":CONF:CURR:DC 0.33,0.33")
amp.write("SAMP:COUN 10")
amp.write("TRIG:SOUR BUS")


# ps = tenma.Tenma722535("COM6")
# print(ps.com("*IDN?"))
# print(ps.get_identification())
ps.set_output(False)


# ps.com("OUT0") # This is the hard way, in case their wrappers don't work
# ps.com("ISET1:0.33")
# ps.com("VSET1:0")
# ps.com("OCP1")

while True:


    volts = []
    amps = []
    start = input("start (q to exit): ")
    if start == "q":
        exit()
    elif start == "a":
        start = 0
        max_current = float(input("Max current: "))
        step = float(input("Step: "))
        if step == "":
            step = 0.01
        ps.set_output(False)
        ps.set_current(max_current)
        ps.set_voltage(10)
        ps.set_output(True)
        plt.pause(0.5)
        stop = ps.get_actual_voltage()
        ps.set_output(False)
        print(stop)
    else:
        start = float(start)
        stop = float(input("stop: "))
        step = float(input("step: "))
        max_current = float(input("Max current: "))
        if max_current == "":
            max_current = 0.05
        ps.set_current(max_current)
    s_type = str(input("Semiconductor type:"))

    ps.set_voltage(0)
    # ps.set_overcurrent_protection(True)
    ps.set_output(True)

    am = []
    vm = []
    fig = plt.figure()
    fig.show()
    fig.canvas.draw()
    plt.title(s_type)
    try:
        for val in np.arange(start, stop, step):
            ps.set_voltage(val)
            volt.write("INIT")
            amp.write("INIT")
            volt.write("*TRG")
            amp.write("*TRG")
            plt.pause(0.1)
            v_temp = (volt.query("FETC?"))[:-2]
            a_temp = (amp.query("FETC?"))[:-2]
            v_temp=v_temp.split(",")
            a_temp=a_temp.split(",")
            v_temp=np.array(v_temp,dtype=float)
            a_temp = np.array(a_temp, dtype=float)
            vm.append(np.mean(v_temp))
            am.append(np.mean(a_temp))
            volts.append(v_temp)
            amps.append(a_temp)
            plt.plot(vm[-1], am[-1], 'bo')
            fig.canvas.draw()

        ps.set_output(False)
    

    



        with open(str(s_type)+".csv", "w") as csvf:
            wr = csv.writer(csvf, delimiter=",", quotechar="|",
                            quoting=csv.QUOTE_MINIMAL)
            wr.writerow(volts)
            wr.writerow(amps)

        with open(str(s_type+"_T"), "wb") as pick:
            pickle.dump(amps, pick)

        with open(str(s_type+"V_T"), "wb") as pick:
            pickle.dump(volts, pick)
    
    
    except KeyboardInterrupt:
        ps.set_output(False)

def exit():
    ps.close()
    amp.close()
    volt.close()
    sys.exit()
