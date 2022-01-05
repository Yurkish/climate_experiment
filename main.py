import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from numpy.linalg import inv

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


def import_csv_weather(csvfilename):
    data = []
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.DictReader(scraped, delimiter=';')
        # header = reader.fieldnames
        row_index = 0
        for rowincsv in reader:
            if rowincsv:  # avoid blank lines
                row_index += 1
                columns = [str(row_index), int(rowincsv["ts"]) // 1000, rowincsv["Temperature"]]
                data.append(columns)
        print(csvfilename, ' - begins at: ', datetime.datetime.fromtimestamp(float(data[1][1])))
        print(csvfilename, ' - ends at  : ', datetime.datetime.fromtimestamp(float(data[-1][1])))
    return data


# importing data from csv files
data5 = import_csv_temperature('june/r5.csv')
data6 = import_csv_temperature('june/r6.csv')
data7 = import_csv_temperature('june/r7.csv')
dataweather = import_csv_weather('june/w1.csv')

# define time interval that is covered by data from all three rooms
time_start = max(data5[1][1], data6[1][1], data7[1][1])
time_stop = min(data5[-1][1], data6[-1][1], data7[-1][1])

data5x = []
data5y = []
for row in data5:
    data5x.append(row[1])
    data5y.append(row[2])
data6x = []
data6y = []
for row in data6:
    data6x.append(row[1])
    data6y.append(row[2])
data7x = []
data7y = []
for row in data7:
    data7x.append(row[1])
    data7y.append(row[2])

room5_inter = interp1d(data5x, data5y, kind='cubic')
room6_inter = interp1d(data6x, data6y, kind='cubic')
room7_inter = interp1d(data7x, data7y, kind='cubic')
x1new = np.linspace(time_start, time_stop, num=500, endpoint=True)

with open('june/result.csv', 'w') as res:
    conc = csv.DictWriter(res, delimiter=";", fieldnames=['ts', 'tr5', 'tr6', 'tr7', 'tw', 'twt', 'deltat'])
    conc.writeheader()
    ind = 1
    fin = int(dataweather[-1][0])
    for row in x1new:
        time_is_now = float(row)
        for i in range(ind, fin):
            if int(dataweather[i][1]) < time_is_now:
                continue
            else:
                ind = i
                break
        # time_is_second = int(time_is_now)
        conc.writerow(dict(ts="%.0f" % row, tr5="%.3f" % room5_inter(row), tr6="%.3f" % room6_inter(row),
                           tr7="%.3f" % room7_inter(time_is_now), tw="%.3f" % float(dataweather[ind][2]),
                           twt="%.0f" % dataweather[ind][1], deltat=round(row - dataweather[ind][1])))
res.close()


ksi = []
x1ksi = []
U = np.ones[4]
with open('june/result.csv', 'r') as data_res:
    reader = csv.DictReader(data_res, delimiter=';')
    row_index1 = 0
    for row in reader:
        if row_index1 < 2:
            if row_index1 == 1:
               arr = np.array([[float(row['tr6']),float(row['tr5']), float(row['tr7']),float(row['tw'])]])
               U.append(arr)
        else:
            if row_index1 > 497:
                arr = np.array([[float(row['tr6']),float(row['tr5']), float(row['tr7']),float(row['tw'])]])
                U.append(arr)
                break
            else:
                ksi.append(float(row['tr6']))
                x1ksi.append(x1new[row_index1])
                arr = np.array([[float(row['tr6']),float(row['tr5']), float(row['tr7']),float(row['tw'])]])
                U.append(arr)
        row_index1 += 1
    Ut = np.transpose(np.matrix(U))
    UtU = np.dot(Ut,U)
    UtUinv = inv(UtU)
    UtUinvUt = np.dot(UtUinv,Ut)
    a_estimate = np.dot(UtUinvUt, ksi)
    print(a_estimate)
    # plt.plot(x1ksi, ksi, '-', x1new, room6_inter(x1new), '*')
    # plt.legend(['data', 'linear', 'cubic'], loc='best')
    # plt.show()