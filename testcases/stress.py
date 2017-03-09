'''
    stress: Threads High Load Test
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
        srcdir = RunTest._pretesttool('stress', "stress-1.0.4.tar.gz", self.tool, self.homepath)
        os.chdir(srcdir)
        self._configure('')
        self._make('')

    def _runtest(self):
        print "test is %s" % self.args
        args = self.args['args'] # times
        argt = self.args['argt'] # threads
        thread = int(argt) / 4
        args = int(args) * 3600
        cmd = "--cpu %s --io %s --vm %s -d %s --timeout %s" % (thread,\
            thread, thread, thread, args)
        os.chdir("src")
        RunTest._dotest('stress', cmd, 1)
        print "stress test is PASS"
        print "stress test finish"
