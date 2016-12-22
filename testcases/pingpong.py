'''
    pingpong: thread manage test benchmark
    test: Perf_thread
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
        # download and install testtool
        srcdir = RunTest._pretesttool('pingpong',"pingpong.tar.gz", self.tool, self.homepath)
        os.chdir(srcdir)

    def _runtest(self):
        print "test is %s" % self.args
        runtimes = self.args['args']
        numthread=self.args['argt'].split(',')
        args_thread = ""
        for thread in numthread:
            args_thread = args_thread + ' %s ' % thread
        
        RunTest._dotest('RunTest.sh', args_thread, runtimes)
