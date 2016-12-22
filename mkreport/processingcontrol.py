# coding: utf-8
import sys
from datasorting import ResultSorting
from mkxls import *
from mkhtml import *
from temp_main import *

reload(sys)
sys.setdefaultencoding('utf8')
class Control_processing(object):
    def __init__(self, myargs):
        '''{'items': ['cpu'], 'type': ['xls'], 'osnames': ['iSoft_Desktop_4.0']}'''
        self.args = myargs
        print self.args

    def _getxlsdata(self, oslist, itemlist):
        for testitem in itemlist:
            if testitem in exceptitem:
                for os in oslist:
                    for i, patterns in enumerate(patternmath[testitem]):
                        testdata=[]
                        datalist = []
                        for j, pattern in enumerate(patterns):
                            data = ResultSorting()
                            datatmp = data.datasearch_lm(pattern, "../current-result/%s/performance/%s/result/result.out" %(os, testitem), patternnum[testitem])
                            for k, datasub in enumerate(datatmp):
                                datalist.append(datatmp[k])
                        testdata.append(datalist)   
                        for datasub in testdata:
                            totaldata[testitem][i].append(datasub)
            else:
                for os in oslist:
                    for i, patterns in enumerate (patternmath[testitem]):
                        testdata=[]
                        datalist = []
                        for j, pattern in enumerate(patterns):
                            data=ResultSorting()
                            datatmp = data.datasearch(pattern, "../current-result/%s/performance/%s/result/result.out" %(os, testitem), patternnum[testitem])
                            for k, datasub in enumerate(datatmp):
                                datalist.append(datatmp[k])
                        testdata.append(datalist)   
                        for datasub in testdata:
                            totaldata[testitem][i].append(datasub)
        return totaldata
 
    def _gethtmldata(self, oslist, itemlist):
        for testitem in itemlist:
            if testitem in exceptitem:
                for i, patterns in enumerate (patternmath[testitem]):
                    for os in oslist:
                        testdata=[]
                        datalist = []
                        for j, pattern in enumerate(patterns):
                            data=ResultSorting()
                            datatmp = data.datasearch_lm(pattern, "../current-result/%s/performance/%s/result/result.out" %(os, testitem), 3)
                            for k, datasub in enumerate(datatmp):
                                datalist.append(datatmp[k])
                        testdata.append(datalist)
                        for datasub in testdata:
                            htmldata[testitem].append(datasub)
            else:
                for i, patterns in enumerate (patternmath[testitem]):
                    for os in oslist:
                        testdata=[]
                        datalist = []
                        for j, pattern in enumerate(patterns):
                            data=ResultSorting()
                            datatmp = data.datasearch(pattern, "../current-result/%s/performance/%s/result/result.out" %(os, testitem), 3)
                            for k, datasub in enumerate(datatmp):
                                datalist.append(datatmp[k])
                        testdata.append(datalist)
                        for datasub in testdata:
                            htmldata[testitem].append(datasub)
        return htmldata

    def _mkxls(self):
        '''infolist=[sheet_speccpu_info, sheet_lmbench_info, sheet_syscpu_info]
           datalist=[sheet_speccpu_data, sheet_lmbench_data, sheet_syscpu_data]
        ''' 
        itemlist = self.args['items']
        oslist = self.args['osnames']
        for reporttype in self.args['type']:
            if reporttype == "xls":
                totaldata = self._getxlsdata(oslist, itemlist)
                mkxls(totaldata, itemlist, oslist)
            elif reporttype == "html":
                htmldata = self._gethtmldata(oslist, itemlist)
                mkhtml(htmldata, itemlist, oslist)
            else:
                print("Wrong report type, please check it")
                exit()
     
#testcase
#a=Control_processing()
#a._mkxls()
