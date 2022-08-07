from MyFunctions import *
import pandas as pd
from pandas.plotting import table # EDIT: see deprecation warnings below

month_array = ['july']
rooms_array = ['room5']
save_fig = 0
data = np.zeros((len(month_array),len(rooms_array)))
vector = np.zeros(5)
for room in rooms_array:
     for month in month_array:
         vector = pearson_correlation_research(month,room,save_fig)
         data[month_array.index(month)][rooms_array.index(room)]=vector[0]
dt = pd.DataFrame(data,columns=rooms_array,index=month_array)
print(dt)
the_table = plt.table(cellText=data, rowLabels=month_array, colLabels=rooms_array,)
plt.show()