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
         Deepend: gcc make 
        '''
        RunTest._depend('gcc', 'make') 
        srcdir = RunTest._pretesttool('x11perf', 'x11perf-1.0.tar.gz', self.tool, self.homepath)
        os.chdir(srcdir)
        self._make('')

    def _runtest(self):
        print "test is %s" % self.args
        runtimes = self.args["argt"]
        cmd = ''
        RunTest._dotest("x11perf.sh", cmd, runtimes)
