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
        RunTest._depend('gcc', 'make','expect', 'gcc-c++', 'glew-devel', 'SDL-devel', 'qt5*', 'qt5-qttools-devel') 
        srcdir = RunTest._pretesttool(self.setupxml, self.testxml, 'Perf_graphics', self.homepath)
        os.chdir(srcdir)
        RunTest._dotest('Make', '', 1)

    def _runtest(self):
        basearg = self.baseparameter('Perf_graphics', self.testxml)
        print basearg
        runtimes = basearg['runtimes']
        resolution_itmp = basearg['resolution'].split(',')
        args_resolution = ''
        for arg in resolution_itmp:
            args_resolution = args_resolution + ' ' + arg
        RunTest._dotest('Run', args_resolution, runtimes)
        
#        resulttmppath = os.path.join(self.homepath, 'resulttmp/performance/Perf_cpu/result/result.out')
#        doprocessresult = MkResult(data_cpu_aidinfo, runtimes, resulttmppath, self.result)
#        doprocessresult.mkresult()          
# testcase
#a = Perf_cpu('Testsetup_sample.xml', 'Test_parameter.xml')
#a._setup()
#a._runtest()
