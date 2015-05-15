"""
Copyright (c) 2015 Rakshak Talwar
"""

import datetime, math, os, time
import numpy as np
import json, sqlite3
from sklearn.cross_validation import StratifiedKFold
from sklearn.neighbors import KNeighborsRegressor
import vincent
start_time = time.time()

crime_database_file = 'crime_records.db'

type_mapper = vincent.Mapper()
beat_mapper = vincent.Mapper()

#create and add crime instances to the database
db_con = sqlite3.connect(crime_database_file)
db_cur = db_con.cursor()
db_cur.execute('SELECT cTime, OffenseType, Beat, NumOffenses FROM HPDCrimes ORDER BY cTime ASC')

all_data_from_sql = []

base_time = 0.0 #this is base line from where time will be referenced
for ctr, crime in enumerate(db_cur.fetchall()):
    temp_list = []
    #find the base time
    if ctr == 0:
        base_time = float(crime[0])
    #add the time with respect to base_time
    temp_list.append(crime[0] - base_time)
    #convert the OffenseTypes and Beats to hashes
    temp_list.append(type_mapper.get_hash(crime[1]))
    temp_list.append(beat_mapper.get_hash(crime[2]))
    #add the number of offenses
    temp_list.append(crime[3])
    #append this temporary list to the main list which stores all the data
    all_data_from_sql.append(temp_list)

major_array = np.vstack(all_data_from_sql)
split_major_array = np.hsplit(major_array, 4)

X_data = np.hstack((split_major_array[0], split_major_array[1], split_major_array[2]))
y_data = np.ravel(split_major_array[3])

print type(y_data)

"""
scores = []
skf = StratifiedKFold(y_data, n_folds = 3) #create cross validation model
neigh = KNeighborsRegressor(n_neighbors=5) #create KNN model
for train_index, test_index in skf:
    X_train, X_test = X_data[train_index], X_data[test_index]
    y_train, y_test = y_data[train_index], y_data[test_index]
    neigh.fit(X_train, y_train)
    scores.append(neigh.score(X_test, y_test))
print("Mean(scores) = %.5f" % (np.mean(scores)))

#account for base time
#reverse hash lookup

#predictions for the next week

#find the current epoch time
times = [] #stores the normalized time in seconds of each day for the following days
for i in range(7):
    times.append((time.time() + i*86400) - base_time)

#create a dictionary to store future crimes
fut_week_crimes = dict()

fut_week_crimes_list = []
for time_i in times:
    for beat_id in beatMapper.hash_to_key:
        temp_dict = {
            'date' : time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_i+base_time)),
            'beat': beat_mapper.get_key(beat_id),
            'type': type_mapper.get_key(neigh.predict([time_i, beat_id])[0])
            }

        fut_week_crimes_list.append(temp_dict)
fut_week_crimes["crimes"] = fut_week_crimes_list
with open('future.json', 'w') as fl:
    json.dump(fut_week_crimes, fl)
"""
print 'time to complete: %ds' % (time.time() - start_time)