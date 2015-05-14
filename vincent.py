"""
Copyright (c) 2015 Rakshak Talwar
"""

import datetime, math, os, time
import numpy as np
import json
from sklearn import cross_validation
from sklearn.neighbors import KNeighborsClassifier

class Crime():
    """crime instance"""

    def __init__(self):
        self.id = -1
        self.date_in_sec = -1
        self.type = ''
        self.beat = ''
        self.n_instances = 0

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

    def update_n_instances(self, p_n_instances):
        if isinstance(p_n_instances, int):
            self.n_instances = p_n_instances
        elif isinstance(p_n_instances, float):
            self.n_instances = int(p_n_instances)
        else:
            raise TypeError

class Crime_db():
    """ stores crime instances in memory for use"""

    def __init__(self):
        self.crimes = dict()

    def _add_crime(self, p_crime):
        if isinstance(p_crime, Crime):
            self.crimes.update( { p_crime.id : p_crime } )

    def fill_crime_db(self, p_crimes_data, p_type_mapper, p_beat_mapper):
    """Pass it a list of crime data. Will sort by date and add to crime_db's
    dict where crime's rank is the id. lower ranks imply earlier events"""

    crimes_list = []
    for crime_row in crimes_data:
        tmp_list = [0.0, 0, 0, 0] #in format of: cTime, type, beat, numOffenses
        tmp_list[0] = crime_row[0]
        tmp_list[1] = type_mapper.get_hash(crime_row[1])
        tmp_list[2] = beat_mapper.get_hash(crime_row[2])
        tmp_list[3] = crime_row[3]
        crimes_list.append(tmp_list)

    crimes_list_tuples = [tuple(l) for l in crimes_list]
    data_type = [('cTime', float), ('type', int), ('beat', int), ('num_offenses', int)]
    chrono_array = np.asarray(crimes_list_tuples, dtype=data_type)
    np.sort(chrono_array, order=['cTime', 'type', 'beat', 'num_offenses'])

    crime_instances = []
    for id_ctr, crime in enumerate(chrono_array):
        crime_instances.append(Crime())
        crime_instances[id_ctr].update_id(id_ctr)
        crime_instances[id_ctr].update_date_in_sec(crime[0])
        crime_instances[id_ctr].update_type(crime[1])
        crime_instances[id_ctr].update_beat(crime[2])
        crime_instances[id_ctr].update_n_instances(crime[3])
        self._add_crime(crime_instances[id_ctr])

class Mapper():
    def __init__(self):
        self.key_to_hash = {};
        self.hash_to_key = {};

    def get_hash(self, key):
        if key not in self.key_to_hash:
            hash_val = len(self.key_to_hash)
            self.key_to_hash[key] = hash_val
            self.hash_to_key[hash_val] = key
        return self.key_to_hash[key]

    def get_key(self, hash_val):
        if hash_val in self.hash_to_key:
            return self.hash_to_key[hash_val]

