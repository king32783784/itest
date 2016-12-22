# coding: utf-8
# spec2000_cpau
sheet_speccpu_data = [
    [
        ["spec2000， bigger is better", "spec2000"],
        ["ITEM", "SPECint2000", "SPECfp2000", "SPECint_rate2000",\
        "SPECfp_rate2000"],
        ],
]
# sysbench_cpu
# sysbench_cpu_xls
sheet_syscpu_data = [
    [
        ["execution time, less is better", "sysbench"],
        ["ITEM", "10000", "20000", "30000"],
    ],
]
# sysbench_cpu_html
html_syscpu_data = []
# perf_graphics_xls
sheet_graphics_data = [
    [
        ["2D test results", "2D"],
        ["ITEM", "Qtperf", "unixbench-x11perf"],
    ],
    [
        ["3D test results", "3D"],
        ["ITEM", "Glmark", "unixbench-glxgears"],
    ],
]
html_graphics_data = []
# sysbench_mem
# sysbench_mem_xls
sheet_sysmem_data = [
    [
        ["Operations performed ops/sec", "sysbench"],
        ["ITEM", "4threads", "8threads"],
    ],
    [
        ["Transferred  MB/sec", "sysbench"],
        ["ITEM", "4threads", "8threads"],
    ],
]
# sysbench_mem_html
html_sysmem_data=[]
# iozone_io
# iozone_io_html
html_iozone_data = []
# iozone_io_xls
sheet_io_data = [
    [
        ["Variety of file operations KB/sec", "iozone"],
        ["ITEM", "Writer", "Re-writer", "Reader", "Re-reader", "Random Read", "Random Write"],
    ],
]
# pingpong_html
html_pingpong_data = []
# pingpong_xls
sheet_pingpong_data = [
    [
        ["Threads initialised usec", "pingpong"],
        ["ITEM", "32threads", "64threads", "128threads"],
    ],
    [
        ["Games completed usec", "pingpong"],
        ["ITEM", "16Games", "32Games", "64Games"],
    ],
]
# stream_html
html_stream_data = []
# stram_xls
sheet_stream_data = [
    [
        ["1Thread(MB/s)", "stream"],
        ["ITEM", "Copy", "Scale", "Add", "Triad"],
    ],
    [
        ["4Thread(MB/s)", "stream"],
        ["ITEM", "Copy", "Scale", "Add", "Triad"],
    ],
    [
        ["16Thread(MB/s)", "stream"],
        ["ITEM", "Copy", "Scale", "Add", "Triad"],
    ],
]
# system_html
html_system_data = []
# system_xls
sheet_system_data = [
    [
        ["unixbench system index", "unixbench"],
        ["ITEM", "1threads", "4thread"],
    ],
]
# browser_html
html_browser_data = []
# browser_xls
sheet_browser_data = [
    [
        ["Browser test", "browser"],
        ["ITEM", "css4", "acid3", "V8test", "octane", "html5", "dromaeotest"],
    ],
]  
# lmbench_html
html_lmbench_data = []
# lmbench_xls
sheet_lmbench_data =[
    [
        ["Processor, Processes - times in microseconds - smaller is better", \
        "Processor"],
        ["ITEM", "null call", "null I/O", "stat", "open clos", "slct TCP",\
         "sig inst", "sig hndl", "fork proc(k)", "exec porc(k)", "sh proc(k)"],
    ],
    [
        ["Context switching - times in microseconds - smaller is better",\
        "Context switching"],
        ["ITEM", "2p/0k", "2p/16k", "2p/64k", "8p/16k", "8p/64k", "16p/16k",\
        "16p/64k"],
    ],
    [
        ["*Local* Communication latencies in microseconds - smaller is better", "*Local* Communication latencie"],
        ["ITEM", "2p/0K ctxsw", "Pipe", "AF UNIX", "UDP", "TCP", "TCP conn"],
    ],
    [
        ["File & VM system latencies in microseconds - smaller is better", "File & VM system latencies"],
        ["ITEM", "0K Create", "0K Delete", "10K Create", "10K Delete", "Mmap Latency(K)", "Port Fault",
         "Page Fault", "100fd selct"],
    ],
    [
        ["*Local* Communication bandwidths in MB/s - bigger is better", "*Local* Communication bandwidths"],
        ["ITEM", "Pipe", "AF UNIX", "TCP", "File reread", "Mmap reread", "Bcopy(libc)", "Bcopy(hand)", "Mem read", "Mem write"],
    ],
]

