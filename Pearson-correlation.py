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
month_code = 'june'
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

time_start_june = max(data5_june[1][1], data6_june[1][1], data7_june[1][1])
time_stop_june = min(data5_june[-1][1], data6_june[-1][1], data7_june[-1][1])

time_start_july = max(data5_july[1][1], data6_july[1][1], data7_july[1][1])
time_stop_july = min(data5_july[-1][1], data6_july[-1][1], data7_july[-1][1])

time_start_aug = max(data5_aug[1][1], data6_aug[1][1], data7_aug[1][1])
time_stop_aug = min(data5_aug[-1][1], data6_aug[-1][1], data7_aug[-1][1])

data5x_june = []
data5y_june = []
for row in data5_june:
    data5x_june.append(row[1])
    data5y_june.append(row[2])
data6x_june = []
data6y_june = []
for row in data6_june:
    data6x_june.append(row[1])
    data6y_june.append(row[2])
data7x_june = []
data7y_june = []
for row in data7_june:
    data7x_june.append(row[1])
    data7y_june.append(row[2])

data5x_july = []
data5y_july = []
for row in data5_july:
    data5x_july.append(row[1])
    data5y_july.append(row[2])
data6x_july = []
data6y_july = []
for row in data6_july:
    data6x_july.append(row[1])
    data6y_july.append(row[2])
data7x_july = []
data7y_july = []
for row in data7_july:
    data7x_july.append(row[1])
    data7y_july.append(row[2])

data5x_aug = []
data5y_aug = []
for row in data5_aug:
    data5x_aug.append(row[1])
    data5y_aug.append(row[2])
data6x_aug = []
data6y_aug = []
for row in data6_aug:
    data6x_aug.append(row[1])
    data6y_aug.append(row[2])
data7x_aug = []
data7y_aug = []
for row in data7_aug:
    data7x_aug.append(row[1])
    data7y_aug.append(row[2])
#datawx = []
#datawy = []
#for row in dataweather:
  #  datawx.append(row[1])
 #   datawy.append(row[2])

room5_inter_june = interp1d(data5x_june, data5y_june, kind='cubic')
room6_inter_june = interp1d(data6x_june, data6y_june, kind='cubic')
room7_inter_june = interp1d(data7x_june, data7y_june, kind='cubic')

room5_inter_july = interp1d(data5x_july, data5y_july, kind='cubic')
room6_inter_july = interp1d(data6x_july, data6y_july, kind='cubic')
room7_inter_july = interp1d(data7x_july, data7y_july, kind='cubic')

room5_inter_aug = interp1d(data5x_aug, data5y_aug, kind='cubic')
room6_inter_aug = interp1d(data6x_aug, data6y_aug, kind='cubic')
room7_inter_aug = interp1d(data7x_aug, data7y_aug, kind='cubic')
#weath_inter = interp1d(datawx, datawy, kind='cubic')

#x1new = np.linspace(time_start, time_stop, num=time_point_amount, endpoint=True)

#period 1
time_start_aug1 = 1596445120
time_stop_aug1  = 1597524902
time_point_amount_aug1 = 15000
#period 2
time_start_aug2 = 1597613321
time_stop_aug2 = 1598591287
time_point_amount_aug2 = 15000
x1_june = np.linspace(time_start_june, time_stop_june, num=time_point_amount_june, endpoint=True)
x1_july = np.linspace(time_start_july, time_stop_july, num=time_point_amount_july, endpoint=True)

x1_aug = np.linspace(time_start_aug1, time_stop_aug1, num=time_point_amount_aug1, endpoint=True)
x2_aug = np.linspace(time_start_aug2, time_stop_aug2, num=time_point_amount_aug2, endpoint=True)
h_june = len(x1_june)
h_july = len(x1_july)
h_aug1 = len(x1_aug1)
h_aug2 = len(x1_aug2)

x_simple5_june = np.zeros( h_june )
x_simple5_july = np.zeros( h_july )
x_simple5_aug1 = np.zeros( h_aug1 )
x_simple5_aug2 = np.zeros( h_aug2 )

x_simple6_june = np.zeros( h_june )
x_simple6_july = np.zeros( h_july )
x_simple6_aug1 = np.zeros( h_aug1 )
x_simple6_aug2 = np.zeros( h_aug2 )

x_simple7_june = np.zeros( h_june )
x_simple7_lujy = np.zeros( h_july )
x_simple7_aug1 = np.zeros( h_aug1 )
x_simple7_aug2 = np.zeros( h_aug2 )

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
#plt.show()

x = np.linspace(0.0, 5.0, 501)

fig, (ax1, ax2) = plt.subplots(2, 1, constrained_layout=True, sharey=True)
ax1.plot(x1new[research_amount:], x5_s[research_amount:], '-.')
ax1.set_title('damped')
ax1.set_xlabel('time (s)')
ax1.set_ylabel('amplitude')

ax2.plot(x1new[research_amount:],myfunc5(y_s[q5:h-research_amount+q5]))
ax2.set_xlabel('time (s)')
ax2.set_title('undamped')

fig.suptitle('Different types of oscillations', fontsize=16)
plt.show()