'''
    specjvm2008: Java test benchmark
    test: Perf_java
'''
import os
from subprocess import Popen,PIPE
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
        RunTest._depend('java')
        # download and install testtool
        srcdir = RunTest._pretesttool('specjvm',"SPECjvm2008.tar.gz", self.tool, self.homepath)
        os.chdir(srcdir)

    def _runtest(self):
        print "test is %s" % self.args
        runtimes = self.args['argt']
        test = Popen('which java', stdout=PIPE, shell=True)
        cmd = test.communicate()[0].strip('\n')
        args = " -jar SPECjvm2008.jar "
        RunTest._dotest(cmd, args, runtimes)
