'''
    unixbench: system index benchmark
    test: Perf_system
'''
import os
from runtest import RunTest
from common import *

class DoTest(RunTest):
    def __init__(self,testtoolget, testargs, homepath):
        self.homepath = homepath
        self.tool = testtoolget
        self.args = testargs
    
    def _setup(self):
        '''
         Setup before starting test
         Depend: gcc make perl-Time-HiRes
        '''
        # install depend tool
        RunTest._depend('gcc', 'make', 'perl-Time-HiRes')
        # download and install testtool
        srcdir = RunTest._pretesttool('unixbench',"unixbench-5.1.3.tar.gz", self.tool, self.homepath)
        os.chdir(srcdir)
        self._make('')

    def _runtest(self):
        print "test is %s" % self.args
        runtimes = self.args['args']
        numthread=self.args['argt'].split(',')
        for thread in numthread:
            RunTest._dotest('unixbench', thread, runtimes)
