# coding: utf-8
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class ResultSorting(object):

    def readfile(self, resultfile):
        fopen = open(resultfile, 'r')
        f = fopen.read().strip()
        return f

    def datasearch(self, searchmode, resultfile, times):
        times = int(times)
        f = self.readfile(resultfile)
        re_list = re.findall(r"%s" % searchmode, f, re.S)
        testarry = []
        for i in re_list:
            testarry.append(float(i))
        j = 0
        averge = []
        for i, data in enumerate(testarry, 1):
            if i % times == 0:
                averge.append((sum(testarry[j:i]) / times))
                j = i
        result = []
        for i in averge:
            result.append(float(format(i, '0.2f')))
        return result

    def datasearch_lm(self, searchmode, resultfile, times):
        def checkk(num):
            if 'K' in num:
                testtmp = float((re.sub('K', '0', num)))
                return testtmp * 1000
            else:
                return float(num)
                re_list_new.append(checkk(j))
        times = int(times)
        f = self.readfile(resultfile)
        re_list = re.findall(r"%s" % searchmode, f, re.S)
        re_list_new = []
        for i in re_list:
            re_list_tmp = i.split(' ')
            re_list_temp = []
            for j in re_list_tmp:
                if len(j) > 0:
                    re_list_temp.append(checkk(j))
            re_list_new.append(re_list_temp)
        re_list_total=re_list_new[0]
        for i in re_list_new[1:]:
             re_list_total = map(lambda(a,b):a+b, zip(i, re_list_total))
        re_list_final=[]
        for i in re_list_total:
            re_list_final.append(round(i / times ,2))
        return re_list_final
# useage
# a=ResultSorting()
# d = a.datasearch_lm("V8test result is 总成绩: (.*?)\n", "finalresult/iSoft_Server_OS_5.0/Perf_browser/result/result.out", 3)
# print d
