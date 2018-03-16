import serial
import time
import sys
import numpy as np
import serial.tools.list_ports
from PyExpLabSys.drivers import tenma

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

sp = serial_ports()

for i, port in enumerate(sp):
    print str(i) + ") " + port
try:
    sprt = int(raw_input("which? "))
    rlc = serial.Serial(sp[sprt])

    psprt = int(raw_input("ps? "))
    ps = tenma.Tenma722535(sp[psprt])


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
    rlc.write("BIAS_EXT\r\n")
    rlc.write("MON_BIAS")
    data=[]
    ps.set_output(False)
    ps.set_current(0.03)
    ps.set_voltage(0)
    ps.set_output(True)
    for i in np.arange(0,2,0.05):
        ps.set_voltage(i)
        rlc.write("*TRG\r\n")
        rlc.write("C?\r\n")
        data.append(rlc.readline())


    rlc.write(b"\x01\r\n")
except Exception as e:
    print(e)
finally:
    rlc.close()
    ps.close()