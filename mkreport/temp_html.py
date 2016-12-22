# sysbench_cpu
md_syscpu = [
    '''

##sysbench - Performance Test of CPU

###CPU Execution time(second) - 1thread

*OS* | *10000* | *20000* | *30000*
------ | --------- | --------- | ---------''',
]
chart_syscpu = [{
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'CPU Execution time (sec)',
          'osnames': [],
          'subjects': ('1000', '2000', '3000'),
          'scores': [[10.844, 28.028, 48.917], [11.304, 28.860, 50.346]],
          'pngname': 'current-report/svgfile/syscpu0.png'
           }, ]
# sysbench_browser
md_browser = [
    '''

##Browser - Performance Test of browser

###Browser test suite

*OS* | *css4* | *acid3* | *V8test* | *octane* | *html5* | *dromaeotest*
---- | ------ | ------- | -------- | -------- | ------- | ------------''',
]
chart_browser = [{
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'Browser test ',
          'osnames': [],
          'subjects': ('css4', 'acid3', 'V8test', 'octane', 'html5', 'dromaetest'),
          'scores': [[10.844, 28.028, 48.917], [11.304, 28.860, 50.346]],
          'pngname': 'current-report/svgfile/browser0.png'
           }, ]

# sysbench_mem
md_sysmem = [
    '''

##sysbench - Performance Test of MEM

###MEM Operations performed - 4threads & 8 threads

*OS* | *4threads(ops/sec)* | *8threads(ops/sec)*
------ | ------------------- | ----------------''',
    '''

###MEM Transfer rate - 4threads & 8 threads

*OS* | *4threads(MB/sec)* | *8threads(MB/sec)*
------ | ------------------- | ------------------'''
]
chart_sysmem = [{
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'MEM Operations performed (ops/sec)',
    'osnames': [],
    'subjects': ('4threads', '8threads'),
    'scores': ([3324739.04, 3298945.06], [3351746.42, 3457950.96]),
    'pngname': 'current-report/svgfile/sysmem0.png'},
    {
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'Mem Transfer Rate (MB/s)',
    'osnames': [],
    'subjects': ('4threads', '8threads'),
    'scores': ([12987.26, 12886.51], [13092.76, 13507.62]),
    'pngname': 'current-report/svgfile/sysmem1.png'}, ]
# pingpong_thread
md_pingpong = [
    '''

##Pingpong - Performance Test of Threads

###Threads initialised - times in microseconds - smaller is better

*OS* | *Tables 16* | *Tables 32* | *Tables 64*
------ | ------------- | ------------- | ------------''',
    '''

###Games completed - times in microseconds - smaller is better

*OS* | *Tables 16* | *Tables 32* | *Tables 64*
------ | ------------ | ------------ | ------------'''
]
chart_pingpong = [{
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'Threads initialised(usec)',
    'osnames': [],
    'subjects': ('32threads', '64threads', '128threads'),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'current-report/svgfile/pingpong0.png'},
    {
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'Games completed (usec)',
    'osnames': [],
    'subjects': ('16Games', '32Games', '64Games'),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'current-report/svgfile/pinpong1.png'}, ]

# stream_thread
md_stream = [
    '''

##Stream - Performance Test of memory

###1 Threads test - MB/s - more is better

*OS* | *Copy* | *Scare* | *Add* | *Triad*
---- | ------ | --------| ----- | ------''',
    '''

###4 Threads test - MB/s - more is better

*OS* | *Copy* | *Scare* | *Add* | *Triad*
-----| -------| ------- | ----- | -------''',
    '''

###16 Threads test - MB/s - more is better

*OS* | *Copy* | *Scare* | *Add* | *Triad*
-----| -------| ------- | ----- | -------''',
]
chart_stream = [{
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': '1threads test(MB/s)',
    'osnames': [],
    'subjects': ('Copy', 'Scare', 'Add', 'Triad'),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'current-report/svgfile/stream0.png'},
    {
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': '4threads test(MB/s)',
    'osnames': [],
    'subjects': ('Copy', 'Scare', 'Add', 'Triad'),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'current-report/svgfile/stream1.png'}, 
    {
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': '16threads test(MB/s)',
    'osnames': [],
    'subjects': ('Copy', 'Scare', 'Add', 'Triad'),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'current-report/svgfile/stream2.png'}, 
]
# graphics
md_graphics = [
    '''

##Graphics - Performance Test of Graphic

###2Dtest - Qtperf(sec)smaller is better - X11perf more is better

*OS* | *Qtperf* | *X11perf*
------ | ------------- | -------------''',
    '''

###3Dtest - Glmark & glxgers - more is better

*OS* | *Glmark* | *Glxgears*
------ | ------------ | ------------ | ------------'''
]
chart_graphics = [{
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': '2D Test',
    'osnames': [],
    'subjects': ('Qtperf', 'X11perf'),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'current-report/svgfile/graphics0.png'},
    {
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': '3D Test',
    'osnames': [],
    'subjects': ('Glmark', 'Glxgears'),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'current-report/svgfile/graphics1.png'}, ]

