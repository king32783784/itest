#/usr/bin/env python
# coding: utf-8
'''
    Name: Test report automatically generate tool
    Function: Automatically generate performance test results xls format report
              with Python and XlsxWriter
    Author: peng.li@i-soft.com.cn
    Date :20160701
'''
import os
import sys
from processingcontrol import *
reload(sys)
sys.setdefaultencoding('utf8')

if __name__== "__main__":
    reciveargs = {}
    reciveargs['osnames'] = ["itest-20161213033232"]
    reciveargs['type'] = ["html", "xls"]
    reciveargs['items'] = ["sysbenchcpu", "sysbenchmem", "stream", "iozone", "pingpong", "unixbench"]
    maincontrol = Control_processing(reciveargs)
    maincontrol._mkxls()

# reciveargs={'items': ['cpu', 'mem'], 'type': ['xls', 'html'], 'osnames': ['iSoft_Desktop_4.0', 'deepin']}
# error: lmbench
