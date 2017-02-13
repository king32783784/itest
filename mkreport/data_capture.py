#*-* coding=utf-8 *-*
import re
import sys
from common import *
from data_operation import *


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

    def info_search(self, search_pattern):
        f = self.readfile()
        if f == "NULL":
            return "unknow"
        else:
            info_cache_str = re.findall(r"%s" % search_pattern, f, re.S)
        return info_cache_str

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


# sysbenchcpu 数据处理
class Data_sysbenchcpu(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        pattern_sysbenchcpu = "execution time \(avg\/stddev\):(.*?)\/0.00"
        item_args = get_item_temp_args("sysbenchcpu")
        cpu_items = item_args["argp"].split(',')
        testtime = int(item_args["args"])
        num_sysbenchcpu = self.data_search(pattern_sysbenchcpu, testtime)
        data_sysbenchcpu = {}
        for i, value in enumerate(cpu_items):
            data_sysbenchcpu[value] = num_sysbenchcpu[i]
        data_sysbenchcpu["threads"] = item_args["argt"]
        data_sysbenchcpu["cpu_args"] = cpu_items
        return data_sysbenchcpu


# sysbenchmem数据处理
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
        data_sysbenchmem = {}
        data_sysbenchmem["threads"] = item_args["argt"]
        data_sysbenchmem["ops"] = data_sysbenchmem_ops
        data_sysbenchmem["rate"] = data_sysbenchmem_rate
        return data_sysbenchmem


# stream数据处理
class Data_stream(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("stream")
        testtime = int(item_args["args"])
        stream_threads = item_args["argt"].split(",")
        datalist_stream = {}
        for thread in stream_threads:
            pattern_stream = "\\(%s\\)threads_result: (.*?)\n" % thread
            data_stream = self.datalist_search(pattern_stream, testtime)
            datalist_stream[thread]= data_stream
        stream_args = ["Copy", "Scare", "Add", "Triad"]
        datalist_stream["stream_args"] = stream_args
        datalist_stream["threads"] = stream_threads
        return datalist_stream


# lmbench数据处理
class Data_lmbench(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("lmbench")
        testtime = int(item_args["args"])
        pattern_lmbench = ["Processor_r  (.*?)\\n", "Context_r (.*?)\\n", "Local_r   (.*?)\\n",
                           "File_VM_r (.*?)\\n", "Bandwidth (.*?)\\n"]
        lmbench_item = ["Processor", "Context", "Local_latencies", "File", "Local_bandwidths"]
        datalist_lmbench = {}
        for i, pattern in enumerate(pattern_lmbench):
            data_part = self.datalist_search(pattern, testtime)
            datalist_lmbench[lmbench_item[i]] = data_part
        datalist_lmbench["lmbenchitem"] = lmbench_item
        return datalist_lmbench


# pingpong数据处理
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
        datalist_pingpong = {}
        datalist_pingpong["tables"]=pingpong_games
        datalist_pingpong["thread"] = datalist_thread
        datalist_pingpong["games"] = datalist_games
        return datalist_pingpong


# iozone数据处理
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
        datadict_iozone["modelist"] = iozone_modelist
        datadict_iozone["rblock"] = item_args["argr"]
        datadict_iozone["filesize"] = item_args["args"]
        datadict_iozone["threads"] = item_args["argt"]
        return datadict_iozone
               

# unixbench数据处理
class Data_unixbench(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("unixbench")
        testtime = int(item_args["args"])
        unixbench_thread = item_args["argt"].split(",")
        datadict_unixbench = {}
        for thread in unixbench_thread:
            unixbench_pattern = "Threads_%s: (.*?)\n" % thread
            data_unixbench = self.data_search(unixbench_pattern, testtime)
            datadict_unixbench[thread] = data_unixbench[0]
        datadict_unixbench["threads"] = unixbench_thread
        return datadict_unixbench      


# acid数据处理
class Data_Acid(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("acid")
        testtime = int(item_args["args"])
        acid_browser = item_args["argt"].split(",")
        datadict_acid = {}
        for browser in acid_browser:
            pattern = "%s acid result: (.*?)\n" % browser
            data_acid= self.data_search(pattern, testtime)
            datadict_acid[browser] = data_acid[0]
        datadict_acid["browsetype"] = acid_browser
        return datadict_acid  


# css数据处理
class Data_Css(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("acid")
        testtime = int(item_args["args"])
        css_browser = item_args["argt"].split(",")
        datadict_css = {}
        for browser in css_browser:
            pattern = "%s css result: (.*?)\n" % browser
            data_css = self.data_search(pattern, testtime)
            datadict_css[browser] = data_css[0]
        datadict_css["browsetype"] = css_browser
        return datadict_css


# html数据处理
class Data_Html(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("acid")
        testtime = int(item_args["args"])
        html_browser = item_args["argt"].split(",")
        datadict_html = {}
        for browser in html_browser:
            pattern = "%s html5 result: (.*?)\n" % browser
            data_html = self.data_search(pattern, testtime)
            datadict_html[browser] = data_html[0]
        datadict_html["browsetype"] = html_browser
        return datadict_html


# octane数据处理
class Data_Octane(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("acid")
        testtime = int(item_args["args"])
        octane_browser = item_args["argt"].split(",")
        datadict_octane = {}
        for browser in octane_browser:
            pattern = "%s octane result: (.*?)\n" % browser
            data_octane = self.data_search(pattern, testtime)
            datadict_octane[browser] = data_octane[0]
        datadict_octane["browsetype"] = octane_browser
        return datadict_octane


# dromaeo数据处理
class Data_Dromaeo(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("acid")
        testtime = int(item_args["args"])
        dromaeo_browser = item_args["argt"].split(",")
        datadict_dromaeo = {}
        for browser in dromaeo_browser:
            pattern = "%s dromaeo result: (.*?)\n" % browser
            data_dromaeo = self.data_search(pattern, testtime)
            datadict_dromaeo[browser] = data_dromaeo[0]
        datadict_dromaeo["browsetype"] = dromaeo_browser
        return datadict_dromaeo


# v8数据处理
class Data_V8(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("acid")
        testtime = int(item_args["args"])
        v8_browser = item_args["argt"].split(",")
        datadict_v8 = {}
        for browser in v8_browser:
            pattern = "%s v8 result: (.*?)\n" % browser
            data_v8 = self.data_search(pattern, testtime)
            datadict_v8[browser] = data_v8[0]
        datadict_v8["browsetype"] = v8_browser
        return datadict_v8


# glmark数据处理
class Data_Glmark(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("glmark")
        testtime = int(item_args["args"])
        datadict_glmark = {}
        pattern = "Your GLMark08 Score is (.*?) "
        data_glmark = self.data_search(pattern, testtime)
        datadict_glmark['glmark'] = data_glmark[0]
        return datadict_glmark


# qtperf数据处理
class Data_Qtperf(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("qtperf")
        testtime = int(item_args["args"])
        datadict_qtperf = {}
        pattern = "Total: (.*?) s"
        data_qtperf = self.data_search(pattern, testtime)
        datadict_qtperf['qtperf'] = data_qtperf[0]
        return datadict_qtperf


# x11perf数据处理
class Data_X11perf(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("x11perf")
        testtime = int(item_args["argt"])
        datadict_x11perf = {}
        pattern = "2D Graphics Benchmarks Index Score                                  (.*?)\n"
        data_x11perf = self.data_search(pattern, testtime)
        datadict_x11perf['x11perf'] = data_x11perf[0]
        return datadict_x11perf


# ubgears数据处理
class Data_Ubgears(DataCapture):
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        item_args = get_item_temp_args("ubgears")
        testtime = int(item_args["argt"])
        datadict_ubgears = {}
        pattern = "3D Graphics Benchmarks Index Score                                  (.*?)\n"
        data_ubgears = self.data_search(pattern, testtime)
        datadict_ubgears['ubgears'] = data_ubgears[0]
        return datadict_ubgears

# hw数据处理
class Data_Hw(DataCapture):
    parttern_hw = {
        "cpuinfo": "cpuinfo: (.*?)\n",
        "mbinfo": "mbinfo: (.*?)\n",
        "biosinfo": "biosinfo: (.*?)\n",
        "meminfo": "meminfo: (.*?)\n",
        "northbridge": "northbridge: (.*?)\n",
        "sorthbridge": "sorthbridge: (.*?)\n",
        "gfcinfo": "gfcinfo: (.*?)\n",
        "audioinfo": "audioinfo: (.*?)\n",
        "net": "net: (.*?)\n",
        "wlan": "wlan: (.*?)\n",
        "sata": "sata: (.*?)\n",
        "hdd": "hdd: (.*?)\n",
        "odd": "odd: (.*?)\n",
        "raid": "raid: (.*?)\n",
        "blue": "blue: (.*?)\n",
        "kb": "kb: (.*?)\n",
        "ms": "ms: (.*?)\n",
        "usb": "usb: (.*?)\n"}

    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        data_hw = {}
        for key, value in self.parttern_hw.iteritems():
            data_hw[key] = self.info_search(value)
        return data_hw


# sw数据处理
class Data_Sw(DataCapture):
    pattern_sw = {
        "os": "os: (.*?)\n",
        "kernel": "kernel: (.*?)\n",
        "fs": "fs: (.*?)\n",
        "gcc": "gcc: (.*?)\n",
        "glibc": "glibc: (.*?)\n",
        "env": "env: (.*?)\n",
        "qt": "qt: (.*?)\n",
        "xorg": "xorg: (.*?)\n",
        "mesa": "mesa: (.*?)\n",
        "java": "java: (.*?)\n",
        "browser": "browser: (.*?)\n",  
        "nbdriver": "nbdriver: (.*?)\n",
        "sbdriver": "sbdriver: (.*?)\n",
        "gfcdriver": "gfcdriver: (.*?)\n",
        "audiodriver": "audiodriver: (.*?)\n",
        "landriver": "landriver: (.*?)\n",  
        "wlandriver": "wlandriver: (.*?)\n",
        "raiddriver": "raiddriver: (.*?)\n"}
 
    def __init__(self, result_file):
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        data_sw = {}
        for key, value in self.pattern_sw.iteritems():
            data_sw[key] = self.info_search(value)
        return data_sw


# INFO数据处理
class Data_All(DataCapture):
    def __init__(self, result_file):
        self.result_file = result_file
        DataCapture.__init__(self, result_file)

    def getresultdata(self):
        data_all = {}
        data_hw = Data_Hw(self.result_file)
        datahw = data_hw.getresultdata()
        data_sw = Data_Sw(self.result_file)
        datasw = data_sw.getresultdata()
        data_all = dict(datahw, **datasw)
        return data_all



# 数据处理列表
Data_classlist = {'sysbenchcpu': Data_sysbenchcpu,
                  'sysbenchmem': Data_sysbenchmem,
                  'lmbench': Data_lmbench,
                  'pingpong': Data_pingpong,
                  'stream': Data_stream,
                  'iozone': Data_iozone,
                  'unixbench': Data_unixbench,
                  'acid': Data_Acid,
                  'css': Data_Css,
                  'v8': Data_V8,
                  'dromaeo': Data_Dromaeo,
                  'octane': Data_Octane,
                  'html': Data_Html,
                  'glmark': Data_Glmark,
                  'qtperf': Data_Qtperf,
                  'x11perf': Data_X11perf,
                  'ubgears': Data_Ubgears,
                  'hw': Data_Hw,
                  'sw': Data_Sw,
                  'all': Data_All}

result_filepath = "current-result/"

# 保存当前测试结果
def save_current_data():
    typelist = get_aftertest_typelist() # 获取测试type列表
    testlist = get_aftertest_itemlist(typelist[0]) # 获取type对应的测试列表;目前只处理perf
    src_file = result_filepath + typelist[0]
    data_os_result = {}
    for testitem in testlist:
        src_file = os.path.join(src_file, testitem)
        src_file = os.path.join(src_file, "result/result.out")
        datacapture = Data_classlist[testitem]
        object_data = datacapture(src_file)
        item_data = object_data.getresultdata()
        data_os_result[testitem] = item_data
        src_file = result_filepath + typelist[0]
    data_os_result["testlist"] = testlist
    write_database("test", data_os_result)


# test
# 保存数据
if __name__ == "__main__": 
     save_current_data() 

# a = Data_sysbenchcpu("../current-result/performance/sysbenchcpu/result/result.out")
# data = a.getresultdata()
# print data

# a = Data_sysbenchmem("../current-result/performance/sysbenchmem/result/result.out")
# data = a.getresultdata()
# print data

# test stream
# a = Data_stream("../current-result/performance/stream/result/result.out")
# data = a.getresultdata()
# print data

# a = Data_lmbench("../current-result/performance/lmbench/result/result.out")
# data = a.getresultdata()
# print data

# a = Data_pingpong("../current-result/performance/pingpong/result/result.out")
# data = a.getresultdata()
# print data


# a = Data_iozone("../current-result/performance/iozone/result/result.out")
# data = a.getresultdata()
# print data

# a = Data_unixbench("../current-result/performance/unixbench/result/result.out")
# data = a.getresultdata()
# print data
