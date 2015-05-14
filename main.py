"""
Copyright (c) 2015 Rakshak Talwar
"""

import datetime, math, os, time
import numpy as np
import json, sqlite3
from sklearn import cross_validation
from sklearn.neighbors import KNeighborsClassifier
import vincent
start_time = time.time()

crime_database_file = 'crime_records.db'

beat_mapper = vincent.Mapper()
type_mapper = vincent.Mapper()

cdb = vincent.Crime_db() #create the Crime_db instance

#create and add crime instances to the database
db_con = sqlite3.connect(crime_database_file)
db_cur = db_con.cursor()
db_cur.execute('SELECT cTime, OffenseType, Beat, NumOffenses FROM HPDCrimes ORDER BY cTime ASC')

#convert the OffenseTypes and Beats to hashes
all_data_from_sql = []
first_crime = db_cur.fetchone() #grab the first crime
base_time = #this is base line from where time will be referenced

for crime in db_cur.fetchall():
    temp_list = []
    temp_list.append()

major_array = np.vstack(db_cur.fetchall())
split_major_array = np.hsplit(major_array, 4)

X_data = np.hstack((split_major_array[0], split_major_array[1], split_major_array[2]))
y_data = np.ravel(split_major_array[3])

scores = []
skf = cross_validation.StratifiedKFold(y_data, n_folds = 3) #create cross validation model
neigh = KNeighborsClassifier(n_neighbors=5) #create KNN model
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
            'beat': beatMapper.get_key(beat_id),
            'type': typeMapper.get_key(neigh.predict([time_i, beat_id])[0])
            }

        fut_week_crimes_list.append(temp_dict)
fut_week_crimes["crimes"] = fut_week_crimes_list
with open('future.json', 'w') as fl:
    json.dump(fut_week_crimes, fl)

print 'time to complete: %ds' % (time.time() - start_time)
