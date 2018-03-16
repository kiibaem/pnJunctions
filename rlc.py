import numpy as np
import pickle
import serial
import serial.tools.list_ports
import sys
import time
import visa

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
    ps_num = input("Select RLC: ")
    if ps_num.isdecimal() and int(ps_num) < len(instruments):
        try:
            temp = serial.Serial(instruments[int(ps_num)][4:-7])
            temp.write(b"*IDN?\r\n")
            print(temp.readline())
            response = input("Is that correct (Y/N)? ")
            if response.capitalize() == "Y":
                    rlc = temp
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

FILE = input("Enter filename: ")
try:


    rlc.write(b"\x20\r\n")
    rlc.write(b"\x09\r\n")
    rlc.write(b"*RST;*CLS\r\n")
    rlc.write(b"*TRG\r\n")
    rlc.write(b"C?\r\n")
    print(rlc.readline())
    rlc.write(b"LEVEL?\r\n")
    print(rlc.readline())
    rlc.write(b"LEVEL_LOW\r\n")
    rlc.write(b"LEVEL?\r\n")
    print(rlc.readline())
    rlc.write(b"BIAS_EXT\r\n")
    print("mon")
    rlc.write(b"MON_BIAS\r\n")
    data=[]
    voltages=[]
    ps.set_output(False)
    ps.set_current(0.03)
    ps.set_voltage(0)
    ps.set_output(True)
    for i in np.arange(0,2,0.05):
        ps.set_voltage(i)
        rlc.write(b"*TRG\r\n")
        rlc.write(b"C?\r\n")
        data.append(rlc.readline())
        rlc.write(b"MON_B?\r\n")
        voltages.append(rlc.readline())


    rlc.write(b"\x01\r\n")

    d = [i[2:-2] for i in data]
    d1 = np.array(d, dtype=float)
    v = [i[2:-2] for i in voltages]
    v1 = np.array(v, dtype=float)

    with open(FILE, "wb") as pick:
        pickle.dump(d1, pick)

    with open(FILE+"V", "wb") as pick:
        pickle.dump(v1, pick)
    
except Exception as e:
    print(e)
finally:
    ps.set_output(False)
    rlc.close()
    ps.close()


