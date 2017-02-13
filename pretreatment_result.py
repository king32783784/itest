import os
from datasorting import ResultSorting
from public import ReadSysinfo


class MkResult(ResultSorting):
     def __init__(self, testitemaidinfo, times, resultfile, resultdir):
         self.testaidinfo = testitemaidinfo
         self.times = times
         self.resultfile = resultfile
         self.resultdir = resultdir
     
     def wraptreatment(self, length, charters):
         temp =''
         t = 0
         for i, charter in enumerate(charters, 1):
              if i % length == 0:
                  temp = temp + charters[t:i] + "\n"
                  t = i
         temp = temp + charters[t:]
         return temp
     
     def _mkmdfile(self, mdfile):
         dataresult = self.datasearch(self.testaidinfo['search_path'], self.resultfile, self.times)
         datatemp = ""
         for charter in dataresult:
              datatemp = datatemp + "|" + "%s" % charter
         f = open(mdfile, 'a+')
         testresult ="%s %s" %(ReadSysinfo.os_name(), datatemp)
         f.write("%s=\"%s\"" % (self.testaidinfo['itemname'], testresult))
    
     def mkresult(self):
         mdfile = os.path.join(self.resultdir, 'Lpb_i_pre.py')
         self._mkmdfile(mdfile)
#a = MkResult(data_cpu_aidinfo, 3, '/home/isoft_lp/Github/Lpbs-i/resulttmp/performance/Perf_cpu/result/result.out', '/home/isoft_lp/Github/Lpbs-i/finalresult')
#a.mkresult()
