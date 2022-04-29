import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
from scipy.interpolate import interp1d
from tkinter import filedialog
from tkinter import *
from scipy.interpolate import CubicSpline
kind_lst = ['nearest', 'zero', 'slinear', 'cubic', 'previous', 'next']

def import_csv_temperature(csvfilename):
    data = []
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.DictReader(scraped, delimiter=';')
        # header = reader.fieldnames
        row_index = 0
        for rowincsv in reader:
            if rowincsv:  # avoid blank lines
                row_index += 1
                columns = [str(row_index), int(rowincsv["ts"]) // 1000, float(rowincsv["temperature"])]
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
def create_file_list():
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return root
def pearson_correlation_research(month_code,room):
    print(' -> ',month_code, ' ', room)
    match month_code:
        case 'june':
            dataweather = import_csv_weather('dataset/jun20/Meteostantsiia_1.csv')
            time_point_amount = 14320
            research_amount = 300
            match room:
                case 'room5':
                    data = import_csv_temperature('dataset/jun20/ELT_aud.5_6D73.csv')
                case 'room6':
                    data = import_csv_temperature('dataset/jun20/ELT_aud._6_8B17.csv')
                case 'room7':
                    data = import_csv_temperature('dataset/jun20/ERS-CO2_aud._7.csv')
            time_start = data[1][1]
            time_stop  = data[-1][1]
        case 'july':
            dataweather = import_csv_weather('dataset/jul20/Meteostantsiia_1.csv')
            time_point_amount = 18720
            research_amount = 600
            match room:
                case 'room5':
                    data = import_csv_temperature('dataset/jul20/ELT_aud.5_6D73.csv')
                case 'room6':
                    data = import_csv_temperature('dataset/jul20/ELT_aud._6_8B17.csv')
                case 'room7':
                    data = import_csv_temperature('dataset/jul20/ERS-CO2_aud._7.csv')
            time_start = data[1][1]
            time_stop  = data[-1][1]
        case 'aug1':
            dataweather = import_csv_weather('dataset/aug20/Meteostantsiia_1.csv')
            time_point_amount = 15000
            research_amount = 1000
            match room:
                case 'room5':
                    data = import_csv_temperature('dataset/aug20/ELT_aud.5_6D73.csv')
                case 'room6':
                    data = import_csv_temperature('dataset/aug20/ELT_aud._6_8B17.csv')
                case 'room7':
                    data = import_csv_temperature('dataset/aug20/ERS-CO2_aud._7.csv')
            time_start = 1596445120
            time_stop = 1597524902
        case 'aug2':
            dataweather = import_csv_weather('dataset/aug20/Meteostantsiia_1.csv')
            time_point_amount = 14400
            research_amount = 1000
            time_point_amount = 15000
            match room:
                case 'room5':
                    data = import_csv_temperature('dataset/aug20/ELT_aud.5_6D73.csv')
                case 'room6':
                    data = import_csv_temperature('dataset/aug20/ELT_aud._6_8B17.csv')
                case 'room7':
                    data = import_csv_temperature('dataset/aug20/ERS-CO2_aud._7.csv')
            time_start = 1597613321
            time_stop = 1598591287

    x = []
    y = []
    for row in data:
        x.append(float(row[1]))
        y.append(float(row[2]))
    x_new = np.linspace(time_start, time_stop, num=time_point_amount, endpoint=True)
    cs = CubicSpline(x, y)

    # for k in kind_lst:
    #     f = interp1d(x, y, kind=k)
    #     y_new = f(x_new)
    #     plt.plot(x_new, y_new, label=k)
    room_funct = interp1d(x, y, kind='linear')
    R = len(data[:])
    print('\n R = ',R, '\n')
    for row in range(R):
        diff1 = cs(x[row]) - y[row]
        diff2 = y[row] - room_funct(x[row])
        print('d[2] = ', data[row][2], 'y=',y[row] ,' cs=', cs(data[row][1]),' diff1 = ', diff1 ,' diff2 = ', diff2 ,'\n')
    plt.plot(x,y,'*',x, room_funct(x),'-',x_new, cs(x_new),'-.')
    plt.legend(['raw','linear','cubic'], loc='best')
    plt.show()
    return 1
