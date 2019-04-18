# Combine all years into a single matrix 

import numpy as np
import pandas as pd
import sys
from subprocess import call
import os

folder = '.'
files = os.listdir(folder)
files = [file for file in files if file.endswith('.csv' )]
df = pd.DataFrame()
for filename in files:
    path_and_file = folder + '/' + filename
    new_df = pd.read_csv(path_and_file)
    df = pd.concat([df,new_df])
df.to_csv('dataMatrix_combined.csv')
print("Made concatenated matrix and saved to dataMatrix_combined.csv")
