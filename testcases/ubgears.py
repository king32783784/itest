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
         Deepend: gcc make glew-devel SDL-devel
        '''
        RunTest._depend('gcc', 'make', 'glew-devel', 'SDL-devel') 
        srcdir = RunTest._pretesttool('ubgears', 'ubgears-1.0.tar.gz', self.tool, self.homepath)
        os.chdir(srcdir)
        self._make('')

    def _runtest(self):
        print "test is %s" % self.args
        runtimes = self.args["argt"]
        cmd = ''
        RunTest._dotest("ubgears.sh", cmd, runtimes)
