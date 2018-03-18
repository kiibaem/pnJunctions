import pickle
import temperature


FILE="TEST"

times, temps = temperature.import_temps(str(FILE+"_TEMP.txt"))

with open(FILE+"_T", "rb") as pick:
    results = pickle.load(pick)

for i in results:
    start_time = results[i]["start_time"]
    end_time = results[i]["end_time"]
    mean_temp = temperature.mean_temp(start_time, end_time, times, temps)
    results[i]["mean_temp"] = mean_temp

with open(FILE, "wb") as pick:
    pickle.dump(results, pick)