# lmbench_kernel

md_lmbench = [
    '''

##Lmbench - Performance Test of Kernel

###Processor, Processes - times in microseconds - smaller is better

*OS* | *null call* | *null I/O* | *stat* | *open clos* | *slct TCP* | *sig inst* | *sig hndl* | *fork proc* | *exec proc* | *sh proc*
---- | --------- | ---------- | ------ | ----------- | ---------- | ---------- | ---------- | ----------- | ----------- | ---------''',
    '''

###Context switching - times in microseconds - smaller is better

*OS* | *2p/0K ctxsw* | *2p/16K ctxsw* | *2p/64K ctxsw* | *8p/16K ctxsw* | *8p/64K ctxsw* | *16p/16K ctxsw* | *16p/64K ctxsw*
------ | ------------- | -------------- | -------------- | -------------- | -------------- | --------------- | ---------------''',
    '''

###\*Local\* Communication latencies in microseconds - smaller is better

*OS* | *2p/0K ctxsw* | *Pipe* | *AF UNIX* | *UDP* | *RPC/UDP* | *TCP* | *RPC/TCP* | *TCP conn*
------ | ------------- | ------ | --------- | ----- | --------- | ----- | --------- | ----------''',
    '''

###File & VM system latencies in microseconds - smaller is better

*OS* | *0K File Create* | *0K File Delete* | *10K File Create* | *10K File Delete* | *Mmap Latency* | *Prot Fault* | *Page Fault* | *100fd selct*
------ | ---------------- | ---------------- | ----------------- | ----------------- | -------------- | ------------ | ------------ | ------------''',
    '''

###\*Local\* Communication bandwidths in MB/s - bigger is better

*OS* | *Pipe* | *AF UNIX* | *TCP* | *File reread* | *Mmap reread* | *Bcopy(libc)* | *Bcopy(hand)* | *Mem read* | *Mem write*
------ | ------ | --------- | ----- | ------------- | ------------- | ------------- | ------------- | ---------- | ---------''',
]
chart_lmbench = [{
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'Processor(usec)',
    'osnames': [],
    'subjects': ('null\ncall', 'null\nI/0', "slct\nTCP",\
         "sig\ninst", "sig\nhndl", "fork\nproc", "exec\nporc", "sh\nproc"),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'current-report/svgfile/lmbench0.png'},
    {
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'Context Switching (usec)',
    'osnames': [],
    'subjects': ("2p/0k", "2p/16k", "2p/64k", "8p/16k", "8p/64k", "16p/16k",\
        "16p/64k"),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'current-report/svgfile/lmbench1.png'},
    {
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': '*Local* Communication latencies (usec)',
    'osnames': [],
    'subjects': ("2p/0K\nctxsw", "Pipe", "AF\nUNIX", "UDP", "TCP", "TCP\nconn"),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'current-report/svgfile/lmbench2.png'},
    {
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'File & VM system latencies (usec)',
    'osnames': [],
    'subjects': ("0K\nCreate", "0K\nDelete", "10K\nCreate", "10K\nDelete", "Mmap\nLatency(K)", "Port\nFault",
         "Page\nFault", "100fd\nselct"),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'current-report/svgfile/lmbench3.png'},
    {   
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': '*Local* Communication bandwidths(MB/s)',
    'osnames': [],
    'subjects': ("Pipe", "AF\nUNIX", "TCP", "File\nreread", "Mmap\nreread", "Bcopy\n(libc)", "Bcopy\n(hand)", "Mem\nread", "Mem\nwrite"),
    'scores': ([0, 0, 0], [1, 1, 1]),
    'pngname': 'current-report/svgfile/lmbench4.png'}, 
 ]
# iozone_io
md_iozone = [
    '''

##iozone - Performance Test of IO

###Variety of file operations

*OS* | *Write* | *Rewrite* | *Read* | *Reread* | *Rondom read* | *Rondom write*
-----| ------- | --------- | ------ | -------- | ------------- | --------------'''
]
chart_iozone = [{
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'Variety of file operatios KB/sec',
    'osnames': [],
    'subjects': ('Write', 'Rewrite', 'Read', 'Reread', 'Rondom read', 'Rondom write'),
    'scores': ([3324739.04, 3298945.06, 12222, 124123, 12344, 12344],),
    'pngname': 'current-report/svgfile/iozone0.png'},]

# unixbench_system
md_system = [
    '''

##Unixbench - Performance Test of system

###system index

*OS* | *1threads* | *4threads* 
-----| ---------- | ---------'''
]
chart_system = [{
    'custom_font': '/usr/share/fonts/goffer.ttf',
    'title': 'system index',
    'osnames': [],
    'subjects': ('1threads', '4threafs'),
    'scores': ([3324739.04, 3298945.06],),
    'pngname': 'current-report/svgfile/unixbench0.png'},]

