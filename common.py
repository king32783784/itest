# *-* coding=utf-8 *-*
import os
import time
import shutil
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui,QtCore

# 计算测试总数
def sumtests():
    totaltests = readtestlist()
    totalnum = 0
    for key, value in totaltests.iteritems():
        totalnum += len(value)
    return totalnum

# 获取某一测试类型的待测项目列表
def getestlist(testtype):
    testlist = []
    config = QSettings(".testseting.ini", QSettings.IniFormat)
    config.beginGroup(testtype)
    tmptestlist = config.allKeys()
    config.endGroup()
    for testitem in tmptestlist:
        testlist.append(str(testitem))
    return testlist

# 读取全部待测项目列表
def readtestlist():
    try:
        todotestlist = {}
        for testtype in ["info_testlists", "func_testlists",
                         "perf_testlists", "stress_testlists"]:
            if testtype == "info_testlists":
                infolist = getestlist(testtype)
                if len(infolist) > 0:
                    todotestlist["info"] = infolist
            elif testtype == "func_testlists":
                funclist = getestlist(testtype)
                if len(funclist) > 0:
                    todotestlist["function"] = funclist
            elif testtype == "perf_testlists":
                perflist = getestlist(testtype)
                if len(perflist) > 0:
                    todotestlist["performance"] = perflist
            else:
                strlist = getestlist(testtype)
                if len(strlist) > 0:
                    todotestlist["stress"] = strlist
        return todotestlist
    except:
        return 0

# 获取测试项目
def getitemlist(item):
    try:
        todotests = []
        config = QSettings(".testseting.ini", QSettings.IniFormat)
        itemtmp = item + "-user"
        config.beginGroup(itemtmp)
        itemlist = config.allKeys()
        for test in itemlist:
            status = checkstatus(itemtmp, test)
            if status == "E":
                todotests.append(str(test))
        return todotests
    except:
        return 0

# 获取测试报告列表
def getresultslist():
    try:
        resultslist = {}
        config = QSettings(".resultseting.ini", QSettings.IniFormat)
        config.beginGroup("totalresults")
        namelist = config.allKeys()
        config = QSettings(".resultseting.ini", QSettings.IniFormat)
        for name in namelist:
            resultslist[str(name)] = str(config.value(QString("totalresults/") + name).toString()[0:])
        return resultslist
    except:
        return None

# 检查item是否被选中 
def checkstatus(group, item):
    config = QSettings(".testseting.ini", QSettings.IniFormat)
    status = config.value(QString("%s/" % group) + item).toString()[0:]
    return status

# 获得测试项目的状态
def getitemargs(testtool):
    try:
        testargs = {}
        toollabel = testtool + "-user"
        config = QSettings(".testseting.ini", QSettings.IniFormat)
        config.beginGroup(toollabel)
        argslist = config.allKeys()
        config = QSettings(".testseting.ini", QSettings.IniFormat)
        for arg in argslist:
            testargs[str(arg)] = str(config.value(QString("%s/"% toollabel) + arg).toString()[0:])
        return testargs
    except:
        return 0

# 获取测试工具地址
def gettesttool():
    try:
        testtool = {}
        config = QSettings(".testseting.ini", QSettings.IniFormat)
        testtool["mode"] = config.value(QString("testtool-user/") + "settoolstatus").toString()[0:]
        if testtool["mode"] == "L":
            testtool["address"] = config.value(QString("testtool-user/") + "dir").toString()[0:]
        else:
            testtool["address"] = config.value(QString("testtool-user/") + "address").toString()[0:]
        return testtool
    except:
        print "testtool adress get faild"
        return 0 

# congig写入
def writeconfig(configname, begin, key, value):
    config = QSettings(configname, QSettings.IniFormat)
    config.beginGroup(begin)
    config.setValue(key, value)
    config.endGroup()
    
# 删除文件夹及文件夹全部内容
def delete_file_folder(src):
    '''delete files and folders'''
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc=os.path.join(src,item)
            delete_file_folder(itemsrc) 
        try:
            os.rmdir(src)
        except:
            pass

# 获取当前路径
def getlocatepath():
    return  os.getcwd()

# 获取当前时间
def getlocattime():
    FORMAT = '%Y%m%d%H%M%S'
    return time.strftime(FORMAT, time.localtime(time.time()))

