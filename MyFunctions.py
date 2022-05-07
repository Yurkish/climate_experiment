import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
from scipy.interpolate import interp1d
from tkinter import filedialog
from tkinter import *
from scipy.interpolate import CubicSpline
from scipy import stats
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
            time_stop  = 1598591287

    x = []
    y = []
    for row in data:
        if row[1] > time_stop:
            break
        elif row[1] < time_start:
            continue
        else:
            x.append(float(row[1]))
            y.append(float(row[2]))
    #########################################################################
    ### new time points net ###########
    time_new = np.linspace(x[0], x[-1], num=time_point_amount, endpoint=True)
    #########################################################################
    ### interpolated function of temperature inside the room ################
    r_t = interp1d(x, y, kind='linear')
    #########################################################################
    # here we get data from meteostation dataset
    # time of measurement matches with time point for interpolation
    #
    ind = 1
    indd = 0
    w = np.zeros(time_point_amount)
    room_inter = np.zeros(time_point_amount)
    fin = int(dataweather[-1][0])
    for row in time_new:
        time_is_now = float(row)
        for i in range(ind, fin):
            if int(dataweather[i][1]) < time_is_now:
                continue
            else:
                ind = i
                break
        w[indd] = "%.7f" % float(dataweather[ind][2])
        room_inter[indd] = "%.7f" % float(r_t(time_is_now))
        indd += 1
    #cs = CubicSpline(x, y)

    # for k in kind_lst:
    #     f = interp1d(x, y, kind=k)
    #     y_new = f(x_new)
    #     plt.plot(x_new, y_new, label=k)

    # R = len(x)
    # print('\n R = ',R, '\n')
    # for row in range(R):
    #     diff1 = cs(x[row]) - y[row]
    #     diff2 = y[row] - room_funct(x[row])
    #     print('d[2] = ', data[row][2], 'y=',y[row] ,' cs=', cs(data[row][1]),' diff1 = ', diff1 ,' diff2 = ', diff2 ,'\n')
    #########################################################
    ##### here we start our estimation research #############
    #########################################################
    room_weather_corr = np.corrcoef(room_inter, w)
    print(room_weather_corr)
    #########################################################
    ##### let's shift reading frame #########################
    #########################################################
    search_for_maximum_corr = np.zeros(research_amount)
    #
    w_reduced = w[:time_point_amount - research_amount]
    for i in range(research_amount):
        # room temperature with i-shifted frame
        room_research = room_inter[i:time_point_amount - research_amount + i]
        # correlation of shifted room-t frame and fixed weather-t frame
        search_for_maximum_corr[i] = np.corrcoef(room_research, w_reduced)[0][1]
        print('pearson coefficient ', i, ' = ', search_for_maximum_corr [i])
    print(np.where(search_for_maximum_corr  == max(search_for_maximum_corr)))
    print(np.argmax(search_for_maximum_corr ))
    ########################################################
    ### best for correlation shift size ####################
    chosen_shift = np.argmax(search_for_maximum_corr)
    ###################################################
    slope, intercept, r, p, std_err = stats.linregress(w_reduced, room_inter[chosen_shift:time_point_amount - research_amount + chosen_shift])

    #########################################################################
    ### prediction of room_temperature from shifted weather temp ############
    def linear_room_weather_prediction(x):
        return slope * x + intercept
    #########################################################################
    ###### prepareing predicting array ######################################
    mymodel = list(map(linear_room_weather_prediction, w[:time_point_amount]))
    #########################################################################
    figure_shifting, (initial_fig, correl_to_shift, shifted_fig) = plt.subplots(3, 1, constrained_layout=True, sharey=True)
    initial_fig.plot(time_new, room_inter,'-')
    initial_fig.plot(time_new, w, '*')
    initial_fig.set_title('Initial data')
    initial_fig.set_xlabel('time (s)')
    initial_fig.set_ylabel('temperature (C)')

    correl_to_shift.plot(range(research_amount),search_for_maximum_corr,'-')
    correl_to_shift.set_xlabel('shifting time frame')
    correl_to_shift.set_title('Correlation Coeffitient')

    shifted_fig.plot(time_new[:time_point_amount - research_amount],w[:time_point_amount - research_amount],'-', time_new[:time_point_amount - research_amount],room_inter[chosen_shift:time_point_amount - research_amount+chosen_shift])
    shifted_fig.set_xlabel('time (s)')
    shifted_fig.set_title('undamped')

    figure_shifting.suptitle('Different figures', fontsize=16)
    # plt.show()
    #
    # plt.plot(x,y,'*',time_new, r_t(time_new),'-')
    # plt.legend(['raw','linear'], loc='best')
    plt.show()
    return 1
