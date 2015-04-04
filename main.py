import os, time
import xlrd
import numpy as np
from sklearn import linear_model

start_time = time.time()

data_dir = 'data'

data = [] #stores all crime data
for root, dirs, filenames in os.walk(data_dir): #iterate over files
    for f in filenames:
        #file = open(os.path.join(root, f), 'r')
        try:
            wkbk = xlrd.open_workbook(os.path.join(root, f), logfile=open(os.devnull, 'w'))
        except:
            pass

print 'time to complete: %ds' % (time.time() - start_time)
