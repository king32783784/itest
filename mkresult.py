#coding=utf8

import os
import shutil
from common import *
from mkreport.mk_html import *
from mkreport.data_operation import *


# 制作当前报告
def mk_current_report():
   typelist = get_aftertest_typelist()
   testlist = get_aftertest_itemlist(typelist[0])
   mk_html_main("current-report/test.md", ["test"], testlist)

# 获取数据库中结果os列表
def get_result_oslist():
    oslist = read_database('OSLIST')
    return oslist

# 获取oslist中公共项目
def getos_common_items(mkoslist):
    mkos_less = mkoslist[0]
    itemlist_len = read_database(mkoslist[0])["testlist"]
    for mkos in mkoslist:
        itemlist = read_database(mkos)["testlist"]
        if len(itemlist) < itemlist_len:
            mkos_less = mkos
    tomakelist = []
    checktype = "TRUE"
    for item in read_database(mkos_less)["testlist"]:
        for mkos in mkoslist:
            if item in read_database(mkos)["testlist"]:
                pass
            else:
                checktype = "FLASE"
                break
        if checktype == "TRUE":
            tomakelist.append(item)
    return tomakelist


# 制作html定制报告
def mkhtml_custom_report(mkoslist, reportname):
    homepath = getlocatepath()
    tomakelist = getos_common_items(mkoslist)
    reportpath = os.path.join(homepath, "ReportRepository")
    reportname = str(reportname)
    reportpath = os.path.join(reportpath, reportname)
    mk_html_main("current-report/test.md", mkoslist, tomakelist)
    shutil.move("current-report", reportpath)
    report_url = "file://" + "%s" % reportpath + "/test.html"
    config = QSettings(".resultseting.ini", QSettings.IniFormat)
    config.beginGroup("totalresults")
    config.setValue(reportname, report_url)
    config.endGroup()
#mk_current_report()
