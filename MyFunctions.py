import csv
import datetime
import numpy as np
from numpy.linalg import inv
from scipy.interpolate import interp1d
from tkinter import filedialog
from tkinter import *

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
        print(csvfilename, ' - begins at: ', data[1][1])
        print(csvfilename, ' - ends at  : ', data[-1][1])
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
def find_nobreak_periods(csvfilename):
    data = []
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.DictReader(scraped, delimiter=';')
        for rowincsv in reader:
            data[rowincsv] = int(rowincsv["ts"])

def create_file_list():
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return root

def create_res_by_time(csvfilename, t1, t2, data5x, data5y,data6x, data6y, data7x, data7y, dataweather):
    room5_inter = interp1d(data5x, data5y, kind='cubic')
    room6_inter = interp1d(data6x, data6y, kind='cubic')
    room7_inter = interp1d(data7x, data7y, kind='cubic')
    with open(csvfilename, 'w', newline='') as res:
        conc = csv.DictWriter(res, delimiter=";", fieldnames=['ts', 'tr5', 'tr6', 'tr7', 'tw', 'twt', 'deltat'])
        conc.writeheader()
        ind = 1
        time_point_amount = 14000
        x1new = np.linspace(t1, t2, num=time_point_amount, endpoint=True)
        fin = int(dataweather[-1][0])
        for row in x1new:
            time_is_now = float(row)
            for i in range(ind, fin):
                if int(dataweather[i][1]) < time_is_now:
                    continue
                else:
                    ind = i
                    break
            conc.writerow(dict(ts="%.0f" % row, tr5="%.3f" % room5_inter(time_is_now), tr6="%.7f" % room6_inter(time_is_now),
                     tr7="%.3f" % room7_inter(time_is_now), tw="%.3f" % float(dataweather[ind][2]),
                     twt="%.0f" % dataweather[ind][1], deltat=round(row - dataweather[ind][1])))
    res.close()

def create_arrays (month_code):
    match month_code:
        case 'june':
            data5 = import_csv_temperature('dataset/jun20/ELT_aud.5_6D73.csv')
            data6 = import_csv_temperature('dataset/jun20/ELT_aud._6_8B17.csv')
            data7 = import_csv_temperature('dataset/jun20/ERS-CO2_aud._7.csv')
            dataweather = import_csv_weather('dataset/jun20/Meteostantsiia_1.csv')
            time_point_amount = 4320
        case 'july':
            data5 = import_csv_temperature('dataset/jul20/ELT_aud.5_6D73.csv')
            data6 = import_csv_temperature('dataset/jul20/ELT_aud._6_8B17.csv')
            data7 = import_csv_temperature('dataset/jul20/ERS-CO2_aud._7.csv')
            dataweather = import_csv_weather('dataset/jul20/Meteostantsiia_1.csv')
            time_point_amount = 18720
        case 'aug':
            data5 = import_csv_temperature('aug/r5_aug.csv')
            data6 = import_csv_temperature('aug/r6_aug.csv')
            data7 = import_csv_temperature('aug/r7_aug.csv')
            dataweather = import_csv_weather('aug/w_aug.csv')
            time_point_amount = 14400
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

    # x1new = np.linspace(time_start, time_stop, num=time_point_amount, endpoint=True)
    x1new = np.linspace(1597612430, 1598591836, num=time_point_amount, endpoint=True)
    time_steps = len(x1new)
    print('time steps = ', )
    x_sssr = np.zeros(time_steps)
    y_sssr = np.zeros(time_steps)
    ind = 1
    indd = 0
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
            x_sssr[indd] = "%.7f" % float(room6_inter(time_is_now))
            y_sssr[indd] = "%.7f" % float(dataweather[ind][2])

            indd += 1
    return x_sssr, y_sssr
