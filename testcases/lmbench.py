'''
    lmbench: linux kernel performance benchmark
    test: Perf_kernel
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
        RunTest._depend('gcc', 'make')
        # download and install testtool
        srcdir = RunTest._pretesttool('lmbench',"lmbench3.tar.gz", self.tool, self.homepath)
        os.chdir(srcdir)
        self._make('results')

    def _runtest(self):
        print "test is %s" % self.args
        runtimes = self.args['args']
        runtimes = int(runtimes) - 1
        cmd = ' '
        RunTest._dotest('/bin/make rerun', cmd, runtimes)
        RunTest._dotest('/bin/make see', cmd, 1)
