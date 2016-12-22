'''
    sysbench: System evaluation benchmark
    test: Perf_cpu Perf_mem Perf_mysql
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
        RunTest._depend('gcc', 'make', 'automake', 'libtool')
        # download and install testtool
        srcdir = RunTest._pretesttool('sysbench',"sysbench-0.4.12.tar.gz", self.tool, self.homepath)
        os.chdir(srcdir)
        self._configure('--without-mysql')
        self._make('LIBTOOL=/usr/bin/libtool')

    def _runtest(self):
        print "test is %s" % self.args
        runtimes = self.args['argts']
        numthread=self.args['argt'].split(',')
        memblock = self.args["argb"]
        memsize = self.args["args"]
        for thread in numthread:
            cmd = "--test=memory --num-threads=%s --memory-block-size=%s --memory-total-size=%sG run" % (thread, memblock, memsize)
            RunTest._dotest('sysbench', cmd, runtimes)
