"""
Copyright (c) 2015 Rakshak Talwar
"""

import datetime, math, os, time
import multiprocessing
import xlrd
import numpy as np
from sklearn import cross_validation, linear_model

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

            date_val = xlrd.xldate_as_tuple(dirty_row[0].value, wkbk.datemode)
            date_in_proper_tuple = time.strptime(str(date_val), "(%Y, %m, %d, 0, 0, 0)")
            date_in_sec = time.mktime(date_in_proper_tuple)

            clean_row = [item.value for item in dirty_row]
            clean_row.pop(0)
            clean_row.insert(0, date_in_sec)
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

class Crime():
    """crime instance"""

    def __init__(self):
        self.id = -1
        self.date_in_sec = -1
        self.type = ''
        self.beat = ''

    def update_id(self, p_id):
        if isinstance(p_id, int):
            self.id = p_id
        else:
            raise TypeError

    def update_date_in_sec(self, p_sec):
        if isinstance(p_sec, int) or isinstance(p_sec, float):
            self.date_in_sec = p_sec
        else:
            raise TypeError

    def update_type(self, p_type):
        if isinstance(p_type, int):
            self.type = p_type
        else:
            raise TypeError

    def update_beat(self, p_beat):
        if isinstance(p_beat, int):
            self.beat = p_beat
        else:
            raise TypeError

class Crime_db():
    """ stores crime instances """

    def __init__(self):
        self.crimes = dict()

    def add_crime(self, p_crime):
        if isinstance(p_crime, Crime):
            self.crimes.update( { p_crime.id : p_crime } )

class StringToIntMapper():
    def __init__(self):
        self.key_to_hash = {};
        self.hash_to_key = {};

    def get_hash(self, key):
        if key not in self.key_to_hash:
            hash = len(self.key_to_hash)
            self.key_to_hash[key] = hash
            self.hash_to_key[hash] = key
        return self.key_to_hash[key]

    def get_key(self, hash):
        if hash in self.hash_to_key:
            return self.hash_to_key[hash]

beatMapper = StringToIntMapper()
typeMapper = StringToIntMapper()

def fill_crime_db(crimes_data, crime_db):
    """Pass it a list of crime data. Will sort by date and add to crime_db's
    dict where crime's rank is the id. lower ranks imply earlier events"""

    crimes_list = []
    for crime_row in crimes_data:
        tmp_list = [0.0, 0, 0] #in format of: date, beat, type
        tmp_list[0] = crime_row[0]
        tmp_list[1] = beatMapper.get_hash(crime_row[3])
        tmp_list[2] = typeMapper.get_hash(crime_row[2])
        crimes_list.append(tmp_list)

    crimes_list_tuples = [tuple(l) for l in crimes_list]
    data_type = [('date', float), ('beat', int), ('type', int)]
    chrono_array = np.asarray(crimes_list_tuples, dtype=data_type)
    np.sort(chrono_array, order=['date', 'beat', 'type'])
    crime_instances = []

    for id_ctr, crime in enumerate(chrono_array):
        crime_instances.append(Crime())
        crime_instances[id_ctr].update_id(id_ctr)
        crime_instances[id_ctr].update_date_in_sec(crime[0])
        crime_instances[id_ctr].update_beat(crime[1])
        crime_instances[id_ctr].update_type(crime[2])
        crime_db.add_crime(crime_instances[id_ctr])

data = [] #stores all crime data
file_names = [] #stores names of xls filenames within the data/ directory
for root, dirs, filenames in os.walk(data_dir): #iterate over files
    for f in filenames:
        file_names.append(f)

x = multiprocessing_file_reader(file_names, 8)
for row in x:
    data.extend(row)

cdb = Crime_db() #create the crime database instance

fill_crime_db(data, cdb) #create and add crime instances to the database

X_data = np.array([], ndmin=2).reshape(-1, 2) #input
y_data = np.array([]) #output

for crime_key in cdb.crimes:
    row = np.array([ cdb.crimes[crime_key].date_in_sec, cdb.crimes[crime_key].beat ]) #date, beat
    X_data = np.vstack((X_data, row))

for i in range(5):
    print X_data[i]

#skf = cross_validation.StratifiedKFold(y_data, n_folds = 3)

#for i in range(0,1000,100):
#    print str(cdb.crimes[i].id) + ' ' + str(cdb.crimes[i].date_in_sec) + ' ' + str(beatMapper.get_key(cdb.crimes[i].beat)) + ' ' + str(typeMapper.get_key(cdb.crimes[i].type))

print 'time to complete: %ds' % (time.time() - start_time)
