'''
    sysbench: System evaluation benchmark
    test: Perf_cpu Perf_mem Perf_mysql
'''
import os
from runtest import RunTest
from pretreatment_result import MkResult

class DoTest(RunTest):
    def __init__(self, setupxml, testxml, homepath, finalresult):
        self.setupxml = os.path.abspath(setupxml)
        self.testxml = os.path.abspath(testxml)
        self.homepath = homepath
        self.result = finalresult
    
    def _setup(self):
        '''
         Setup before starting test
        '''
        print self.setupxml
        print self.testxml
        RunTest._depend('gcc', 'make') 
        srcdir = RunTest._pretesttool(self.setupxml, self.testxml, 'Perf_kernel', self.homepath)
        os.chdir(srcdir)
        self._make('results')

    def _runtest(self):
        basearg = self.baseparameter('Perf_kernel', self.testxml)
        print basearg
        runtimes = basearg['runtimes']
        cmd = ' '
        RunTest._dotest('/bin/make rerun', cmd, runtimes-1)
        RunTest._dotest('/bin/make see', cmd, 1)
        
#        resulttmppath = os.path.join(self.homepath, 'resulttmp/performance/Perf_cpu/result/result.out')
#        doprocessresult = MkResult(data_cpu_aidinfo, runtimes, resulttmppath, self.result)
#        doprocessresult.mkresult()          
# testcase
#a = Perf_cpu('Testsetup_sample.xml', 'Test_parameter.xml')
#a._setup()
#a._runtest()
