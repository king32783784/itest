import os
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui,QtCore

def sumtests():
    totaltests = readtestlist()
    totalnum = 0
    for key, value in totaltests.iteritems():
        totalnum += len(value)
    return totalnum

def getestlist(testtype):
    testlist = []
    config = QSettings(".testseting.ini", QSettings.IniFormat)
    config.beginGroup(testtype)
    tmptestlist = config.allKeys()
    config.endGroup()
    for testitem in tmptestlist:
        testlist.append(str(testitem))
    return testlist

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

def checkstatus(group, item):
    config = QSettings(".testseting.ini", QSettings.IniFormat)
    status = config.value(QString("%s/" % group) + item).toString()[0:]
    return status

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
        print testargs
        return testargs
    except:
        return 0

def gettesttool():
    try:
        testtool = {}
        config = QSettings(".testseting.ini", QSettings.IniFormat)
        testtool["mode"] = config.value(QString("testtool-user/") + "settoolstatus").toString()[0:]
        if testtool["mode"] == "L":
            testtool["address"] = config.value(QString("testtool-user/") + "dir").toString()[0:]
        else:
            testtool["address"] = config.value(QString("testtool-user/") + "address").toString()[0:]
        print testtool
        return testtool
    except:
        print "testtool adress get faild"
        return 0 

def writeconfig(configname, begin, key, value):
    config = QSettings(configname, QSettings.IniFormat)
    config.beginGroup(begin)
    config.setValue(key, value)
    config.endGroup()
    

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

def getlocatepath():
    return  os.getcwd()

def getlocattime():
    FORMAT = '%Y%m%d%H%M%S'
    return time.strftime(FORMAT, time.localtime(time.time()))

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

def createresultdir():
    homepath = getlocatepath()
    locatime = getlocattime()
    RESULTTYPE = "isoft-test-"
    tmpresultdir = RESULTTYPE + locatime
    return tmpresultdir

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