# 匹配规则

patternmath = {'sysbenchcpu': [["execution time \(avg\/stddev\):(.*?)\/0.00", ],],
               'sysbenchmem': [["Operations performed: 2097152 \((.*?)ops\/sec\)",],
                            ["8192.00 MB transferred \((.*?)MB\/sec\)",]],
               'iozone': [["Children see throughput for  1 initial writers \t=  (.*?)KB\\/sec",
                           "Children see throughput for  1 rewriters \t=  (.*?)KB\\/sec",
                           "Children see throughput for  1 readers \t\t= (.*?)KB\\/sec",
                           "Children see throughput for 1 re-readers \t= (.*?)KB\\/sec",
                           "Children see throughput for 1 random readers \t= (.*?)KB\\/sec",
                           "Children see throughput for 1 random writers \t=  (.*?)KB\\/sec"],],
               'pingpong': [["32 threads initialised in(.*?)usec", "64 threads initialised in(.*?)usec",
                                "128 threads initialised in(.*?)usec"],
                               ["16 games completed in(.*?)msec", "32 games completed in(.*?)msec",
                                "64 games completed in(.*?)msec",]],
               'lmbench': [["Process_r(.*?)\n"], ["Context_r(.*?)\n"],
                               ["Local_r(.*?)\n"], ["File_VM_r(.*?)\n"],
                               ["Bandwidth(.*?)\n"]],
               'stream': [["\\(1\\)threads_result:(.*?)\n"], ["\\(4\\)threads_result:(.*?)\n"],
                               ["\\(4\\)threads_result:(.*?)\n"]],
               'Perf_graphics': [["Total: (.*?) s","2D Graphics Benchmarks Index Score(.*?)\n",],
                                  ["Your GLMark08 Score is (.*?)\\^\\_\\^", "3D Graphics Benchmarks Index Score(.*?)\n"],],
               'unixbench': [["Threads_1: (.*?)\n", "Threads_4: (.*?)\n"],],
               'Perf_browser': [["css4 result is (.*?)\n", "acid3 result is (.*?)\\/100", "V8test result is 总成绩: (.*?)\n",
                                 "octane result is 您的浏览器得分: (.*?)\n", "html5test result is (.*?)\n",
                                 "dromaeotest result is (.*?)\n"],],
                            }
patternnum = {'sysbenchcpu': 3, 'sysbenchmem':3, 'iozone':3, 'pingpong':3, 'lmbench':2, 'stream':3,
              'Perf_graphics': 3, 'unixbench': 3, 'Perf_browser':3}
totaldata = { 'speccpu': sheet_speccpu_data, 'sysbenchcpu': sheet_syscpu_data,
              "lmbench": sheet_lmbench_data, "sysbenchmem": sheet_sysmem_data,
              "iozone": sheet_io_data, "pingpong": sheet_pingpong_data,
              "stream": sheet_stream_data, "Perf_graphics": sheet_graphics_data,
              "unixbench": sheet_system_data, "Perf_browser": sheet_browser_data}
htmldata = {'sysbenchcpu' : html_syscpu_data, 'sysbenchmem': html_sysmem_data,
            'iozone': html_iozone_data, 'pingpong': html_pingpong_data,
            'lmbench': html_lmbench_data, 'stream': html_stream_data,
            'Perf_graphics': html_graphics_data, 'unixbench': html_system_data,
            'Perf_browser': html_browser_data,}
exceptitem = ("lmbench", "stream", "Perf_graphics", "Perf_browser")
