import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_args():
    if len(sys.argv) < 2:
        print 'Usage: analyse.py in_file'
        exit(1)
        
    return sys.argv[1]


fname = read_args()
data = pd.read_csv(fname)

data1 = data[['ministry_id', 'placa', 'stevilo_dodatkov_pos', 'vsota_dodatkov_pos']]
grouped = data1.groupby('ministry_id')
means = grouped.aggregate(np.mean)
means.sort('vsota_dodatkov_pos', ascending=0)[:30]['vsota_dodatkov_pos'].plot(kind='bar')
means.sort('stevilo_dodatkov_pos', ascending=0)[:100]['stevilo_dodatkov_pos'].plot(kind='bar')