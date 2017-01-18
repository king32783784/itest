'''
    ubgears: System 3d benchmark
    test: Perf_3d
'''
import os
from runtest import RunTest
from common import *

class DoTest(RunTest):
    def __init__(self, testtoolget, testargs, homepath):
        self.homepath = homepath
        self.tool = testtoolget
        self.args = testargs
    
    def _setup(self):
        '''
         Setup before starting test
         Deepend: gcc make  qt5*  qt5-qttools-devel
        '''
        RunTest._depend('gcc', 'make', 'qt4*', 'qt5-qttools-devel') 
        srcdir = RunTest._pretesttool('qtperf', 'qtperf.tar.gz', self.tool, self.homepath)
        os.chdir(srcdir)
        RunTest._dotest("Make", " ", 1)
     #   self._make('')

    def _runtest(self):
        print "test is %s" % self.args
        runtimes = self.args["args"]
        cmd = ''
        RunTest._dotest("qtperf4.sh", cmd, runtimes)
