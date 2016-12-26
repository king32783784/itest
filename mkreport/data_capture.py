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
 
    def datalist_search(self, search_pattern, testtime):
        def check_k(num):
            if 'K' in num:
                numtmp = float((re.sub('K', '0', num)))
                return numtmp * 1000
            else:
                return float(num)
        f = self.readfile()
        if f == "NULL":
            return 0
        else:
            data_cache_str = re.findall(r"%s" % search_pattern, f, re.S)
            datalist_average = []
            datalist_tmp = []
            for data in data_cache_str:
                datalist = data.split(' ')
                tmplist = []
                for num in datalist:
                    if len(num) > 0:
                        tmplist.append(num)
                datalist = map(check_k, tmplist)
                datalist_tmp.append(datalist)
            datalist_total = datalist_tmp[0]
            for datalist in datalist_tmp[1:]:
                datalist_total = map(lambda(a,b):a+b, zip(datalist, datalist_total))
            for data in datalist_total:
                datalist_average.append(round(data / testtime, 2))
            return datalist_average

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

class Data_stream(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("sysbenchmem")
        testtime = int(item_args["argts"])
        stream_threads = item_args["argt"].split(",")
        datalist_stream = []
        for thread in stream_threads:
            pattern_stream = "\\(%s\\)threads_result: (.*?)\n" % thread
            data_stream = self.datalist_search(pattern_stream, testtime)
            datalist_stream.append(data_stream)
        return datalist_stream

class Data_lmbench(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("lmbench")
        testtime = int(item_args["args"])
        pattern_lmbench = ["Processor_r  (.*?)\\n", "Context_r (.*?)\\n", "Local_r   (.*?)\\n",
                           "File_VM_r  (.*?)\\n", "Bandwidth (.*?)\\n"]
        datalist_lmbench = []
        for pattern in pattern_lmbench:
            data_part = self.datalist_search(pattern, testtime)
            datalist_lmbench.append(data_part)
        return datalist_lmbench

class Data_pingpong(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("pingpong")
        testtime = int(item_args["args"])
        pingpong_games = map(int,item_args["argt"].split(","))
        pingpong_threads = map(lambda(a):a * 2, pingpong_games)
        datalist_thread = []
        for thread in pingpong_threads:
            pingpong_pattern = "%s threads initialised in(.*?)usec" % thread
            data_thread = self.data_search(pingpong_pattern, testtime)
            datalist_thread.append(data_thread[0])
        datalist_games = []
        for game in pingpong_games:
            pingpong_pattern = "%s games completed in(.*?)msec" % game
            data_game = self.data_search(pingpong_pattern, testtime)
            datalist_games.append(data_game[0])
        datalist_pingpong = [datalist_thread, datalist_games]
        return datalist_pingpong

class Data_iozone(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        writers = ["Children see throughput for  1 initial writers \t=  (.*?)KB\\/sec",
                   "Children see throughput for  1 rewriters \t=  (.*?)KB\\/sec"]
        readers = ["Children see throughput for  1 readers \t\t= (.*?)KB\\/sec",
                   "Children see throughput for 1 re-readers \t= (.*?)KB\\/sec"]
        random_read_write = ["Children see throughput for 1 random readers \t= (.*?)KB\\/sec",
                              "Children see throughput for 1 random writers \t=  (.*?)KB\\/sec"]
        iozone_patternlist = {"0": writers, "1": readers, "2": random_read_write}                 
        item_args = get_item_temp_args("iozone")
        iozone_modelist = item_args["argi"].split(",")
        testtime = int(item_args["times"])
        datadict_iozone = {}
        for mode in iozone_modelist:
           iozone_pattern = iozone_patternlist[mode]
           datalist_iozone = []
           for pattern in iozone_pattern:
               data_iozone = self.data_search(pattern, testtime)
               datalist_iozone.append(data_iozone[0])
           datadict_iozone[mode] = datalist_iozone
        return datadict_iozone
               

class Data_unixbench(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("unixbench")
        print item_args      
        testtime = int(item_args["args"])
        unixbench_thread = item_args["argt"].split(",")
        datadict_unixbench = {}
        for thread in unixbench_thread:
            unixbench_pattern = "Threads_%s: (.*?)\n" % thread
            data_unixbench = self.data_search(unixbench_pattern, testtime)
            datadict_unixbench[thread] = data_unixbench[0]
        return datadict_unixbench      
           

# test
#a = DataCapture("result.out")
#a.data_search("execution time \(avg\/stddev\):(.*?)\/0.00")
# a = Data_sysbenchmem("result.out")
# data = a.getresultdata()
# print data
#a = get_item_temp_args("sysbenchmem")
#print a
# test stream
#a = Data_stream("result.out")
#data = a.getresultdata()
#print data
#a = Data_lmbench("result.out")
#data = a.getresultdata()
#print data
#a = Data_pingpong("result.out")
#data = a.getresultdata()
#print data
#a = Data_iozone("result.out")
#data = a.getresultdata()
#print data
#a = Data_unixbench("result.out")
#data = a.getresultdata()
#print data
