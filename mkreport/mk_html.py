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

    def mk_pic_chart(self, pic_chart):
        mkcontrol(pic_chart)
 
    def mk_md_chart(self, chart_png_name):
        md_chart_png = "\n![](./svgfile/%s)" % chart_png_name
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
    
    def mkmd_data(self, osname):
        data_sysbenchcpu_list = []
        data_sysbenchcpu = {}
        for arg in self.result_data[osname]["sysbenchcpu"]["cpu_args"]:
            data_sysbenchcpu_list.append(self.result_data[osname]["sysbenchcpu"][arg])
        data_sysbenchcpu[osname] = data_sysbenchcpu_list
        return data_sysbenchcpu

    def mkmd_mkchart(self, osname, data_sysbenchcpu):
        osnames = []
        osnames.append(osname)
        self.md_chart_sysbenchcpu["osnames"] = osnames
        self.md_chart_sysbenchcpu["subjects"] = self.result_data[osname]["sysbenchcpu"]["cpu_args"]
        scores = map(float,data_sysbenchcpu[osname])
        self.md_chart_sysbenchcpu["scores"] = [scores]
        pngname = osname + '_' + "syscpu.png"
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_sysbenchcpu["pngname"] = pngpath
        mkcontrol(self.md_chart_sysbenchcpu)
        return pngname

    def mkmd_single(self):
        for osname in self.oslist:
            self.mk_md_title(self.md_title_sysbenchcpu)
            subtitle = "###CPU Execution time(second) - %sthread\n" % self.result_data[osname]["sysbenchcpu"]["threads"]
            self.mk_md_title(subtitle)
            self.mk_md_item(self.result_data[osname]["sysbenchcpu"]["cpu_args"])
            data_sysbenchcpu = self.mkmd_data(osname)
            self.mk_md_data(data_sysbenchcpu)
            pngname = self.mkmd_mkchart(osname, data_sysbenchcpu)
            self.mk_md_chart(pngname)
    
    def mkmd_mult(self):
        pass
            
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

    def mkmd_data(self, osname, item):
        data_sysbenchmem = {}
        data_sysbenchmem[osname] = self.result_data[osname]["sysbenchmem"][item]
        return data_sysbenchmem

    def mkmd_mkchart_ops(self, osname, data_sysbenchmem, subjects):
        osnames = []
        osnames.append(osname)
        self.md_chart_sysbenchmem_ops["osnames"] = osnames
        self.md_chart_sysbenchmem_ops["subjects"] = subjects
        scores = map(float,data_sysbenchmem[osname])
        self.md_chart_sysbenchmem_ops["scores"] = [scores]
        pngname = osname + '_' + "sysmem1.png"
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_sysbenchmem_ops["pngname"] = pngpath
        mkcontrol(self.md_chart_sysbenchmem_ops)
        return pngname
 
    def mkmd_mkchart_rate(self, osname, data_sysbenchmem, subjects):
        osnames = []
        osnames.append(osname)
        self.md_chart_sysbenchmem_rate["osnames"] = osnames
        self.md_chart_sysbenchmem_rate["subjects"] = subjects
        scores = map(float,data_sysbenchmem[osname])
        self.md_chart_sysbenchmem_rate["scores"] = [scores]
        pngname = osname + '_' + "sysmem2.png"
        pngpath = 'current-report/svgfile/%s' % pngname
        self.md_chart_sysbenchmem_rate["pngname"] = pngpath
        mkcontrol(self.md_chart_sysbenchmem_ops)
        return pngname

    def mkmd_item(self, osname):
        threads = self.result_data[osname]["sysbenchmem"]["threads"].split(",")
        md_item = []
        for thread in threads:
            md_item.append("%sthreads" % thread)
        return md_item

    def mkmd_single(self):
        for osname in self.oslist:
            self.mk_md_title(self.md_title_sysbenchmem)
            self.mk_md_title(self.md_subtitle_sysbenchmem_ops)
            md_item = self.mkmd_item(osname)
            self.mk_md_item(md_item)
            data_sysbenchmem = self.mkmd_data(osname, "ops")
            self.mk_md_data(data_sysbenchmem)
            pngname = self.mkmd_mkchart(osname, data_sysbenchmem, md_item)
            self.mk_md_chart(pngname)

    def mkmd_mult(self):
        pass

    def create_md(self):
        self.check_key_args()
        if self.resulttype == "SIGNLE":
            self.mkmd_single()
        else:
            self.mkmd_mult()
  

def mk_html_main(src_file, oslist):
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
    print os_result_data
    os_result_data["oslist"] = oslist
    result_md = Create_md_Sysbenchmem(src_file, os_result_data)
    result_md.create_md()
    shutil.copy("style.css", "current-report/style.css")
    try:
        retcode = call("pandoc --toc -c ./style.css -o current-report/test.html \
                       current-report/test.md", shell=True)
        if retcode < 0:
            print >> sys.stderr, "Child was terminated by signal", -retcode
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e      

"""
mk_picture_chart={'title': 'Variety of file operatios KB/sec', 'custom_font': '/usr/share/fonts/goffer.ttf', 'subjects': ('Write', 'Rewrite', 'Read', 'Reread', 'Rondom read', 'Rondom write'), 'osnames': ['Fedora_24', 'iSoft_Desktop_4.0'], 'scores': [[123362.94, 126166.84, 120646.95, 121933.63, 63139.51, 86510.43], [99066.85, 100225.93, 114350.42, 114411.4, 62679.6, 85086.96]], 'pngname': 'result_html/svgfile/iozone0.png'}
"""

# test
mdtitle = """
##sysbench - Performance Test of CPU

###CPU Execution time(second) - 1thread
"""
"""
a = Create_Md("current-report/test.md")
a.mk_md_title(mdtitle)
a.mk_md_item(["10000","20000", "30000", "40000"])
comprelist = {"Fedora_24": ["9.94","24.92","42.09", "100"], "isoft_4.0": ["9.93", "25.61", "44.65", "100"]}
a.mk_md_data(comprelist)
a.mk_md_chart("sysbenchcpu.png")
"""
mk_html_main("current-report/test.md", ["local"])
