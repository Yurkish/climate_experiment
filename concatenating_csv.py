from MyFunctions import *
import csv
import pandas as pd
from pathlib import Path
from functools import partial
import glob
import shutil
import os
month_array = ['january','february', 'march', 'april','may','june', 'july', 'august', 'september', 'october','november','december']
rooms_array = ['room5', 'room6', 'room7', 'room9', 'room10']
arr_spring = [ 'march', 'april','may' ]
arr_summer = ['june', 'july', 'august']
arr_autumn_winter = ['september', 'october','november','december']
arr_train = ['march','may','june', 'august', 'september', 'october','december']
arr_test = ['april', 'july','november']
rooms_from_devices = ['Climate_2', 'Climate_8', 'Climate_7', 'Climate_3', 'Climate_1','Meteo_0', 'Meteo_1']
meteostations = ['Meteo_0', 'Meteo_1']
train_arr = ['03','05','06', '08', '09','10','12']
test_arr = ['04', '07', '11']
print(Path.home())
dataset_path = str(Path.home()) + "/dataset2021"

# ############### concatenating all files ################################
# for room in rooms_from_devices:
#     all_files = glob.glob(dataset_path + "/2021.**/" + room + ".csv")
#     all_files.sort()
#     print(all_files)
#     with open(dataset_path + '/' + room + '_concat.csv', 'wb') as outfile:
#         for i, fname in enumerate(all_files):
#             with open(fname, 'rb') as infile:
#                 if i != 0:
#                     infile.readline()  # Throw away header on all but first file
#                 # Block copy rest of file from input to output without parsing
#                 shutil.copyfileobj(infile, outfile)
#                 print(fname + " has been sucsessfully imported.")
# ########################################################################

############### concatenating train files ##############################
for room in rooms_from_devices:
    all_train_files = [dataset_path + "/2021." + x + "/" + room + ".csv" for x in train_arr]
    print(all_train_files)
    ## this is list of files that have to be concatenated
    all_train_files.sort()
    results = [pd.read_csv(i, sep=';') for i in all_train_files]
    df = pd.concat(results, ignore_index=True)
    print(df)
    df.to_csv(dataset_path + '/' + room + '_train_1.csv')

for room in rooms_from_devices:
    all_test_files = [dataset_path + "/2021." + x + "/" + room + ".csv" for x in test_arr]
    print(all_test_files)
    ## this is list of files that have to be concatenated
    all_test_files.sort()
    results = [pd.read_csv(i, sep=';') for i in all_test_files]
    df = pd.concat(results, ignore_index=True)
    print(df)
    df.to_csv(dataset_path + '/' + room + '_test_1.csv')


