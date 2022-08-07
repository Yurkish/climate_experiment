from MyFunctions import *
import pandas as pd
import glob
import shutil
import os
month_array = ['january','february', 'march', 'april','may','june', 'july', 'august', 'september', 'october','november','december']
rooms_array = ['room5', 'room6', 'room7', 'room9', 'room10']
rooms_from_devices = ['Climate_8', 'Climate_7', 'Climate_2', 'Climate_3', 'Climate_1','Meteo_0', 'Meteo_1']
meteostations = ['Meteo_0', 'Meteo_1']
dataset_path = '/home/yurkish/dataset_2021'

for room in rooms_from_devices:
    all_files = glob.glob(dataset_path + "/2021.0*/" + room + ".csv")
    all_files.sort()
    # print(all_files)
    with open(dataset_path + '/' + room + '_concat.csv', 'wb') as outfile:
        for i, fname in enumerate(all_files):
            with open(fname, 'rb') as infile:
                if i != 0:
                    infile.readline()  # Throw away header on all but first file
                # Block copy rest of file from input to output without parsing
                shutil.copyfileobj(infile, outfile)
                print(fname + " has been sucsessfully imported.")