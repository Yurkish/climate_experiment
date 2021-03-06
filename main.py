import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


# ts;humidity;light;motion;temperature;vdd
def import_csv_temperature(csvfilename):
    data = []
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.DictReader(scraped, delimiter=';')
        # header = reader.fieldnames
        row_index = 0
        for rowincsv in reader:
            if rowincsv:  # avoid blank lines
                row_index += 1
                columns = [str(row_index), int(rowincsv["ts"]) // 1000, rowincsv["temperature"]]
                data.append(columns)
        print(csvfilename, ' - begins at: ', datetime.datetime.fromtimestamp(float(data[1][1])))
        print(csvfilename, ' - ends at  : ', datetime.datetime.fromtimestamp(float(data[-1][1])))
    return data


# importing data from csv files
data5 = import_csv_temperature('june/r5.csv')
data6 = import_csv_temperature('june/r6.csv')
data7 = import_csv_temperature('june/r7.csv')

with open('june/r5.csv', 'r', newline='') as room5, \
        open('june/r6.csv', 'r') as room6, \
        open('june/r7.csv', 'r') as room7, \
        open('june/r9.csv', 'r') as room9, \
        open('june/r10.csv', 'r') as room10, \
        open('june/w1.csv', 'r') as outside, \
        open('june/result.csv', 'w') as res:
    # ts;humidity;light;motion;temperature;vdd
    # ts;BaroPressure;DewPoint;Humidity;Temperature;WindDirection;WindSpeed
    r5 = csv.DictReader(room5, delimiter=";")
    headers_room = r5.fieldnames
    print(headers_room)
    r6 = csv.DictReader(room6, delimiter=";")
    r7 = csv.DictReader(room7, delimiter=";")
    r9 = csv.DictReader(room9, delimiter=";")
    r10 = csv.DictReader(room10, delimiter=";")
    m = csv.DictReader(outside, delimiter=";")
    headers_weather = m.fieldnames
    conc = csv.DictWriter(res, delimiter=";", fieldnames=['ts', 'tr', 'tm'])
    conc.writeheader()
    print(headers_weather)

    x_r5 = []
    x_r6 = []
    x_r7 = []
    y_r5 = []
    y_r6 = []
    y_r7 = []

    for row in r5:
        time_r5 = int(row["ts"]) // 1000
        timer5 = datetime.datetime.fromtimestamp(time_r5)
        temp_r5 = float(row["temperature"])
        x_r5.append(time_r5)
        y_r5.append(temp_r5)
        for row_m in m:
            time_m = int(row_m["ts"]) // 1000
            if time_m < time_r5:
                continue
            else:
                # print("time_m =", time_m, " time_r9 = ", time_r9)
                rt = float(row["temperature"])
                rm = float(row_m["Temperature"])
                rslt = [time_m, rt, rm]
                conc.writerow({'ts': time_m, 'tr': rt, 'tm': rm})
                break
    # print(y_r5[10])
f22 = interp1d(x_r5, y_r5, kind='cubic')
x1new = np.linspace(x_r5[0], x_r5[-1], num=100, endpoint=True)
plt.plot(x_r5, y_r5, '-', x1new, f22(x1new), 'o')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.show()
