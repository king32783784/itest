'''
    stressapptest: CPU&MEM High Load Test
    test: stb-cpu&mem
'''
import os
import time
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
        srcdir = RunTest._pretesttool('ltpbasic',"ltp-full-20170116.tar.gz", self.tool, self.homepath)
        os.chdir(srcdir)
        self._configure('')
        self._make('')

    def _runtest(self):
        os.chdir("/opt/ltp")
        print "test is %s" % self.args
        cmd = "-o runalltest.out -p -l runalltest.log"
        RunTest._dotest('runltp', cmd, 1)
        time.sleep(10)
        f = open("/opt/ltp/results/runalltest.log")
        while 1:
            lines = f.readlines(10000)
            if not lines:
                break
            for line in lines:
                print line
