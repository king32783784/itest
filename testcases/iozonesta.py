'''
    io: I/O test benchmark
    test: Perf_io
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
        srcdir = RunTest._pretesttool('iozonesta',"iozone3_465.tar.gz", self.tool, self.homepath)
        srcdir = os.path.join(srcdir, 'src/current')
        os.chdir(srcdir)
        self._make('linux')

    def _runtest(self):
        print "test is %s" % self.args
        argt = self.args['argt']
        RunTest._dotest('iozone.sh', argt, 1)
