from MyFunctions import *
import numpy as np
from numpy.linalg import inv
from scipy.interpolate import interp1d

# importing data from csv files
month_code = 'june'
match month_code:
    case 'june':
        data5 = import_csv_temperature('june/r5.csv')
        data6 = import_csv_temperature('june/r6.csv')
        data7 = import_csv_temperature('june/r7.csv')
        dataweather = import_csv_weather('june/w1.csv')
    case 'july':
        data5 = import_csv_temperature('july/room5_july.csv')
        data6 = import_csv_temperature('july/room6_july.csv')
        data7 = import_csv_temperature('july/room7_july.csv')
        dataweather = import_csv_weather('july/met.csv')
    case 'aug':
        data5 = import_csv_temperature('aug/r5_aug.csv')
        data6 = import_csv_temperature('aug/r6_aug.csv')
        data7 = import_csv_temperature('aug/r7_aug.csv')
        dataweather = import_csv_weather('aug/w_aug.csv')

# define time interval that is covered by data from all three rooms
time_start = max(data5[1][1], data6[1][1], data7[1][1])
time_stop = min(data5[-1][1], data6[-1][1], data7[-1][1])

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
x1new = np.linspace(time_start, time_stop, num=800, endpoint=True)
#
