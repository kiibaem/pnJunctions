if start == "a":
    start = 0
    ps.set_output(False)
    ps.set_current(0.3)
    ps.set_voltage(10)
    ps.set_output(True)
    plt.pause(0.5)
    stop = ps.get_actual_voltage()
    ps.set_output(False)
    step = 0.01
    
else: