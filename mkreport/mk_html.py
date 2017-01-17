# coding=utf-8
import os
import sys
import shutil
from subprocess import call, PIPE, Popen
from mkchart import *
from temp_html import *
from data_operation import *


class Create_Md(object):
    def __init__(self,src_file):
        self.src_file = src_file

    def file_write(self, tagetfile, text):
        f = open(tagetfile, 'a+')
        f.write(text)
        f.write("\n")
        f.close()

    def mk_md_title(self, md_title):
        self.file_write(self.src_file, md_title)

    def joinstar(self, item):
        item = '*%s*' % item
        return item

    def joinvertical(self, item):
        item = '%s | ' % item
        return item

    def mk_md_item(self, itemlist):
        itemlist = map(self.joinstar, itemlist)
        md_item_title = ' | '.join(itemlist)
        md_item_title = '*OS* | ' + md_item_title
        self.file_write(self.src_file, md_item_title)
        table_line = '---------- |'
        for item in itemlist:
            table_line += ' ----------- |'
        self.file_write(self.src_file, table_line)

    def mk_md_data(self, comparelist):
        for compare_item, compare_datalist in comparelist.iteritems():
            compare_list = ' | '.join(compare_datalist)
            compare_list = '%s | ' % compare_item + compare_list
            self.file_write(self.src_file, compare_list)

    def mk_md_chart(self, chart_png_name):
        md_chart_png = "\n![](./svgfile/%s)\n" % chart_png_name
        self.file_write(self.src_file, md_chart_png)


class Create_md_Sysbenchcpu(Create_Md):
    # sysbenchcpu title 模板
    md_title_sysbenchcpu ="""
##sysbench - Performance Test of CPU
"""
    # sysbenchcpu 柱状图参数模板
    md_chart_sysbenchcpu = {
        'custom_font': 'goffer.ttf', 
        'title':  'CPU Execution Time(sec)',
        'osnames':[],
        'subjects':('1000', '2000', '3000'),
        'scores': [[10, 20, 30], [11, 21, 31]],
        'pngname': 'current-report/svgfile/syscpu0.png'}
    def __init__(self, src_file, result_data):
        Create_Md.__init__(self, src_file)
        self.result_data = result_data
               
    def check_key_args(self):
        self.oslist = self.result_data["oslist"]
        if len(self.oslist) > 1:
            init_thread = self.result_data[self.oslist[0]]["sysbenchcpu"]["threads"] 
            for osname in self.oslist[1:]:
                if self.result_data[osname]["sysbenchcpu"]["threads"] == init_thread:
                    self.resulttype = "MULT"
                else:
                    self.resulttype = "SIGNLE"
                    break
        else:
            self.resulttype = "SIGNLE"

    def key_compare(self, key):
        compare_flag = ""
        init_key = self.result_data[self.oslist[0]]["sysbenchcpu"][key]
        for osname in self.oslist[1:]:
            if self.result_data[osname]["sysbenchcpu"][key] == init_key:
                compare_flag = "T"
            else:
                compare_flag = "F"
                break
        return compare_flag

    def check_key_args(self):
        self.oslist = self.result_data["oslist"]
        key_list = ["threads", "cpu_args"]
        self.resulttype = "MULT"
        if len(self.oslist) > 1:
            for key in key_list:
                compare_flag = self.key_compare(key)
                if compare_flag == "F":
                    self.resulttype = "SIGNLE"
                    break
        else:
            self.resulttype = "SIGNLE"
    
    def mkmd_data_single(self, osname):
        data_sysbenchcpu_list = []
        data_sysbenchcpu = {}
        for arg in self.result_data[osname]["sysbenchcpu"]["cpu_args"]:
            data_sysbenchcpu_list.append(self.result_data[osname]["sysbenchcpu"][arg])
        data_sysbenchcpu[osname] = data_sysbenchcpu_list
        return data_sysbenchcpu

    def mkmd_data_mult(self):
        data_sysbenchcpu = {}
        for osname in self.oslist:
            data_sysbenchcpu_list = []
            for arg in self.result_data[osname]["sysbenchcpu"]["cpu_args"]:
                data_sysbenchcpu_list.append(self.result_data[osname]["sysbenchcpu"][arg])
            data_sysbenchcpu[osname] = data_sysbenchcpu_list
        return data_sysbenchcpu

    def mkmd_mkchart_single(self, osname, data_sysbenchcpu):
        osnames = []
        osnames.append(osname)
        self.md_chart_sysbenchcpu["osnames"] = osnames
        self.md_chart_sysbenchcpu["subjects"] = self.result_data[osname]["sysbenchcpu"]["cpu_args"]
        scores = map(float,data_sysbenchcpu[osname])
        self.md_chart_sysbenchcpu["scores"] = [scores]
        pngname = osname + '_' + "syscpu.png"
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_sysbenchcpu["pngname"] = pngpath
        mkchart(self.md_chart_sysbenchcpu)
      #  mkchart(self.md_chart_sysbenchcpu)
        return pngname

    def mkmd_mkchart_mult(self, data_sysbenchcpu):
        scores = []
        for osname in self.oslist:
            score = map(float, data_sysbenchcpu[osname])
            scores.append(score)
        self.md_chart_sysbenchcpu["osnames"] = self.oslist
        self.md_chart_sysbenchcpu["subjects"] = self.result_data[self.oslist\
                                                [0]]["sysbenchcpu"]["cpu_args"]
        self.md_chart_sysbenchcpu["scores"] = scores
        pngname = "sysbenchcpu.png"
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_sysbenchcpu["pngname"] = pngpath
        mkchart(self.md_chart_sysbenchcpu)
        return pngname

    def mkmd_single(self):
        self.mk_md_title(self.md_title_sysbenchcpu)
        for osname in self.oslist:
            subtitle = "###CPU Execution time(second) - %sthread\n" % self.result_data[osname]["sysbenchcpu"]["threads"]
            self.mk_md_title(subtitle)
            self.mk_md_item(self.result_data[osname]["sysbenchcpu"]["cpu_args"])
            data_sysbenchcpu = self.mkmd_data_single(osname)
            self.mk_md_data(data_sysbenchcpu)
            pngname = self.mkmd_mkchart_single(osname, data_sysbenchcpu)
            self.mk_md_chart(pngname)
    
    def mkmd_mult(self):
        self.mk_md_title(self.md_title_sysbenchcpu)
        subtitle = "###CPU Execution time(second) - %sthread\n" % \
            self.result_data[self.oslist[0]]["sysbenchcpu"]["threads"]
        self.mk_md_title(subtitle)
        self.mk_md_item(self.result_data[self.oslist[0]]["sysbenchcpu"]\
                        ["cpu_args"])
        data_sysbenchcpu = self.mkmd_data_mult()
        self.mk_md_data(data_sysbenchcpu)
        pngname = self.mkmd_mkchart_mult(data_sysbenchcpu)
        self.mk_md_chart(pngname)
            
    def create_md(self):
        self.check_key_args()
        if self.resulttype == "SIGNLE":
            self.mkmd_single()
        else:
            self.mkmd_mult()

class Create_md_Sysbenchmem(Create_Md): 
    # sysbenchmem title 模板
    md_title_sysbenchmem ="""
##sysbench - Performance Test of MEM
"""
    md_subtitle_sysbenchmem_ops = "###MEM Operations Performed"
    md_subtitle_sysbenchmem_rate =  "###MEM Transfer Rate"
    md_subtitle_sysbenchmem = {"ops": md_subtitle_sysbenchmem_ops,
                               "rate": md_subtitle_sysbenchmem_rate}
    # sysbenchmem 柱状图参数模板
    md_chart_sysbenchmem_ops = {
        'custom_font': 'goffer.ttf',
        'title':  'Mem Operations Performed(ops/sec)',
        'osnames':[],
        'subjects':['4threads'],
        'scores': [[10,20],],
        'pngname': 'current-report/svgfile/sysmem0.png'}
    md_chart_sysbenchmem_rate = {
        'custom_font': 'goffer.ttf',
        'title': 'Mem Transfer Rate(MB/s)',
        'osnames': [],
        'subjects':['4threads'],
        'scores': [[10,20]],
        'pngname': 'current-report/svgfile/sysmem1.png'} 
    md_chart_sysbenchmem = {"ops": md_chart_sysbenchmem_ops,
                            "rate": md_chart_sysbenchmem_rate}

    def __init__(self, src_file, result_data):
        Create_Md.__init__(self, src_file)
        self.result_data = result_data

    def check_key_args(self):
        self.oslist = self.result_data["oslist"]
        if len(self.oslist) > 1:
            init_thread = self.result_data[self.oslist[0]]["sysbenchmem"]["threads"]
            for osname in self.oslist[1:]:
                if self.result_data[osname]["sysbenchmem"]["threads"] == init_thread:
                    self.resulttype = "MULT"
                else:
                    self.resulttype = "SIGNLE"
                    break
        else:
            self.resulttype = "SIGNLE"

    def mkmd_data_single(self, osname, item):
        data_sysbenchmem = {}
        data_sysbenchmem[osname] = self.result_data[osname]["sysbenchmem"][item]
        return data_sysbenchmem

    def mkmd_data_mult(self, item):
        data_sysbenchmem = {}
        for osname in self.oslist:
            data_sysbenchmem[osname] = self.result_data[osname]["sysbenchmem"]\
                                       [item]
        return data_sysbenchmem
 
    def mkmd_mkchart_single(self, osname, data_sysbenchmem,
                            subjects, subitem):
        osnames = []
        osnames.append(osname)
        self.md_chart_sysbenchmem[subitem]["osnames"] = osnames
        self.md_chart_sysbenchmem[subitem]["subjects"] = subjects
        scores = map(float,data_sysbenchmem[osname])
        self.md_chart_sysbenchmem[subitem]["scores"] = [scores]
        pngname = "sysbenchmem"+ '_'+ subitem + ".png"
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_sysbenchmem[subitem]["pngname"] = pngpath
        mkchart(self.md_chart_sysbenchmem[subitem])
        return pngname

    def mkmd_mkchart_mult(self, data_sysbenchmem, subjects, subitem):
        scores = []
        for osname in self.oslist:
            score = data_sysbenchmem[osname]
            score = map(float, score)
            scores.append(score)
        self.md_chart_sysbenchmem[subitem]["osnames"] = self.oslist
        self.md_chart_sysbenchmem[subitem]["subjects"] = subjects
        self.md_chart_sysbenchmem[subitem]["scores"] = scores
        pngname = "sysbenchmem" + "_" + subitem + ".png"
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_sysbenchmem[subitem]["pngname"] = pngpath
        mkchart(self.md_chart_sysbenchmem[subitem])
        return pngname
 
    def mkmd_item(self, osname):
        threads = self.result_data[osname]["sysbenchmem"]["threads"].split(",")
        md_item = []
        for thread in threads:
            md_item.append("%sthreads" % thread)
        return md_item

    def mkmd_single(self):
        self.mk_md_title(self.md_title_sysbenchmem)
        for osname in self.oslist:
            for key, value in self.md_subtitle_sysbenchmem.iteritems():
                self.mk_md_title(value)
                md_item = self.mkmd_item(osname)
                self.mk_md_item(md_item)
                data_sysbenchmem = self.mkmd_data_single(osname, key)
                self.mk_md_data(data_sysbenchmem)
                pngname = self.mkmd_mkchart_single(osname, data_sysbenchmem, md_item, key)
                self.mk_md_chart(pngname)

    def mkmd_mult(self):
        self.mk_md_title(self.md_title_sysbenchmem)
        for key, value in self.md_subtitle_sysbenchmem.iteritems():
            self.mk_md_title(value)
            md_item = self.mkmd_item(self.oslist[0])
            self.mk_md_item(md_item)
            data_sysbenchmem = self.mkmd_data_mult(key)
            self.mk_md_data(data_sysbenchmem)
            pngname = self.mkmd_mkchart_mult(data_sysbenchmem, md_item, key)
            self.mk_md_chart(pngname)

    def create_md(self):
        self.check_key_args()
        if self.resulttype == "SIGNLE":
            self.mkmd_single()
        else:
            self.mkmd_mult()


class Create_md_Lmbench(Create_Md):
    # lmbench title 模板
    md_title_lmbench ="""
##Lmbench - Performance Test of Kernel"""
    md_subtitle_lmbench_pro = "###Processor - Times in miscroseconds - smaller is better"
    md_subtitle_lmbench_con = "###Context Switching - Times in microseconds - smaller is better"
    md_subtitle_lmbench_loc = "###Local Communication Latencies in microseconds - smaller is better"
    md_subtitle_lmbench_file = "###File & Vm System Latencies in microseconds - samaller is better"
    md_subtitle_lmbench_ban = "###Local Communication Bandwidths in MB/s - bigger is better"
    md_subtitle_lmbench = {"Processor": md_subtitle_lmbench_pro,
                           "Context": md_subtitle_lmbench_con,
                           "Local_latencies": md_subtitle_lmbench_loc,
                           "File" : md_subtitle_lmbench_file,
                           "Local_bandwidths" : md_subtitle_lmbench_ban
                            }    
    # lmbench 柱状图参数模板
    md_chart_lmbench_pro = {
        'custom_font': 'goffer.ttf',
        'title':  'Processor(usec)',
        'osnames':[],
        'subjects':['null\ncall', 'null\nI/O', "Slot\nTCP",\
            "sig\ninst", "sig\nhndl", "fork\nproc", "exec\nproc", "sh\nproc"],
        'scores': [[10,20],],
        'pngname': 'current-report/svgfile/lmbench.png'}
    md_chart_lmbench_con = {
        'custom_font': 'goffer.ttf',
        'title': 'Context Swithcing(usec)',
        'osnames': [],
        'subjects':['2p/0k', '2p/16k', '2p/64k', '8p/16k', '8p/64k', '16p/16k',\
            '16p/64k'],
        'scores': [[10,20]],
        'pngname': 'current-report/svgfile/lmbench.png'}
    md_chart_lmbench_loc = {
        'custom_font': 'goffer.ttf',
        'title': 'Local Communication latencies(usec)',
        'osnames': [],
        'subjects':['2p/0k\nctxsw', 'Pipe', 'AF\nUNIX', 'UDP', 'TCP', 'TCP\nconn'],
        'scores': [[10,20]],
        'pngname': 'current-report/svgfile/lmbench.png'}
    md_chart_lmbench_file = {
        'custom_font': 'goffer.ttf',
        'title': 'File & VM system latencies(usec)',
        'osnames': [],
        'subjects':['0K\nCreate', '0K\nDelete', '10K\nCreate', '10K\nDelete',\
             'Mmap\nLatency(K)', 'Prot\nFault', 'Page\nFault', '100fd\nselect'],
        'scores': [[10,20]],
        'pngname': 'current-report/svgfile/lmbench.png'}
    md_chart_lmbench_ban = {
        'custom_font': 'goffer.ttf',
        'title': 'Local Communication bandwidths(MB/s)',
        'osnames': [],
        'subjects':['Pipe', 'AF\nUNIX', 'TCP', 'File\nreread', 'Mmap\nreread',\
            'Bcopy\n(libc)', 'Bcopy\n(hand)', 'Mem\nread', 'Mem\nwrite'],
        'scores': [[10,20]],
        'pngname': 'current-report/svgfile/lmbench.png'}
    md_chart_lmbench = {"Processor": md_chart_lmbench_pro,
                        "Context": md_chart_lmbench_con,
                        "Local_latencies": md_chart_lmbench_loc,
                        "File" : md_chart_lmbench_file,
                        "Local_bandwidths" : md_chart_lmbench_ban}

    def __init__(self, src_file, result_data):
        Create_Md.__init__(self, src_file)
        self.result_data = result_data

    def mkmd_mkchart(self, data_lmbench, subitem):
        self.md_chart_lmbench[subitem]["osnames"] = self.oslist
        scores = []
        for osname in self.oslist:
            score = map(float,data_lmbench[osname])
            scores.append(score)
        self.md_chart_lmbench[subitem]["scores"] = scores
        pngname = "lmbench"+ '_'+ subitem + ".png"
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_lmbench[subitem]["pngname"] = pngpath
        mkchart(self.md_chart_lmbench[subitem])
        return pngname

    def mkmd_data(self, subitem):
        data_lmbench = {}
        for osname in self.oslist:
            data_lmbench_tmp = self.result_data[osname]["lmbench"][subitem]
            data_lmbench_tmp = map(str, data_lmbench_tmp)
            data_lmbench[osname] = data_lmbench_tmp
        return data_lmbench

    def mkmd_subjects(self, key):
        md_item = self.md_chart_lmbench[key]["subjects"]
        def rmn(test):
            return test.strip("\n")
        md_item = map(rmn,md_item)
        return md_item

    def mkmd_lmbench(self):
        self.mk_md_title(self.md_title_lmbench)
        for osname in self.oslist:
            for key, value in self.md_subtitle_lmbench.iteritems():
                self.mk_md_title(value)
                md_item = self.mkmd_subjects(key)
                self.mk_md_item(md_item)
                data_lmbench = self.mkmd_data(osname, key)
                self.mk_md_data(data_lmbench)
                pngname = self.mkmd_mkchart(osname, data_lmbench, key)
                self.mk_md_chart(pngname)

    def mkmd_lmbench_mult(self):
        self.mk_md_title(self.md_title_lmbench)
        for key, value in self.md_subtitle_lmbench.iteritems():
            self.mk_md_title(value)
            md_item = self.mkmd_subjects(key)
            self.mk_md_item(md_item)
            data_lmbench = self.mkmd_data(key)
            self.mk_md_data(data_lmbench)
            pngname = self.mkmd_mkchart(data_lmbench, key)
            self.mk_md_chart(pngname)

    def create_md(self):
        self.oslist = self.result_data["oslist"]
        self.mkmd_lmbench_mult()


class Create_md_Iozone(Create_Md):
    # iozone title 模板
    md_title_iozone ="""
##Iozone - Performance Test of I/O
"""
    md_subtitle_iozone ="###Variety of File Operations"
    # iozone 柱状图参数模板
    md_chart_iozone = {
        'custom_font': 'goffer.ttf',
        'title':  'Variety of file operations(KB/sec)',
        'osnames':[],
        'subjects':['Write', 'Rewrite', 'Read', 'Reread', 'Rondom read', 'Rondom write'],
        'scores': [[10, 20, 30], [11, 21, 31]],
        'pngname': 'current-report/svgfile/iozone.png'}

    def __init__(self, src_file, result_data):
        Create_Md.__init__(self, src_file)
        self.result_data = result_data

    def key_compare(self, key):
        compare_flag = ""
        init_key = self.result_data[self.oslist[0]]["iozone"][key]
        for osname in self.oslist[1:]:
            if self.result_data[osname]["iozone"][key] == init_key:
                compare_flag = "T"
            else:
                compare_flag = "F"
                break
        return compare_flag

    def check_key_args(self):
        self.oslist = self.result_data["oslist"]
        key_list = ["threads", "filesize", "rblock"]
        self.resulttype = "MULT"
        if len(self.oslist) > 1:
            for key in key_list:
                compare_flag = self.key_compare(key)
                if compare_flag == "F":
                    self.resulttype = "SIGNLE"
                    break
        else:
            self.resulttype = "SIGNLE"

    def mkmd_data_single(self, osname):
        data_iozone_list = []
        itemlist = self.result_data[osname]["iozone"]["modelist"]
        data_iozone = {}
        for i in itemlist:
            data_iozone_list.extend(self.result_data[osname]["iozone"][i])
        data_iozone[osname] = data_iozone_list
        return data_iozone

    def mkmd_data_mult(self):
        data_iozone = {}
        for osname in self.oslist:
            data_iozone_list = []
            itemlist = self.result_data[osname]["iozone"]["modelist"]
            for i in itemlist:
                data_iozone_list.extend(self.result_data[osname]["iozone"][i])
            data_iozone[osname] = data_iozone_list
        return data_iozone

    def mkmd_item(self, osname):
        iozone_itemlist = {"0":["Write", "Rewrite"], "1":["Read", "Reread"],
                       "2":["Rondom read", "Rondom write"]}
        itemlist = self.result_data[osname]["iozone"]["modelist"]
        iozone_item=[]
        for i in itemlist:
            iozone_item.extend(iozone_itemlist[i])
        return iozone_item

    def mkmd_mkchart_single(self, osname, data_iozone, subjects):
        osnames = []
        osnames.append(osname)
        self.md_chart_iozone["osnames"] = osnames
        self.md_chart_iozone["subjects"] = subjects
        scores = map(float,data_iozone[osname])
        self.md_chart_iozone["scores"] = [scores]
        pngname = osname + '_' + "iozone.png"
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_iozone["pngname"] = pngpath
        mkchart(self.md_chart_iozone)
        return pngname

    def mkmd_mkchart_mult(self, data_iozone, subjects):
        scores = []
        for osname in self.oslist:
            score = data_iozone[osname]
            score = map(float, score)
            scores.append(score)
        self.md_chart_iozone["osnames"] = self.oslist
        self.md_chart_iozone["subjects"] = subjects
        self.md_chart_iozone["scores"] = scores
        pngname = "iozone.png"
        pngpath = "current-report/svgfile/%s" % pngname
        self.md_chart_iozone["pngname"] = pngpath
        mkchart(self.md_chart_iozone)
        return pngname

    def mkmd_single(self):
        self.mk_md_title(self.md_title_iozone)
        for osname in self.oslist:
            self.mk_md_title(self.md_subtitle_iozone)
            iozone_item = self.mkmd_item(osname)
            self.mk_md_item(iozone_item)
            data_iozone = self.mkmd_data_single(osname)
            self.mk_md_data(data_iozone)
            pngname = self.mkmd_mkchart_single(osname, data_iozone, iozone_item)
            self.mk_md_chart(pngname)

    def mkmd_mult(self):
        self.mk_md_title(self.md_title_iozone)
        self.mk_md_title(self.md_subtitle_iozone)
        iozone_item = self.mkmd_item(self.oslist[0])
        self.mk_md_item(iozone_item)
        data_iozone = self.mkmd_data_mult()
        self.mk_md_data(data_iozone)
        pngname = self.mkmd_mkchart_mult(data_iozone, iozone_item)
        self.mk_md_chart(pngname)
 

    def create_md(self):
        self.check_key_args()
        if self.resulttype == "SIGNLE":
            self.mkmd_single()
        else:
            self.mkmd_mult()


class Create_md_Stream(Create_Md):
    # Stream title 模板
    md_title_stream ="""
##Stream - Performance Test of Memory"""
    md_subtitle_stream = "Threads Test(MB/s) - More is better"
    # stream 柱状图参数模板
    md_chart_stream = {
        'custom_font': 'goffer.ttf',
        'title':  '1Threads Test(MB/s)',
        'osnames':[],
        'subjects':['Copy', 'Scare', 'Add', 'Triad'],
        'scores': [[10,20],],
        'pngname': 'current-report/svgfile/stream.png'}

    def __init__(self, src_file, result_data):
        Create_Md.__init__(self, src_file)
        self.result_data = result_data

    def mkmd_mkchart_single(self, osname, data_stream, subitem):
        osnames = []
        osnames.append(osname)
        self.md_chart_stream["osnames"] = osnames
        self.md_chart_stream["title"] = "%sThreads Test(MB/s)" % subitem
        scores = map(float,data_stream[osname])
        self.md_chart_stream["scores"] = [scores]
        pngname = "stream"+ '_'+ subitem + ".png"
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_stream["pngname"] = pngpath
        mkchart(self.md_chart_stream)
        return pngname

    def mkmd_mkchart_mult(self, data_stream, subitem):
        scores = []
        for osname in self.oslist:
            score = map(float,data_stream[osname])
            scores.append(score)
        self.md_chart_stream["osnames"] = self.oslist
        self.md_chart_stream["title"] = "%sThreads Test(MB/s" % subitem
        self.md_chart_stream["scores"] = scores
        pngname = "stream" + "_" + subitem + ".png"
        pngpath = "current-report/svgfile/%s" % pngname
        self.md_chart_stream["pngname"] = pngpath
        mkchart(self.md_chart_stream)
        return pngname

    def mkmd_data_single(self, osname, subitem):
        data_stream = {}
        data_stream_tmp = self.result_data[osname]["stream"][subitem]
        data_stream_tmp = map(str, data_stream_tmp)
        data_stream[osname] = data_stream_tmp
        return data_stream
 
    def mkmd_data_mult(self, subitem):
        data_stream = {}
        for osname in self.oslist:
            data_stream_tmp = self.result_data[osname]["stream"][subitem]
            data_stream_tmp = map(str, data_stream_tmp)
            data_stream[osname] = data_stream_tmp
        return data_stream

    def mkmd_subtitle(self, osname):
        stream_subtitle_list = {}
        md_item = self.result_data[osname]["stream"]["threads"]
        for i in md_item:
            stream_subtitle ="###%s" %i + self.md_subtitle_stream
            stream_subtitle_list[i] = stream_subtitle
        return stream_subtitle_list

    def mkmd_single(self):
        self.mk_md_title(self.md_title_stream)
        for osname in self.oslist:
            md_subtitle = self.mkmd_subtitle(osname)
            for key, value in md_subtitle.iteritems():
                self.mk_md_title(value)
                md_item = self.result_data[osname]["stream"]["stream_args"]
                self.mk_md_item(md_item)
                data_stream = self.mkmd_data_single(osname, key)
                self.mk_md_data(data_stream)
                pngname = self.mkmd_mkchart_single(osname, data_stream, key)
                self.mk_md_chart(pngname)

    def check_key_args(self):
        self.oslist = self.result_data["oslist"]
        if len(self.oslist) > 1:
            init_thread = self.result_data[self.oslist[0]]["stream"]["threads"]
            for osname in self.oslist[1:]:
                if self.result_data[osname]["stream"]["threads"] == init_thread:
                    self.resulttype = "MULT"
                else:
                    self.resulttype = "SIGNLE"
                    break
        else:
            self.resulttype = "SIGNLE"

    def mkmd_mult(self):
        self.mk_md_title(self.md_title_stream)
        md_subtitle = self.mkmd_subtitle(self.oslist[0])
        for key, value in md_subtitle.iteritems():
            self.mk_md_title(value)
            md_item = self.result_data[self.oslist[0]]["stream"]\
                      ["stream_args"]
            self.mk_md_item(md_item)
            data_stream = self.mkmd_data_mult(key)
            self.mk_md_data(data_stream)
            pngname = self.mkmd_mkchart_mult(data_stream, key)
            self.mk_md_chart(pngname)

    def create_md(self):
        self.check_key_args()
        if self.resulttype == "SIGNLE":
            self.mkmd_single()
        else:
            self.mkmd_mult()

class Create_md_Pingpong(Create_Md):
    # Pingpong title 模板
    md_title_pingpong ="""
##Pingpong - Performance Test of Thread
"""
    md_subtitle_pingpong_init = "###Threads initialised - times in\
        microseconds - smaller is better"
    md_subtitle_pingpong_com =  "###Games completed - times in\
        microseconds - smaller is better"
    md_subtitle_pingpong = {"thread": md_subtitle_pingpong_init,
                               "games": md_subtitle_pingpong_com}
    # pingpong 柱状图参数模板
    md_chart_pingpong_init = {
        'custom_font': 'goffer.ttf',
        'title':  'Threads initialised(usec)',
        'osnames':[],
        'subjects':['4threads'],
        'scores': [[10,20],],
        'pngname': 'current-report/svgfile/pingpong0.png'}
    md_chart_pingpong_com = {
        'custom_font': 'goffer.ttf',
        'title': 'Games completed(usec)',
        'osnames': [],
        'subjects':['4threads'],
        'scores': [[10,20]],
        'pngname': 'current-report/svgfile/pingpong1.png'}
    md_chart_pingpong = {"thread": md_chart_pingpong_init,
                         "games": md_chart_pingpong_com}

    def __init__(self, src_file, result_data):
        Create_Md.__init__(self, src_file)
        self.result_data = result_data

    def check_key_args(self):
        self.oslist = self.result_data["oslist"]
        if len(self.oslist) > 1:
            init_thread = self.result_data[self.oslist[0]]["pingpong"]["tables"]
            for osname in self.oslist[1:]:
                if self.result_data[osname]["pingpong"]["tables"] == init_thread:
                    self.resulttype = "MULT"
                else:
                    self.resulttype = "SIGNLE"
                    break
        else:
            self.resulttype = "SIGNLE"

    def mkmd_data_single(self, osname, item):
        data_pingpong = {}
        data_pingpong[osname] = self.result_data[osname]["pingpong"][item]
        return data_pingpong

    def mkmd_data_mult(self, item):
        data_pingpong = {}
        for osname in self.oslist:
            data_pingpong[osname] = self.result_data[osname]["pingpong"][item]
        return data_pingpong

    def mkmd_mkchart_single(self, osname, data_pingpong, subjects, subitem):
        osnames = []
        osnames.append(osname)
        self.md_chart_pingpong[subitem]["osnames"] = osnames
        self.md_chart_pingpong[subitem]["subjects"] = subjects
        scores = map(float,data_pingpong[osname])
        self.md_chart_pingpong[subitem]["scores"] = [scores]
        pngname = "pingpong"+ '_'+ subitem + ".png"
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_pingpong[subitem]["pngname"] = pngpath
        mkchart(self.md_chart_pingpong[subitem])
        return pngname

    def mkmd_mkchart_mult(self, data_pingpong, subjects, subitem):
        scores = []
        for osname in self.oslist:
            score = data_pingpong[osname]
            score = map(float, data_pingpong[osname])
            scores.append(score)
        self.md_chart_pingpong[subitem]["osnames"] = self.oslist
        self.md_chart_pingpong[subitem]["subjects"] = subjects
        self.md_chart_pingpong[subitem]["scores"] = scores
        pngname = "pingpong" + "_" + subitem + ".png"
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_pingpong[subitem]["pngname"] = pngpath
        mkchart(self.md_chart_pingpong[subitem])
        return pngname

    def mkmd_item(self, osname):
        tables = self.result_data[osname]["pingpong"]["tables"]
        md_item = []
        for table in tables:
            md_item.append("%stables" % table)
        return md_item

    def mkmd_single(self):
        self.mk_md_title(self.md_title_pingpong)
        for osname in self.oslist:
            for key, value in self.md_subtitle_pingpong.iteritems():
                self.mk_md_title(value)
                md_item = self.mkmd_item(osname)
                self.mk_md_item(md_item)
                data_pingpong = self.mkmd_data_single(osname, key)
                self.mk_md_data(data_pingpong)
                pngname = self.mkmd_mkchart_single(osname, data_pingpong, md_item, key)
                self.mk_md_chart(pngname)

    def mkmd_mult(self):
        self.mk_md_title(self.md_title_pingpong)
        for key, value in self.md_subtitle_pingpong.iteritems():
           self.mk_md_title(value)
           md_item = self.mkmd_item(self.oslist[0])
           self.mk_md_item(md_item)
           data_pingpong = self.mkmd_data_mult(key)
           self.mk_md_data(data_pingpong)
           pngname = self.mkmd_mkchart_mult(data_pingpong, md_item, key)
           self.mk_md_chart(pngname)
           
    def create_md(self):
        self.check_key_args()
        if self.resulttype == "SIGNLE":
            self.mkmd_single()
        else:
            self.mkmd_mult()


class Create_md_Unixbench(Create_Md):
    # unixbench title 模板
    md_title_unixbench ="""
##Unixbench - Performance Test of System
"""
    md_subtitle_unixbench = "###System Index"
    # unixbench 柱状图参数模板
    md_chart_unixbench = {
        'custom_font': 'goffer.ttf',
        'title':  'System Index',
        'osnames':[],
        'subjects':('1threads'),
        'scores': [[10, 20, 30], [11, 21, 31]],
        'pngname': 'current-report/svgfile/unixbench.png'}

    def __init__(self, src_file, result_data):
        Create_Md.__init__(self, src_file)
        self.result_data = result_data

    def check_key_args(self):
        self.oslist = self.result_data["oslist"]
        if len(self.oslist) > 1:
            init_thread = self.result_data[self.oslist[0]]["unixbench"]["threads"]
            for osname in self.oslist[1:]:
                if self.result_data[osname]["unixbench"]["threads"] == init_thread:
                    self.resulttype = "MULT"
                else:
                    self.resulttype = "SIGNLE"
                    break
        else:
            self.resulttype = "SIGNLE"

    def mkmd_data_single(self, osname):
        data_unixbench_list = []
        data_unixbench = {}
        for thread in self.result_data[osname]["unixbench"]["threads"]:
            data_unixbench_list.append(self.result_data[osname]["unixbench"][thread])
        data_unixbench[osname] = data_unixbench_list
        return data_unixbench

    def mkmd_data_mult(self):
        data_unixbench_list = []
        data_unixbench = {}
        for osname in self.oslist:
            for thread in self.result_data[osname]["unixbench"]["threads"]:
                data_unixbench_list.append(self.result_data[osname]\
                    ["unixbench"][thread])
            data_unixbench[osname] = data_unixbench_list
        return data_unixbench

    def mkmd_item(self, osname):
        unixbench_item = []
        threads = self.result_data[osname]["unixbench"]["threads"]
        for thread in threads:
            unixbench_item.append("%sthreads" % thread)
        return unixbench_item

    def mkmd_mkchart_single(self, osname, data_unixbench, subitem):
        osnames = []
        osnames.append(osname)
        self.md_chart_unixbench["osnames"] = osnames
        self.md_chart_unixbench["subjects"] = subitem
        scores = map(float,data_unixbench[osname])
        self.md_chart_unixbench["scores"] = [scores]
        pngname = osname + '_' + "unxibench.png"
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_unixbench["pngname"] = pngpath
        mkchart(self.md_chart_unixbench)
        return pngname

    def mkmd_mkchart_mult(self, data_unixbench, subitem):
        scores = []
        for osname in self.oslist:
            score = data_unixbench[osname]
            score = map(float, score)
            scores.append(score)
        self.md_chart_unixbench["osnames"] = self.oslist
        self.md_chart_unixbench["subjects"] = subitem
        self.md_chart_unixbench["scores"] = scores
        pngname = "unixbench.png"
        pngpath = 'current-report/svgfile/%s' % pngname
        mkchart(self.md_chart_unixbench)
        return pngname

    def mkmd_single(self):
        self.mk_md_title(self.md_title_unixbench)
        for osname in self.oslist:
            self.mk_md_title(self.md_subtitle_unixbench)
            unixbench_item = self.mkmd_item(osname)
            self.mk_md_item(unixbench_item)
            data_unixbench = self.mkmd_data_single(osname)
            self.mk_md_data(data_unixbench)
            pngname = self.mkmd_mkchart_single(osname, data_unixbench, unixbench_item)
            self.mk_md_chart(pngname)

    def mkmd_mult(self):
        self.mk_md_title(self.md_title_unixbench)
        self.mk_md_title(self.md_subtitle_unixbench)
        unixbench_item = self.mkmd_item(self.oslist[0])
        self.mk_md_item(unixbench_item)
        data_unixbench = self.mkmd_data_mult()
        self.mk_md_data(data_unixbench)
        pngname = self.mkmd_mkchart_mult(data_unixbench, unixbench_item)
        self.mk_md_chart(pngname)

    def create_md(self):
        self.check_key_args()
        if self.resulttype == "SIGNLE":
            self.mkmd_single()
        else:
            self.mkmd_mult()


class Create_md_Browser(Create_Md):
    #  title 模板
    md_title_browser ="""
##Css - Performance Test of Browser
"""
    md_subtitle_browser = "###Browser test - Css"
    # browser 柱状图参数模板
    md_chart_browser = {
        'custom_font': 'goffer.ttf',
        'title':  'Browser Css Test',
        'osnames':[],
        'subjects':('chrome', 'firefox'),
        'scores': [[10, 20, 30], [11, 21, 31]],
        'pngname': 'current-report/svgfile/css.png'}

    def __init__(self, src_file, result_data, testitem):
        Create_Md.__init__(self, src_file)
        self.result_data = result_data
        self.testitem = testitem

    def check_key_args(self):
        self.oslist = self.result_data["oslist"]
        if len(self.oslist) > 1:
            init_itemlist = self.result_data[self.oslist[0]][self.testitem]\
                                            ['browsetype']
            for osname in self.oslist[1:]:
                if self.result_data[osname][self.testitem]['browsetype'] == \
                    init_itemlist:
                    self.resulttype = "MULT"
                else:
                    self.resulttype = "SIGNLE"
                    break
        else:
            self.resulttype = "SIGNLE"

    def mkmd_data_single(self, osname, browseritem):
        data_browser = {}
        data_browser_list = []
        for item in browseritem:
            data_browser_list.append(self.result_data[osname][self.testitem][item])
        data_browser[osname] = data_browser_list
        return data_browser

    def mkmd_data_mult(self):
        data_browser_list = []
        data_browser = {}
        for osname in self.oslist:
            for item in self.result_data[osname][self.testitem]["browsetype"]:
                data_browser_list.append(self.result_data[osname]\
                    [self.testitem][item])
            data_browser[osname] = data_browser_list
        return data_browser

    def mkmd_mkchart_single(self, osname, data_browser, subitem):
        osnames = []
        osnames.append(osname)
        self.md_chart_browser["osnames"] = osnames
        self.md_chart_browser["subjects"] = subitem
        scores = map(float,data_browser[osname])
        self.md_chart_browser["scores"] = [scores]
        pngname = osname + '_' + "%s.png" % self.testitem
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_browser["pngname"] = pngpath
        mkchart(self.md_chart_browser)
        return pngname

        mkchart(self.md_chart_browser)
        return self.md_chart_browser['pngname']

    def mkmd_mkchart_mult(self, data_browser, subitem):
        scores = []
        for osname in self.oslist:
            score = data_browser[osname]
            score = map(float, score)
            scores.append(score)
        self.md_chart_browser["osnames"] = self.oslist
        self.md_chart_browser["subjects"] = subitem
        self.md_chart_browser["scores"] = scores
        pngname = self.testitem + '.png'
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_browser["pngname"] = pngpath
        mkchart(self.md_chart_browser)
        return pngname

    def mkmd_single(self):
        self.mk_md_title(self.md_title_browser)
        for osname in self.oslist:
            self.mk_md_title(self.md_subtitle_browser)
            browser_item = self.result_data[osname][self.testitem]['browsetype']
            self.mk_md_item(browser_item)
            data_browser = self.mkmd_data_single(osname, browser_item)
            self.mk_md_data(data_browser)
            pngname = self.mkmd_mkchart_single(osname, data_browser, browser_item)
            self.mk_md_chart(pngname)

    def mkmd_mult(self):
        self.mk_md_title(self.md_title_browser)
        self.mk_md_title(self.md_subtitle_browser)
        browser_item = self.result_data[self.oslist[0]][self.testitem]['browsetype']
        self.mk_md_item(browser_item)
        data_browser = self.mkmd_data_mult()
        self.mk_md_data(data_browser)
        pngname = self.mkmd_mkchart_mult(data_browser, browser_item)
        self.mk_md_chart(pngname)

    def create_md(self):
        self.check_key_args()
        if self.resulttype == "SIGNLE":
            self.mkmd_single()
        else:
            self.mkmd_mult()


