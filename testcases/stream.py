'''
    stream: Mem test benchmark
    test: Perf_mem
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
         Depend: gcc make automake libtool
        '''
        # install depend tool
        RunTest._depend('gcc', 'make')
        print("test setup log")
        # download and install testtool
        srcdir = RunTest._pretesttool('stream',"stream-5.9.tar.gz", self.tool, self.homepath)
        os.chdir(srcdir)
        self._make('')

    def _runtest(self):
        print "test is %s" % self.args
        runtimes = self.args['args']
        numthread=self.args['argt'].split(',')
        for thread in numthread:
            RunTest._dotest('stream_test', thread, runtimes)
