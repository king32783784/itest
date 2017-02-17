'''
    stressapptest: CPU&MEM High Load Test
    test: stb-cpu&mem
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
        srcdir = RunTest._pretesttool('ltpbasic',"ltp-full-20170116.tar.gz", self.tool, self.homepath)
        os.chdir(srcdir)
        self._configure('')
        self._make('')

    def _runtest(self):
        os.chdir("/opt/ltp/testscripts/")
        print "test is %s" % self.args
        argt = self.args["argt"]
        cmd = "-d /tmp/sardate -l /tmp/ltplog -t %s -n -p -S" % argt
        RunTest._dotest('ltpstress.sh', cmd, 1)
        
