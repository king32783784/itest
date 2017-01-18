'''
    glmark: System 3d benchmark
    test: Perf_3d
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
         Deepend: gcc make expect gcc-c++
        '''
        RunTest._depend('gcc', 'make', 'gcc-c++', ) 
        srcdir = RunTest._pretesttool('glmark', 'GLMark-0.5.2.1.tar.gz', self.tool, self.homepath)
        os.chdir(srcdir)
        self._make('')

    def _runtest(self):
        print "test is %s" % self.args
        runtimes = self.args["args"]
        bpp = self.args["argb"]
        height= self.args["argh"]
        width= self.args["argw"]
        window= self.args["argm"]
        cmdargs = width + " " +  height + " " + bpp + " " + window
        RunTest._dotest("glmark.sh", cmdargs, runtimes)
