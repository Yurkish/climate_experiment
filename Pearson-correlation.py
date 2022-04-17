from MyFunctions import *
import numpy as np
from numpy.linalg import inv
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy import stats
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
#datawx = []
#datawy = []
#for row in dataweather:
  #  datawx.append(row[1])
 #   datawy.append(row[2])

room5_inter = interp1d(data5x, data5y, kind='cubic')
room6_inter = interp1d(data6x, data6y, kind='cubic')
room7_inter = interp1d(data7x, data7y, kind='cubic')
#weath_inter = interp1d(datawx, datawy, kind='cubic')
x1new = np.linspace(time_start, time_stop, num=800, endpoint=True)

time_steps = len(x1new)
print('time steps = ', time_steps)
w, h = 4, time_steps
# U: list[list[int]] = [[0 for x in range(w)] for y in range(h)]
U = np.zeros( (h-1,w) )
x_simple = np.zeros( h )
y_simple = np.zeros( h)
time_simple = np.zeros( h)
with open('pearson-corr.csv', 'w') as res:
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
        x_simple[indd] = "%.7f" % float(room6_inter(time_is_now))
        y_simple[indd] = "%.7f" % float(dataweather[ind][2])
        time_simple[indd] = row
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
        indd += 1
        conc.writerow(dict(ts="%.0f" % row, tr5="%.3f" % room5_inter(time_is_now), tr6="%.7f" % room6_inter(time_is_now),
                           tr7="%.3f" % room7_inter(time_is_now), tw="%.3f" % float(dataweather[ind][2]),
                           twt="%.0f" % dataweather[ind][1], deltat=round(row - dataweather[ind][1])))
res.close()

x_s = np.array(x_simple)
y_s = np.array(y_simple)
#plt.plot(time_simple, x_simple, '-', time_simple, y_simple, '*')
#plt.show()
my_rho = np.corrcoef(x_s, y_s)

research_amount = 100
issleduem = np.zeros(research_amount)
print('pearson coefficient = ',my_rho)

for ii in range(research_amount):
    xxs = x_s[ii:]
    yys = y_s[:h-ii]
    #plt.plot(time_simple[:h-ii], xxs, '-', time_simple[:h-ii], yys, '*')
    #plt.show()
    issleduem[ii] = np.corrcoef(xxs,yys)[0][1]
    print('pearson coefficient ', ii,' = ', issleduem[ii])
print(np.where(issleduem == max(issleduem)))
print(np.argmax(issleduem))
q = np.argmax(issleduem)
#print(issleduem.index(issleduem.max()))

slope, intercept, r, p, std_err = stats.linregress(y_s[:h-q],x_s[q:])

def myfunc(xxx):
  return slope * xxx + intercept

mymodel = list(map(myfunc, y_s[:h-q]))

plt.scatter(y_s[:h-q], x_s[q:])
plt.plot(y_s[:h-q], mymodel)
plt.show()