# 创建结果和报告仓库
def createdatarepository():
    homepath = getlocatepath()
    datarepository = os.path.join(homepath, "DataRepository")
    reportrepository = os.path.join(homepath, "ReportRepository")
    if os.path.exists(datarepository):
        pass
    else:
        os.makedirs(datarepository)
    if os.path.exists(reportrepository):
        pass
    else:
        os.makedirs(reportrepository)

# 创建当前结果保存文件夹
def createresultdir():
    homepath = getlocatepath()
    locatime = getlocattime()
    RESULTTYPE = "isoft-test-"
    tmpresultdir = RESULTTYPE + locatime
    return tmpresultdir

# 获取每个测试项目的参数
def get_item_args(item):
    item_args = {}
    item_group = item + "-user"
    config = QSettings(".testseting.ini", QSettings.IniFormat)
    config.beginGroup(item_group)
    item_argslist = config.allKeys()
    config = QSettings(".testseting.ini", QSettings.IniFormat)
    for item_arg in item_argslist:
        item_args[str(item_arg)] = str(config.value(QString("%s/"% item_group) + item_arg).toString()[0:])
    return item_args
    
# 获取当前测试的全部测试项目和对应影响结果处理的参数；并写入.tempseting.ini
def save_testitem_args():
    todo_testlist = {}
    testlist = readtestlist()
    for key, value in testlist.iteritems():
        todo_itemlist = []
        for todo_item in value:
            dotestlist = getitemlist(todo_item)
            for item in dotestlist:
                todo_itemlist.append(item)
        todo_testlist[key] = todo_itemlist
    for key, value in todo_testlist.iteritems():
        writeconfig(".tempseting.ini", "todo_test_type", key, "") # 写入测试类别
        for todo_item in value:
            writeconfig(".tempseting.ini", key, todo_item, "") # 写入测试项目
            item_argslist = get_item_args(todo_item)
            for arg_key, arg_value in item_argslist.iteritems():
                writeconfig(".tempseting.ini", todo_item, arg_key, arg_value) # 写入测试项目对应参数

# 获取已完成测试的项目

def get_aftertest_itemlist(testtype):
    config = QSettings(".tempseting.ini", QSettings.IniFormat)
    config.beginGroup(testtype)
    tmptestlist = config.allKeys()
    config.endGroup()
    tmptestlist = map(str, tmptestlist)
    return tmptestlist

def get_aftertest_typelist():
    config = QSettings(".tempseting.ini", QSettings.IniFormat)
    config.beginGroup("todo_test_type")
    typelist = config.allKeys()
    config.endGroup()
    typelist = map(str, typelist)
    return typelist
    

# 清除选中的测试项目
def itemchecked_clean():
    config = QSettings(".testsetting.ini", QSettings.IniFormat)
    config.remove("perf_testlists")  # 清除perf选择的测试项目
    
# 初始化环境
def initenv():
    # 清除临时文件和目录
    tempfile = [".tempseting.ini", "tmp", "current-result/performance/", "current-report/"]
    for tmpfile in tempfile:
        delete_file_folder(tmpfile)
    # 清除之前选中的测试项目
    itemchecked_clean()

def get_item_temp_args(item):
    item_args = {}
    config = QSettings(".tempseting.ini", QSettings.IniFormat)
    config.beginGroup(item)
    item_argslist = config.allKeys()
    config = QSettings(".tempseting.ini", QSettings.IniFormat)
    for item_arg in item_argslist:
        item_args[str(item_arg)] = str(config.value(QString("%s/"% item) + item_arg).toString()[0:])
    return item_args

# 获取当前结果列表
def getcurrentresult():
    config = QSettings(".resultseting.ini", QSettings.IniFormat)
    result_address = {}
    result_address["address"] = config.value("currentresult/" + "resultaddress").toString()[0:]
    result_address["name"] = config.value("currentresult/" + "resultname").toString()[0:]
    return result_address

#_item_temp_args("sysbenchmem")
#print a
# test-case

# a = getitemlist("perfcpu")
# print(a)
# test = getitemargs("sysbenchcpu")
# print test["args"]
# gettesttool()
# getresultslist()
# writeconfig(".resultseting.ini", "test", "test", "test")    
# delete_file_folder("tmp")
# sumtests()
# save_testitem_args()
# get_item_args("sysbenchcpu")
