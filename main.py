from MyFunctions import *
import numpy as np
from numpy.linalg import inv
from scipy.interpolate import interp1d


# importing data from csv files
month_code = 'july'
match month_code:
    case 'jun':
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

time_steps = len(x1new)
print('time steps = ', time_steps)
w, h = 4, time_steps
# U: list[list[int]] = [[0 for x in range(w)] for y in range(h)]
U = np.zeros( (h-1,w) )
ksi = np.zeros( h-1 )
# ksi = [0 for y in range(h)]

with open('result-aug.csv', 'w') as res:
    conc = csv.DictWriter(res, delimiter=";", fieldnames=['ts', 'tr5', 'tr6', 'tr7', 'tw', 'twt', 'deltat'])
    conc.writeheader()
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
        if indd == 0:
            U[indd][0] = "%.7f" % float(room6_inter(time_is_now))
            U[indd][1] = "%.7f" % float(room5_inter(time_is_now))
            U[indd][2] = "%.7f" % float(room7_inter(time_is_now))
            U[indd][3] = "%.7f" % float(dataweather[ind][2])
        else:
            if indd < time_steps - 1:
                U[indd][0] = "%.7f" % float(room6_inter(time_is_now))
                U[indd][1] = "%.7f" % float(room5_inter(time_is_now))
                U[indd][2] = "%.7f" % float(room7_inter(time_is_now))
                U[indd][3] = "%.7f" % float(dataweather[ind][2])
                ksi[indd-1] = U[indd][0]
        indd += 1
        conc.writerow(dict(ts="%.0f" % row, tr5="%.3f" % room5_inter(time_is_now), tr6="%.7f" % room6_inter(time_is_now),
                           tr7="%.3f" % room7_inter(time_is_now), tw="%.3f" % float(dataweather[ind][2]),
                           twt="%.0f" % dataweather[ind][1], deltat=round(row - dataweather[ind][1])))
res.close()
# print('497 - ', ksi[497], ', 498 - ', ksi[498])
ksi[time_steps - 2] = float(room6_inter(time_stop))
print('ksi length = ', len(ksi))
print('vector ksi: \n',ksi, '\n')
print('U size = ', len(U))

print('Matrix U: \n',U, '\n')
# print(Ut)
Ut = U.transpose()
print('Matrix Ut: \n',Ut, '\n')
mU = np.matrix(U)
mUt = np.matrix(Ut)
UtU = mUt.dot(mU)
print('Matrix UtU: \n',UtU, '\n')
UtUinv = inv(UtU)
UtUinvUt = UtUinv.dot(Ut)
a_estimate = UtUinvUt @ ksi
x2  = np.array(a_estimate)*(1/float(x1new[5]-x1new[4]))
print(x2)

