import math, os, time
import multiprocessing
import xlrd
import numpy as np
from sklearn import linear_model

start_time = time.time()

data_dir = 'data'

def rows_in_xls(xls_file_path):
    """ Pass it the path for an excel file, returns a list of lists. With each
    inner list containing the values for that row. """
    all_rows = []
    try:
        wkbk = xlrd.open_workbook(xls_file_path, logfile=open(os.devnull, 'w'))
        sheet = wkbk.sheet_by_index(0)
        #fill up data list
        for row_ctr in range(1, sheet.nrows):
            dirty_row = sheet.row_slice(row_ctr)
            date_val = xlrd.xldate_as_tuple(dirty_row[0].value,wkbk.datemode)
            clean_row = [item.value for item in dirty_row]
            clean_row.pop(0)
            clean_row.insert(0, date_val)
            all_rows.append(clean_row)

        return all_rows
    except:
        return []

def multiprocessing_file_reader(file_names, n_cores):
    """"""
    def worker(file_names, out_q):
        """"""
        rows_data = []

        for file_name in file_names:
            rows_data.append(rows_in_xls(os.path.join(root, file_name)))

        out_q.put(rows_data)

    out_q = multiprocessing.Queue()
    chunksize = int(math.ceil(len(file_names) / float(n_cores)))
    procs = []
    for i in range(n_cores):
        p = multiprocessing.Process(target=worker, args=(file_names[chunksize * i:chunksize * (i+1)], out_q))
        procs.append(p)
        p.start()

    results_list = []
    for i in range(n_cores):
        results_list.extend(out_q.get())

    for p in procs: #wait until all processes finish
        p.join()

    return results_list


data = [] #stores all crime data
file_names = [] #stores names of xls filenames within the data/ directory
for root, dirs, filenames in os.walk(data_dir): #iterate over files
    for f in filenames:
        file_names.append(f)

x = multiprocessing_file_reader(file_names, 4)
for row in x:
    data.extend(row)

print data[0]

print 'time to complete: %ds' % (time.time() - start_time)
