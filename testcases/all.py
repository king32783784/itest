'''
    pingpong: thread manage test benchmark
    test: Perf_thread
'''
import os
import shutil
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
         Depend: gcc make automake libtool
        '''
        # install depend tool
        RunTest._depend('gcc', 'make')
        # download and install testtool
        srcdir = RunTest._pretesttool('all',"infotest1.0.tar.gz", self.tool, self.homepath)
        os.chdir(srcdir)

    def _runtest(self):
        print "test is %s" % self.args
        testtype = self.args['argt']
        cmd = " -t " + testtype
        RunTest._dotest('info_test.sh', cmd, 1)
