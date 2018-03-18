import csv
import numpy as np
import pickle
import sys
import time
import visa
import serial
import matplotlib
matplotlib.use("TkAgg")


import temperature

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

try:
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
    volt.write("TRIG:SOUR IMM")
    volt.write(":NPLC 1")

    amp.write(":CONF:CURR:DC 0.33,0.33")
    amp.write("SAMP:COUN 10")
    amp.write("TRIG:SOUR IMM")
    amp.write(":NPLC 1")

    ps.set_output(False)

    def exit():
        """Exit gracefully without setting fire to the lab"""
        ps.set_output(False)
        ps.close()
        amp.close()
        volt.close()
        sys.exit()

    while True:

        start = input("start (q to exit): ")
        if start == "q":
            exit()
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
        i = 0
        results = {}

        try:
            while True:
                start_time = temperature.store_time()
                volts = []
                amps = []
                for val in np.arange(start, stop, step):
                    ps.set_voltage(val)
                    v_temp = (volt.query("READ?"))[:-2]
                    a_temp = (amp.query("READ?"))[:-2]
                    v_temp = v_temp.split(",")
                    a_temp = a_temp.split(",")
                    v_temp = np.array(v_temp, dtype=float)
                    a_temp = np.array(a_temp, dtype=float)
                    volts.append(v_temp)
                    amps.append(a_temp)

                end_time = temperature.store_time()
                ps.set_output(False)
                volts = np.array(volts)
                amps = np.array(amps)
                results[i] = {"volts": volts, "amps": amps, "start_time": start_time, "end_time": end_time}
                i += 1


            with open(str(s_type+"_T"), "wb") as pick:
                pickle.dump(results, pick)

        except KeyboardInterrupt:
            ps.set_output(False)
except Exception as e:
    """Try not to set things on fire if something goes wrong"""
    print("ABORT")
    print(e)
    exit()
