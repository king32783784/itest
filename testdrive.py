# *-*coding=utf-8*-*
'''
   Implementation test drive
'''
import os
import shutil
import sys
import logging
from common import *
from runtest import RunTest
from preparetest import TestParpare
from logging_config import *

class TestDrive(TestParpare):
    logger = logging.getLogger('itest')
    homepath = os.getcwd()
    sys.path.append(os.path.abspath('testcases'))

    def __init__(self, testtype, todotesttool):
        self.test = todotesttool
        self.testtype = testtype

    def mktestdir(self, pertesttype, pertest):
        dirtypes = ['result', 'debug']
        dirlist = {}
        localpath = os.path.join(self.homepath, 'current-result/')
        for pertype in dirtypes:
            dirpath = self.mkdirectory(localpath, '/',
                                       pertesttype, pertest,
                                       pertype)
            dirlist[pertype] = dirpath
            self.logger.info(dirlist)
        return dirlist

    def dosetup(self):
        finalresultpath = os.path.join(self.homepath, 'finalresult') # 结果保存目录
        finalresultdir = self.mkdirectory(finalresultpath, '/')   # 创建目录


    def runtest(self):
        testtoolget = gettesttool()
        testargs = getitemargs(self.test)
        self.logger.info("This time test is %s" % self.test)
        pathlist = self.mktestdir(self.testtype, self.test)
        job = __import__('%s' % self.test)
        logname = self.test + "debug"
        Logging_Config.setlogger(logname, '%s/setup.out' % pathlist['debug'])
        stderr_logger = logging.getLogger(logname)
        runjob = job.DoTest(testtoolget, testargs, self.homepath)
        setup = StreamToLogger(stderr_logger, logging.DEBUG)
        sys.stdout = setup
        runjob._setup()
        Logging_Config.setlogger(self.test, '%s/result.out' % pathlist['result'])
        stdout_logger = logging.getLogger(self.test)
        test = StreamToLogger(stdout_logger, logging.INFO)
        sys.stdout = test
        runjob._runtest()
        os.chdir(self.homepath)

    
    def doclean(self):
        tmpfile = os.path.join(self.homepath, "tmp")
        delete_file_folder(tmpfile)

    def dotest(self):
        self.logger.info('test start')
        self.runtest()
        self.doclean()


# testcase

if __name__ == "__main__":

# case1-sysbench
#    testa = TestDrive('perf', 'sysbenchcpu')
#    testa.dotest()
# case2 - stream
#    testb = TestDrive('perf', 'stream')
#    testb.dotest()

# case3 - iozone
#   testc = TestDrive('perf', 'iozone')
#   testc.runtest()

# case4 - unixbench
#   testd = TestDrive('perf', 'unixbench')
#   testd.runtest()

# case5 - pingpong
#    teste = TestDrive('perf', 'pingpong')
#    teste.runtest()

# case6 - lmbench
#    testf = TestDrive('perf', 'lmbench')
#    testf.runtest()

# case7 - specjvm
    testg = TestDrive('perf', 'sysbenchcpu')
    testg.dotest()
