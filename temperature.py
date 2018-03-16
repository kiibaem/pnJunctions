import numpy as np
import time

FILE="test.txt"

lines=[]

with open(FILE, "r") as file:
    for line in file:
        lines.append(line)

l = [i.split('\t') for i in lines][1:]
temps = np.array([i[3] for i in l], dtype=float)
times = np.array([i[1].split('_')[1] for i in l])

def find_time(time_string, times):
    """Readbility"""
    return (times==time_string).argmax()

def store_time():
    return time.asctime()[11:-5]

def mean_temp(start_time, end_time, times, temps):
    start = find_time(start_time, times)
    end = find_time(end_time, times)
    return np.mean(temps[start:end])