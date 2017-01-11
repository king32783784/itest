'''
    Enable client-side test preparation
'''
import os
import subprocess
from subprocess import PIPE, Popen
from downloadfile import downloadfile


class TestParpare():

    def testtooldownload(self, url, toolname, homepath):
        '''
           download test tool
        '''
        testtool = os.path.join(homepath, 'testtool')
        testtool = self.mktooldir(testtool)
        filepath = downloadfile(testtool, url, toolname)
        return filepath

    def baseddependency(*args):
        '''
           Check test tool based on
        '''
        deletioncmdlist = []
        for arg in args:
            testcmd = Popen('which %s' % arg, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True)
            testcmd.wait()
            exitcode = testcmd.poll()
            if exitcode != 0:
                deletioncmdlist.append(arg)
        return deletioncmdlist

    def joinpath(fun):
        def add_mkdir(self, default, sep, *args):
            try:
                default = os.path.join(default, sep.join(args))
                os.makedirs(default)
            except OSError:
                print 'joinpath filed'
            return fun(self, default, sep, *args)
        return add_mkdir

    @joinpath
    def mkdirectory(self, default, sep, *args):
        '''
        Test results directory processing
        '''
        return os.path.abspath(default)

    def mkinstalldir(self, installdir):
        if os.path.exists(installdir) is False:
            return self.mkdirectory(installdir, '')
        else:
            return installdir 

    def mktooldir(self, testtool):
        if os.path.exists(testtool) is False:
            return self.mkdirectory(testtool, '')
        else:
            return testtool
# testcase
# a=TestParpare()
# TestParpare.mktooldir()
# a.testtooldownload('', '')
# b=a.mkdirectory('tmp', ' ')
# print a.baseddependency('make', 'gcc', 'g++', 'java', 'hello', 'ls')
# testtool = a.mkdirectory('testtool', '' )
# print testtool
# a.testtooldownload('http://dl.360safe.com/360ap', '360FreeAP_Setup.exe')
