'''
    sysbench: System evaluation benchmark
    test: Perf_cpu Perf_mem Perf_mysql
'''
import os
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
        '''
        srcdir = RunTest._pretesttool('css', 'Browser_benchmark.tar.gz', self.tool, self.homepath)
        os.chdir(srcdir)
    #    self._make('results')

    def _runtest(self):
        print "test is %s" % self.args
        runtype = self.args['argt']
        runtimes = self.args['args']
        RunTest._dotest('setup', '', 1)
        doargs = "Run.py -t %s -i 'acid'" % runtype
        RunTest._dotest('/usr/bin/python', doargs, runtimes)
