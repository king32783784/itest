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
        srcdir = RunTest._pretesttool('stressapptest',"stressapptest.tar.gz", self.tool, self.homepath)
     #   srcdir = os.path.join(srcdir, 'src/')
        os.chdir(srcdir)
        self._make('')

    def _runtest(self):
        print "test is %s" % self.args
        argt = self.args['argt']
        argl = float(self.args['argl']) / 100
        cmd = "%s %s" % (argt, argl)
        RunTest._dotest('stressapptest.sh', cmd, 1)
