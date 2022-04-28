import csv
import datetime
import numpy as np
from numpy.linalg import inv
from scipy.interpolate import interp1d
from tkinter import filedialog
from tkinter import *

month_array = ['june', 'july', 'aug1', 'aug2']
rooms_array = ['room5', 'room6', 'room7']

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
def create_file_list():
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return root
def pearson_correlation_research(month_code,room):
    match month_code:
        case 'june':
            dataweather = import_csv_weather('dataset/jun20/Meteostantsiia_1.csv')
            time_point_amount = 4320
            research_amount = 300
            match room:
                case 'room5':
                    data = import_csv_temperature('dataset/jun20/ELT_aud.5_6D73.csv')
                case 'room6':
                    data = import_csv_temperature('dataset/jun20/ELT_aud._6_8B17.csv')
                case 'room7':
                    data = import_csv_temperature('dataset/jun20/ERS-CO2_aud._7.csv')
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
        case 'aug1':
            dataweather = import_csv_weather('dataset/aug20/Meteostantsiia_1.csv')
            time_start = 1596445120
            time_stop = 1597524902
            time_point_amount = 15000
            research_amount = 1000
            match room:
                case 'room5':
                    data5 = import_csv_temperature('dataset/aug20/ELT_aud.5_6D73.csv')
                case 'room6':
                    data6 = import_csv_temperature('dataset/aug20/ELT_aud._6_8B17.csv')
                case 'case7':
                    data7 = import_csv_temperature('dataset/aug20/ERS-CO2_aud._7.csv')
        case 'aug2':
            dataweather = import_csv_weather('dataset/aug20/Meteostantsiia_1.csv')
            time_point_amount = 14400
            research_amount = 1000
            time_start_aug2 = 1597613321
            time_stop_aug2 = 1598591287
            time_point_amount_aug1 = 15000
            match room:
                case 'room5':
                    data5 = import_csv_temperature('dataset/aug20/ELT_aud.5_6D73.csv')
                case 'room6':
                    data6 = import_csv_temperature('dataset/aug20/ELT_aud._6_8B17.csv')
                case 'case7':
                    data7 = import_csv_temperature('dataset/aug20/ERS-CO2_aud._7.csv')
    data_x = []
    data_y = []
    for row in data:
        data_x.append(row[1])
        data_y.append(row[2])
    room_funct = interp1d(data_x, data_y, kind='cubic')
    return 1
