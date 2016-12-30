import os
import sys
import shutil
from subprocess import call, PIPE, Popen
from mkchart import *
from temp_html import *


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

    def mk_pic_chart(self, pic_chart)
        mkcontrol(pic_chart)
 
    def mk_md_chart(self, chart_png_name):
        md_chart_png = "\n![](./svgfile/%s)" % chart_png_name
        self.file_write(self.src_file, md_chart_png)


class Create_md_Sysbenchcpu(Create_Md):
    def __init__(self, src_file):
        Create_Md.__init__(self, src_file)
        
       

"""
mk_picture_chart={'title': 'Variety of file operatios KB/sec', 'custom_font': '/usr/share/fonts/goffer.ttf', 'subjects': ('Write', 'Rewrite', 'Read', 'Reread', 'Rondom read', 'Rondom write'), 'osnames': ['Fedora_24', 'iSoft_Desktop_4.0'], 'scores': [[123362.94, 126166.84, 120646.95, 121933.63, 63139.51, 86510.43], [99066.85, 100225.93, 114350.42, 114411.4, 62679.6, 85086.96]], 'pngname': 'result_html/svgfile/iozone0.png'}
"""

# test
mdtitle = """
##sysbench - Performance Test of CPU

###CPU Execution time(second) - 1thread
"""
a = Create_Md("test.md")
a.mk_md_title(mdtitle)
a.mk_md_item(["10000","20000", "30000", "40000"])
comprelist = {"Fedora_24": ["9.94","24.92","42.09", "100"], "isoft_4.0": ["9.93", "25.61", "44.65", "100"]}
a.mk_md_data(comprelist)
a.mk_md_chart("sysbenchcpu.png")
