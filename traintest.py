from MyFunctions import *
from statistics import mean

def acquisition_step(month_code, room):
    data = []
    dataweather = []
    print(' -> ', month_code, ' ', room)
    match month_code:
        case 'june':
            dataweather = import_csv_weather('dataset/jun20/Meteostantsiia_1.csv')
            time_point_amount = 14320
            match room:
                case 'room5':
                    data = import_csv_temperature('dataset/jun20/ELT_aud.5_6D73.csv')
                case 'room6':
                    data = import_csv_temperature('dataset/jun20/ELT_aud._6_8B17.csv')
                case 'room7':
                    data = import_csv_temperature('dataset/jun20/ERS-CO2_aud._7.csv')
            time_start = data[1][1]
            time_stop = data[-1][1]
        case 'july':
            dataweather = import_csv_weather('dataset/jul20/Meteostantsiia_1.csv')
            time_point_amount = 18720
            match room:
                case 'room5':
                    data = import_csv_temperature('dataset/jul20/ELT_aud.5_6D73.csv')
                case 'room6':
                    data = import_csv_temperature('dataset/jul20/ELT_aud._6_8B17.csv')
                case 'room7':
                    data = import_csv_temperature('dataset/jul20/ERS-CO2_aud._7.csv')
            time_start = data[1][1]
            time_stop = data[-1][1]
        case 'aug1':
            dataweather = import_csv_weather('dataset/aug20/Meteostantsiia_1.csv')
            time_point_amount = 15000
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
        if row[1] > time_stop:
            break
        elif row[1] < time_start:
            continue
        else:
            x.append(float(row[1]))
            y.append(float(row[2]))
    #########################################################################
    # new time points net ###########
    time_new = np.linspace(x[0], x[-1], num=time_point_amount, endpoint=True)
    t_days = (x[-1] - x[0])/86400
    tt = np.linspace(0, (x[-1] - x[0]), num=time_point_amount, endpoint=True)
    tt_days = tt/86400
    #########################################################################
    # interpolated function of temperature inside the room ################
    r_t = interp1d(x, y, kind='linear')
    #########################################################################
    # here we get data from meteostation dataset
    # time of measurement matches with time point for interpolation
    #
    ind = 1
    indd = 0
    w = np.zeros(time_point_amount)
    t_points = np.zeros(time_point_amount)
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
        t_points[indd] = time_is_now
        indd += 1
    return w, room_inter, t_points, t_days, tt_days

def create_cvs_from_our_data(t_points, w, r, month, room):
    research_file_name = 'processed_dataset/' + month + '_' + room + '.csv'
    with open(research_file_name, 'w', newline='') as creating_file:
        conc = csv.DictWriter(creating_file, delimiter=";", fieldnames=['step', 'ts', 'w_t', 'r_t'])
        conc.writeheader()
        for i in range(len(w)):
            conc.writerow(dict(step="%.d" % i, ts="%.d" % t_points[i], w_t="%.2f" % w[i], r_t="%.2f" % r[i]))
    return 0
def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts)]


def search_for_best_shift(w, r, month, room, t_days):
    time_point_amount = len(w)
    research_amount = int(len(w) / (t_days * 4))
    print (research_amount)
    research_file_name = 'SHIFT SEARCH ' + month + ' ' + room + '.csv'
    search_for_maximum_corr = np.zeros(research_amount)
    #
    w_reduced = w[:time_point_amount - research_amount]
    with open(research_file_name, 'w', newline='') as research_res_file:
        conc = csv.DictWriter(research_res_file, delimiter=";", fieldnames=['step', 'pearson'])
        conc.writeheader()
        for i in range(research_amount):
            # room temperature with i-shifted frame
            room_research = r[i:time_point_amount - research_amount + i]
            # correlation of shifted room-t frame and fixed weather-t frame
            search_for_maximum_corr[i] = np.corrcoef(room_research, w_reduced)[0][1]
            conc.writerow(
                dict(step="%.d" % i, pearson="%.3f" % search_for_maximum_corr[i]))
    research_res_file.close()
    print(np.where(search_for_maximum_corr == max(search_for_maximum_corr)))
    print(np.argmax(search_for_maximum_corr))
    ########################################################
    ### best for correlation shift size ####################
    chosen_shift = np.argmax(search_for_maximum_corr)
    room_shifted = r[chosen_shift:time_point_amount - research_amount + chosen_shift]
    return w_reduced, room_shifted, research_amount, chosen_shift


def test_linregress_quality(w, r, slp, intr):
    def linear_room_weather_prediction(x):
        return slp * x + intr
    #########################################################################
    # prepareing predicting array ######################################
    mymodel = list(map(linear_room_weather_prediction, w))
    subtracted_list = np.subtract(mymodel, r)
    linear_deviation = np.std(subtracted_list)
    return linear_deviation

def gained_list(lst):
    gained = np.zeros(len(lst))
    avrg = mean(lst)
    for i in range(len(lst)):
        gained[i] = avrg + 2*(lst[i] - avrg)
    return gained
