# usr/bin/env python
# coding: utf-8
#######################################################################
#
# Performance Excel chart with Python and XlsxWriter.
#
# by lp 2016.6.24
#
import xlsxwriter
import sys
import string
reload(sys)
sys.setdefaultencoding('utf8')

# xls_dirt字典保存基础信息
sheet_speccpu_info = {
    'sheetname': '处理器运算',
    'testinfo': ("处理器运算性能", "测试工具：SPEC CPU 2000",
        "性能指标：Spec2000 包括 SPECint2000、SPECfp2000、\
             SPECint_rate2000、 SPECfp_rate2000 4个测试项",
        "对比说明：其中的得分越大说明CPU性能越高",
        "测试参数：runspec -c test.cfg -i ref -n 3 -r -u 4 -I all;\
                   runspec -c test.cfg -i ref -n 3 -I all", ),
    "oslist": ["isoft_desktop V4.0 loongson", "Deepin15_mips_20160520",
               "Neokylin Desktop-7.0-loongson"],
    }

sheet_syscpu_info = {
    'sheetname': '处理器运算_B',
    'testinfo': ("处理器运算性能", "测试工具：sysbench",
        "性能指标: 包括10000、20000、30000",
        "对比说明: 数值越小越好",
        "测试参数：sysbench --test=cpu --cpu-max-prime=10000/20000/30000 run",
         ),
     'oslist': ["isoft_desktop V4.0 loongson", "Deepin15_mips_20160520",
                "Neokylin Desktop-7.0-loongson"],}
sheet_iozone_info = {
    'sheetname': 'IO读写',
    'testinfo': ("I/O读写性能", "测试工具:iozone3",
        "性能指标: 包括IO的写、重复写、读、重复读、随机写、随机读等指标",
        "对比说明：测试结果均为3次平均值， 数值越大，说明I/O性能越好",
        "测试参数：./iozone -s 16G -i 0 -i 1 -i 2 -t 1 -r 1M",),
    'oslist': [],}
sheet_pingpong_info = {
    'sheetname': "线程操作",
    'testinfo': ("线程操作性能", "测试工具： ping-pong",
         "性能指标： 包含 16、32、64 tables的性能",
         "对比说明：测试结果均为3次平均值， 数值越小，说明响应越快，性能越好",
         "测试参数：#./Runtest.sh 16 32 64",),
    'oslist':[],}
sheet_sysmem_info = {
    'sheetname': "内存操作",
    'testinfo': ("内存操作性能", "测试工具: sysbench", "性能指标: \
                 包括4/8线程内存操作速度和带宽", "对比说明：\
                 测试结果为３次求平均值","测试参数:sysbench\
                 --test=memory --num-threads=4/8 --memory-block-size=8192\
                 --memory-total-size=4G run"),
    'oslist':["testos"]
}
sheet_lmbench_info = {
    'sheetname': '内核',
    'testinfo': ("内核性能测试","测试工具：lmbench", 
        "性能指标：选取了Processor、Context switching、*Local* Communication\
         latencies 、File & VM system latencies 、\n    *Local* Communication\
         bandwidths等指标", "对比说明：测试结果均为测试3次求平均值",
         "测试参数：以root用户执行测试，运行make result，之后继续运行两次\
         make rerun，最后执行make see"),
    'oslist': ["testos"],
    }
sheet_stream_info = {
    'sheetname': '内存',
    'testinfo': ("内存性能测试","测试工具：stream",
        "性能指标：Copy, Scale, Add, Triad", "对比说明：测试结果均为测试3次求平均值",
         "测试参数：以root用户执行测试，分别执行stream 单线程　４线程　１６线程测试"),
    'oslist': ["testos"],
    }
sheet_graphics_info = {
    'sheetname': '图形显示',
    'testinfo': ("图形显示性能测试", "测试工具：qtperf unixbench glmark",
         "性能指标：2D 3D","对比说明:测试结果为测试３次的平均值",
         "测试参数：qtperf默认，unixbench默认，glmark指定分辨率"),
    'oslist': ["testos"],
}
sheet_system_info = {
    'sheetname': '系统基准',
    'testinfo': ("系统基准性能测试", "测试工具：unixbench",
         "性能指标：1threads 4threads","对比说明:测试结果为测试３次的平均值",
         "测试参数：1/4threads"),
    'oslist': ["testos"],
}
sheet_browser_info = {
    'sheetname': '浏览器',
    'testinfo': ("浏览器性能测试", "测试工具：Browsertest",
         "性能指标：css4/acid3/v8test/octane/html5/dromaeotest","对比说明:测试结果为测试３次的平均值",
         "测试参数：默认"),
    'oslist': ["testos"],
}
# format_dirt字典保存格式化信息
# 结果图表title格式
formtitle_format = {
    'bold': False,   # 设置加粗
    'border': 1,  # 设置边框格式
    'fg_color': '#CC99FF',  # 设置单元格填充颜色
    'font_size': 10,   # 设置字体大小
    'align': 'center',  # 设置对齐方式
    'valign': 'vcenter',  # 设置对齐方式
}
# 页title格式
sheettitle_format = {
    'bold':     True,
    'border':   1,
    'font_size': 14,
    'font_color': '#FFFF99',
    'align':    'center',
    'valign':   'vcenter',
    'fg_color': '#333399',
}

# 测试说明信息格式

info_fortmat = {
    'bold': False,
    'border': 1,
    'font_size': 10,
    'align': 'left',
    'valign': 'vcenter',
    'fg_color': '#B8CCE4',
}

# 测试结果表格副标题格式
formsubtitle_format = {
    'bold': True,
    'border': 1,
    'font_size': 12,
    'align': 'left',
    'valign': 'vcenter',
    'fg_color': '#339966',
}

# 测试结果数值格式
result_format = {
    'bold': False,
    'border': 1,
    'font_size': 10,
    'align': 'center',
    'valign': 'vcenter',
    'num_format': '0.00',
}

# 测试项目名称格式
item_format = {
    'bold': False,
    'border': 1,
    'font_size': 10,
    'align': 'left',
    'valign': 'vcenter',
    'fg_color': '#CCFFFF',
}

# 测试结果分析title格式
resulttitle_format = {
    'bold': True,
    'border': 1,
    'font_size': 12,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#339966',
}
