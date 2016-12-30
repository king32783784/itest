#coding=utf8
import shelve 
import os
import sys
sys.path.append('..')
from common import *


# 创建数据保存database

def creat_result_database():
    if os.path.isfile('../result.db'):
         pass
    else:
        result_database = shelve.open('../result.db')
        try:
            localtime =  getlocattime()
            result_database['createdate'] = localtime
            result_database['machine'] = []
        finally:
            result_database.close()


def read_database(read_keys):
    result_database = shelve.open('../result.db', flag='r')
    try:
         existing = result_database[read_keys]
    except:
         return "NULL"
    finally:
         result_database.close()
    return existing

def write_database(data_key, data_value):
    result_database = shelve.open('../result.db')
    try:
        result_database[data_key] = data_value
    finally:
        result_database.close()

def append_database_list(data_index, data_value):
    result_database = shelve.open('../result.db', writeback=True)
    try:
        result_database[data_index].append(data_value)
    finally:
        result_database.close()

def update_database(data_index, data_key, data_value):
    result_database = shelve.open('../result.db', writeback=True)
    try:
        result_database[data_index][data_key] = data_value
    finally:
        result_database.close()
        

# test
# test = {'test1':"test1"}
creat_result_database()
append_database_list('machine', "local")
# write_database("test",test)
a = read_database('machine')
print(a)
# update_database('test', 'test1', 'test2')
# a = read_database('test')
# print(a)
