import numpy as np
import pickle
from scipy import stats
import matplotlib.pyplot as plt
import temperature


def mean(results):
    for i in results:
        results[i]["am"] = np.mean(results[i]["amps"], axis=1)
        results[i]["vm"] = np.mean(results[i]["volts"], axis=1)


def load(FILE):
    with open(str(FILE), "rb") as pick:
        r = pickle.load(pick)
    return r


def store(results, FILE):
    with open(str(FILE), "wb") as pick:
        pickle.dump(results, pick)


def intercept(results, n=10, auto=False):
    try:
        for i in results:
            lr = stats.linregress(results[i]['vm'][-n:], results[i]['am'][-n:])
            inter = -lr[1]/lr[0]
            print(inter)
            results[i]["lr"] = lr
            results[i]["intercept"] = inter

    except KeyError as e:
        if auto:
            raise e
        else:
            mean(results)
            intercept(results, n, True)


def plot_temp(results):
    inters = [results[i]["intercept"] for i in results]
    temps = [results[i]["mean_temp"] for i in results]
    plt.plot(temps, inters, 'bo')
    plt.show()


def add_temps(results, FILE):
    times, temps = temperature.import_temps(str(FILE+".txt"))
    for i in results:
        start_time = results[i]["start_time"]
        end_time = results[i]["end_time"]
        start_temp = (times == start_time).argmax()
        if start_temp == 0:
            start_temp = (times == end_time).argmax()
        if start_temp == 0:
            mean_temp = results[i-1]["mean_temp"]
        else:
            mean_temp = temps[start_temp]
        results[i]["mean_temp"] = mean_temp


def make_data(results):
    data = results.copy()
    print(data)
    results.clear()
    results["data"] = data.copy()


def make_volts(results):
    volts = [results["data"][i]["vm"][0] for i in results["data"]]
    volts = np.array(volts)
    results["Volts"] = volts


def make_amps(results):
    amps = [results["data"][i]["am"][0] for i in results["data"]]
    amps = np.array(amps)
    mean_amps = np.mean(amps)
    std_amps = np.std(amps)
    results["meanI"] = [mean_amps, std_amps]


def make_temp(results):
    temps = [results["data"][i]["mean_temp"] for i in results["data"]]
    temps = np.array(temps)
    results["Temp"] = temps


def make_caroline(l_results):
    if type(l_results) == list:
        for results in l_results:
            make_data(results)
            make_volts(results)
            make_amps(results)
            make_temp(results)
    else:
        results = l_results
        make_data(results)
        make_volts(results)
        make_amps(results)
        make_temp(results)
