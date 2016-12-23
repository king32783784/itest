#*-* coding=utf-8 *-*
import re
import sys
sys.path.append('..')
from common import *

class DataCapture(object):
    def __init__(self, result_file):
        self.result_file = result_file

    def readfile(self):
        try:
            fopen = open(self.result_file, 'r')
            f = fopen.read().strip()
            return f
        except OSError:
            return NULL

    def data_search(self, search_pattern, testtime):
        f = self.readfile()
        if f == "NULL":
            return 0
        else:
            data_cache_str = re.findall(r"%s" % search_pattern, f, re.S)
        data_cache = map(float, data_cache_str)
        data_average = []
        j = 0
        for i, data in enumerate(data_cache, 1):
            if i % testtime == 0:
                data_average.append((sum(data_cache[j:i]) / testtime))
                j = i
        data_average = map(lambda(num):format(num, '0.2f'), data_average)
        return data_average

class Data_sysbenchcpu(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        pattern_sysbenchcpu = "execution time \(avg\/stddev\):(.*?)\/0.00"
        item_args = get_item_temp_args("sysbenchcpu")
        testtime = int(item_args["args"])
        data_sysbenchcpu = self.data_search(pattern_sysbenchcpu, testtime)
        return data_sysbenchcpu

class Data_sysbenchmem(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)
    
    def getresultdata(self):
        item_args = get_item_temp_args("sysbenchmem")
        testtime = int(item_args["argts"])
        sysbenchmem_ops = int(item_args["args"]) * 1024 * 1024 * 1024 / int(item_args["argb"])
        sysbenchmem_rate = int(item_args["args"]) * 1024
        pattern_sysbenchmem_ops = "Operations performed: %s \((.*?)ops\/sec\)" % sysbenchmem_ops
        pattern_sysbenchmem_rate =  "%s.00 MB transferred \((.*?)MB\/sec\)" % sysbenchmem_rate
        data_sysbenchmem_ops = self.data_search(pattern_sysbenchmem_ops, testtime)
        data_sysbenchmem_rate = self.data_search(pattern_sysbenchmem_rate, testtime)
        data_sysbenchmem = [data_sysbenchmem_ops, data_sysbenchmem_rate]
        return data_sysbenchmem

# test
#a = DataCapture("result.out")
#a.data_search("execution time \(avg\/stddev\):(.*?)\/0.00")
a = Data_sysbenchmem("result01.out")
data = a.getresultdata()
print data
#a = get_item_temp_args("sysbenchmem")
#print a
