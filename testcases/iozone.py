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
        srcdir = RunTest._pretesttool('iozone',"iozone-3.414.tar.gz", self.tool, self.homepath)
        srcdir = os.path.join(srcdir, 'src/current')
        os.chdir(srcdir)
        self._make('linux')

    def _runtest(self):
        print "test is %s" % self.args
        runtimes = self.args['times']
        testtype=self.args['argi'].split(',')
        args_i = ''
        for arg in testtype:
            args_i = args_i + ' -i ' + arg
        args = self.args['args']
        argt = self.args['argt']
        argr = self.args['argr']
        cmd = " -s %sG %s -t %s -r %s" % (args, args_i, argt, argr)
        RunTest._dotest('iozone', cmd, runtimes)
