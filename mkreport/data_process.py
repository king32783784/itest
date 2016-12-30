# *-*coding=utf-8*-*
import os
import sys
sys.path.append('..')
from common import *
from data_operation import *
from data_capture import *

testtype = "performance"
result_filepath = "../current-result/"
Data_classlist = {'sysbenchcpu': Data_sysbenchcpu, 'sysbenchmem': Data_sysbenchmem,
                  'lmbench': Data_lmbench, 'pingpong': Data_pingpong, 'stream': Data_stream,
                  'iozone': Data_iozone, 'unixbench': Data_unixbench}

def save_current_data(testtype, result_file):
    testlist = get_aftertest_itemlist(testtype)
    src_file = result_filepath + testtype
    for testitem in testlist:
        src_file = os.path.join(src_file, testitem)
        src_file = os.path.join(src_file, "result/result.out")
        datacapture = Data_classlist[testitem]
        object_data = datacapture(src_file)
        item_data = object_data.getresultdata()
        print(testitem, item_data)
        src_file = result_filepath + testtype
    
save_current_data(testtype,result_filepath)
