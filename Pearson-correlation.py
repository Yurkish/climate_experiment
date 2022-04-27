from MyFunctions import *
import numpy as np
from numpy.linalg import inv
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy import stats
# importing data from csv files
data5_june = import_csv_temperature('dataset/jun20/ELT_aud.5_6D73.csv')
data6_june = import_csv_temperature('dataset/jun20/ELT_aud._6_8B17.csv')
data7_june = import_csv_temperature('dataset/jun20/ERS-CO2_aud._7.csv')
dataweather_june = import_csv_weather('dataset/jun20/Meteostantsiia_1.csv')
time_start_june = max(data5_june[1][1], data6_june[1][1], data7_june[1][1])
time_stop_june = min(data5_june[-1][1], data6_june[-1][1], data7_june[-1][1])
time_point_amount_june = int((time_stop_june - time_start_june)/300)
research_amount_june = 300
#################################################################################
data5_july = import_csv_temperature('dataset/jul20/ELT_aud.5_6D73.csv')
data6_july = import_csv_temperature('dataset/jul20/ELT_aud._6_8B17.csv')
data7_july = import_csv_temperature('dataset/jul20/ERS-CO2_aud._7.csv')
dataweather_july = import_csv_weather('dataset/jul20/Meteostantsiia_1.csv')
time_point_amount_july = 18720
research_amount_july = 600
################################################################################
data5_aug = import_csv_temperature('dataset/aug20/ELT_aud.5_6D73.csv')
data6_aug = import_csv_temperature('dataset/aug20/ELT_aud._6_8B17.csv')
data7_aug = import_csv_temperature('dataset/aug20/ERS-CO2_aud._7.csv')
dataweather_aug = import_csv_weather('dataset/aug20/Meteostantsiia_1.csv')
time_point_amount_aug = 14400
research_amount_aug = 1000
#################################################################################
month_code = 'aug'
match month_code:
    case 'june':
        data5 = import_csv_temperature('dataset/jun20/ELT_aud.5_6D73.csv')
        data6 = import_csv_temperature('dataset/jun20/ELT_aud._6_8B17.csv')
        data7 = import_csv_temperature('dataset/jun20/ERS-CO2_aud._7.csv')
        dataweather = import_csv_weather('dataset/jun20/Meteostantsiia_1.csv')
        time_point_amount = 4320
        research_amount = 300
    case 'july':
        data5 = import_csv_temperature('dataset/jul20/ELT_aud.5_6D73.csv')
        data6 = import_csv_temperature('dataset/jul20/ELT_aud._6_8B17.csv')
        data7 = import_csv_temperature('dataset/jul20/ERS-CO2_aud._7.csv')
        dataweather = import_csv_weather('dataset/jul20/Meteostantsiia_1.csv')
        time_point_amount = 18720
        research_amount = 600
    case 'aug':
        data5 = import_csv_temperature('dataset/aug20/ELT_aud.5_6D73.csv')
        data6 = import_csv_temperature('dataset/aug20/ELT_aud._6_8B17.csv')
        data7 = import_csv_temperature('dataset/aug20/ERS-CO2_aud._7.csv')
        dataweather = import_csv_weather('dataset/aug20/Meteostantsiia_1.csv')
        time_point_amount = 14400
        research_amount = 1000

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


#x1new = np.linspace(time_start, time_stop, num=time_point_amount, endpoint=True)
x1new = np.linspace(1597612430, 1598591836, num=time_point_amount, endpoint=True)
time_steps = len(x1new)
print('time steps = ', time_steps)
w, h = 4, time_steps
# U: list[list[int]] = [[0 for x in range(w)] for y in range(h)]
U = np.zeros( (h-1,w) )
x_simple5 = np.zeros( h )
x_simple6 = np.zeros( h )
x_simple7 = np.zeros( h )
y_simple = np.zeros( h)
time_simple = np.zeros( h)
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
    x_simple5[indd] = "%.7f" % float(room5_inter(time_is_now))
    x_simple6[indd] = "%.7f" % float(room6_inter(time_is_now))
    x_simple7[indd] = "%.7f" % float(room7_inter(time_is_now))
    y_simple[indd] = "%.7f" % float(dataweather[ind][2])
    time_simple[indd] = row
    indd += 1
#create_res_by_time('file_aug_1.csv', 1596445282000, 1596773016000, data5x, data5y,data6x, data6y, data7x, data7y, dataweather)


x5_s = np.array(x_simple5)
x6_s = np.array(x_simple6)
x7_s = np.array(x_simple7)
y_s = np.array(y_simple)

#x_s, y_s = create_arrays('aug')

#plt.plot(time_simple, x_simple, '-', time_simple, y_simple, '*')
#plt.show()
my_rho5 = np.corrcoef(x5_s, y_s)
my_rho6 = np.corrcoef(x6_s, y_s)
my_rho7 = np.corrcoef(x7_s, y_s)

issleduem5 = np.zeros(research_amount)
issleduem6 = np.zeros(research_amount)
issleduem7 = np.zeros(research_amount)

print('pearson coefficient = ',my_rho5)
yys = y_s[:h-research_amount]
for ii in range(research_amount):
    xxs5 = x5_s[ii:h - research_amount + ii]
    xxs6 = x6_s[ii:h - research_amount + ii]
    xxs7 = x7_s[ii:h - research_amount + ii]
    #plt.plot(time_simple[:h-ii], xxs, '-', time_simple[:h-ii], yys, '*')
    #plt.show()
    issleduem5[ii] = np.corrcoef(xxs5,yys)[0][1]
    issleduem6[ii] = np.corrcoef(xxs6, yys)[0][1]
    issleduem7[ii] = np.corrcoef(xxs7, yys)[0][1]
    print('pearson coefficient ', ii,' = ', issleduem5[ii])
print(np.where(issleduem5 == max(issleduem5)))
print(np.argmax(issleduem5))
q5 = np.argmax(issleduem5)
q6 = np.argmax(issleduem6)
q7 = np.argmax(issleduem7)
#print(issleduem.index(issleduem.max()))
slope5, intercept5, r5, p5, std_err5 = stats.linregress(y_s[:h-research_amount],x5_s[q5:h-research_amount+q5])
slope6, intercept6, r6, p6, std_err6 = stats.linregress(y_s[:h-research_amount],x6_s[q6:h-research_amount+q6])
slope7, intercept7, r7, p7, std_err7 = stats.linregress(y_s[:h-research_amount],x7_s[q7:h-research_amount+q7])

def myfunc5(xxx):
  return slope5 * xxx + intercept5
def myfunc6(xxx):
  return slope6 * xxx + intercept6
def myfunc7(xxx):
  return slope7 * xxx + intercept7

mymodel5 = list(map(myfunc5, y_s[:h-q5]))
mymodel6 = list(map(myfunc6, y_s[:h-q6]))
mymodel7 = list(map(myfunc7, y_s[:h-q7]))

f15 = plt.figure(1)
plt.plot(x1new[research_amount:], x5_s[research_amount:], '*',x1new[research_amount:],myfunc5(y_s[q5:h-research_amount+q5]),'-')
plt.legend(['inside temp, inside_predicted'], loc='best')
f25 = plt.figure(2)
plt.scatter(y_s[:h-q5], x5_s[q5:])
plt.plot(y_s[:h-q5], mymodel5)

f35 = plt.figure(3)
plt.plot(x1new, x5_s, '-', x1new, y_s, '*')
plt.legend('Initial condition')
f4 = plt.figure(4)
plt.plot(range(research_amount),issleduem5)
plt.show()