class Create_md_Css(Create_md_Browser):
    #  title 模板
    md_title_browser ="""
##Css - Performance Test of Browser
"""
    md_subtitle_browser = "###Browser test - Css"
    # browser 柱状图参数模板
    md_chart_browser = {
        'custom_font': 'goffer.ttf',
        'title':  'Browser Css Test',
        'osnames':[],
        'subjects':('chrome', 'firefox'),
        'scores': [[10, 20, 30], [11, 21, 31]],
        'pngname': 'current-report/svgfile/css.png'}
    def __init__(self, src_file, result_data):
        Create_md_Browser.__init__(self, src_file, result_data, "css")


class Create_md_Html(Create_md_Browser):
    #  title 模板
    md_title_browser ="""
##Html - Performance Test of Browser
"""
    md_subtitle_browser = "###Browser test - Html"
    # browser 柱状图参数模板
    md_chart_browser = {
        'custom_font': 'goffer.ttf',
        'title':  'Browser Html Test',
        'osnames':[],
        'subjects':('chrome', 'firefox'),
        'scores': [[10, 20, 30], [11, 21, 31]],
        'pngname': 'current-report/svgfile/html.png'}
    def __init__(self, src_file, result_data):
        Create_md_Browser.__init__(self, src_file, result_data, "html")


class Create_md_Acid(Create_md_Browser):
    #  title 模板
    md_title_browser ="""
##Acid - Performance Test of Browser
"""
    md_subtitle_browser = "###Browser test - Acid"
    # browser 柱状图参数模板
    md_chart_browser = {
        'custom_font': 'goffer.ttf',
        'title':  'Browser Acid Test',
        'osnames':[],
        'subjects':('chrome', 'firefox'),
        'scores': [[10, 20, 30], [11, 21, 31]],
        'pngname': 'current-report/svgfile/acid.png'}
    def __init__(self, src_file, result_data):
        Create_md_Browser.__init__(self, src_file, result_data, "acid") 


class Create_md_V8(Create_md_Browser):
    #  title 模板
    md_title_browser ="""
##V8 - Performance Test of Browser
"""
    md_subtitle_browser = "###Browser test - V8"
    # browser 柱状图参数模板
    md_chart_browser = {
        'custom_font': 'goffer.ttf',
        'title':  'Browser V8 Test',
        'osnames':[],
        'subjects':('chrome', 'firefox'),
        'scores': [[10, 20, 30], [11, 21, 31]],
        'pngname': 'current-report/svgfile/v8.png'}
    def __init__(self, src_file, result_data):
        Create_md_Browser.__init__(self, src_file, result_data, "v8")      


class Create_md_Octane(Create_md_Browser):
    #  title 模板
    md_title_browser ="""
##Octane - Performance Test of Browser
"""
    md_subtitle_browser = "###Browser test - Octane"
    # browser 柱状图参数模板
    md_chart_browser = {
        'custom_font': 'goffer.ttf',
        'title':  'Browser Octane Test',
        'osnames':[],
        'subjects':('chrome', 'firefox'),
        'scores': [[10, 20, 30], [11, 21, 31]],
        'pngname': 'current-report/svgfile/octane.png'}
    def __init__(self, src_file, result_data):
        Create_md_Browser.__init__(self, src_file, result_data, "octane")


class Create_md_Dromaeo(Create_md_Browser):
    #  title 模板
    md_title_browser ="""
##Dromaeo - Performance Test of Browser
"""
    md_subtitle_browser = "###Browser test - Dromaeo"
    # browser 柱状图参数模板
    md_chart_browser = {
        'custom_font': 'goffer.ttf',
        'title':  'Browser Dromaeo Test',
        'osnames':[],
        'subjects':('chrome', 'firefox'),
        'scores': [[10, 20, 30], [11, 21, 31]],
        'pngname': 'current-report/svgfile/dromaeo.png'}
    def __init__(self, src_file, result_data):
        Create_md_Browser.__init__(self, src_file, result_data, "dromaeo")


# html_md处理列表
Md_classlist = {'sysbenchcpu': Create_md_Sysbenchcpu,
                'sysbenchmem': Create_md_Sysbenchmem,
                'lmbench': Create_md_Lmbench,
                'pingpong': Create_md_Pingpong,
                'stream': Create_md_Stream,
                'iozone': Create_md_Iozone,
                'unixbench': Create_md_Unixbench,
                'css': Create_md_Css,
                'html': Create_md_Html,
                'acid': Create_md_Acid,
                'v8': Create_md_V8,
                'octane': Create_md_Octane,
                'dromaeo': Create_md_Dromaeo}

def mk_html_main(src_file, oslist, itemlist):
    
    if os.path.isdir("current-report"):
        pass
    else:
        os.mkdir("current-report")
    if os.path.isdir("current-report/svgfile"):
        pass
    else:
        os.mkdir("current-report/svgfile")
    os_result_data = {}
    for osname in oslist:
        tmp_data = read_database(osname)
        os_result_data[osname] = tmp_data
    os_result_data["oslist"] = oslist
    for item in itemlist:
        Create_Md = Md_classlist[item]    
        result_md = Create_Md(src_file, os_result_data)
        result_md.create_md()
    shutil.copy("style.css", "current-report/style.css")
    try:
        retcode = call("pandoc --toc -c ./style.css -o current-report/test.html \
                       current-report/test.md", shell=True)
        if retcode < 0:
            print >> sys.stderr, "Child was terminated by signal", -retcode
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e      

# test 生成html报告
# mk_html_main("current-report/test.md", ["test", "test"], ["css", "html", "dromaeo", "acid", "v8", "octane"])
