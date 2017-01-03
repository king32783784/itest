#coding=utf8
import shelve 
import os
import sys
sys.path.append('..')
from common import *


# 创建数据保存database

def create_result_database():
    if os.path.isfile('../result.db'):
         pass
    else:
        result_database = shelve.open('../result.db')
        try:
            localtime =  getlocattime()
            result_database['createdate'] = localtime
            result_database['machine'] = []
            result_database['OS'] = []
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
"""
creat_result_database()
# 添加机器名称
append_database_list('machine', "DELL")
# 添加OS名称
append_database_list('OS', "loacl")
# write_database("test",test)
# 添加OS对应测试项目列表
local_testlist = ["test1", "test2", "test3"]  # local对应测试列表
sysbenchcpu = {"10000":3, "20000":4, "30000":32}       # test1 对应项目及数值
iozone = {"read":20000, "re_read":400000, "write":200000}
operations = {"4threads":2000, "8threads": 3000}
transferrate = {"4threads":3000, "8threads": 4000}
sysbenchmem = {"operations":operations, "transferrate":transferrate}
local_testdata = {"sysbenchcpu":sysbenchcpu, "iozone":iozone, "sysbenchmem":sysbenchmem}
#write_database("local", ["test1", "test2", "test3"])
write_database("local", local_testdata)
# 解析参数
a = read_database('local')
testlist = []
for key, value in a.iteritems():
    print key, value
print "test list is %s" % testlist
# update_database('test', 'test1', 'test2')
# a = read_database('test')
# print(a)
"""
