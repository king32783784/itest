#coding=utf8
import shelve 
import os
import sys

# 创建数据保存database

def create_result_database():
    if os.path.isfile('result.db'):
         pass
    else:
        result_database = shelve.open('result.db')
        try:
            pass
        finally:
            result_database.close()
        write_database('machine', [])
        write_database('OSLIST', ["test"])

def read_database(read_keys):
    if os.path.isfile('result.db'):
        result_database = shelve.open('result.db', flag='r')
        try:
            existing = result_database[read_keys]
        except:
            return "NULL"
        finally:
            result_database.close()
        return existing

def write_database(data_key, data_value):
    result_database = shelve.open('result.db', writeback=True)
    try:
        result_database[data_key] = data_value
    finally:
        result_database.close()

def append_database_list(data_index, data_value):
    old_list = read_database(data_index)
    print old_list
    old_list.append(data_value)
    write_database(data_index, old_list)

def update_database_item(data_index, data_key, data_value):
    result_database = shelve.open('result.db', writeback=True)
    try:
        result_database[data_index][data_key] = data_value
    finally:
        result_database.close()

def update_database(old_key, new_key):
    old_data = read_database(old_key)
    write_database(new_key, old_data)

def remove_database_item(data_index, data_value):
    result_database = shelve.open('result.db', writeback=True)
    try:
        result_database[data_index].remove(data_value)
    finally:
        result_database.close()
        

# test
#append_database_list('OSLIST', 'isoft01')
a = read_database('test')
print(a)
