import os
import time
import signal
import sys
import subprocess
from preparetest import TestParpare
from public import ReadPublicinfo
from testsetup import TestSetup
from parameter import ParameterAnalysis
from subprocess import call, PIPE, Popen


class RunTest(TestSetup, ParameterAnalysis):
    @staticmethod
    def pacagemanger(self, *args):
        '''
           Check test tool based on
        '''
        for arg in args:
            try:
                retcode = call('which %s' % arg, shell=True)
                if retcode == 0:
                    return arg
                    break
            except OSError:
                pass

    @staticmethod
    def packageinstall(defectlist):
        packagetool = RunTest.pacagemanger('dnf', 'yum', 'apt-get')
        for defect in defectlist:
            call('%s -y install %s' % (packagetool, defect), shell=True)

    @staticmethod
    def _depend(*args):
        defectlist = []
        for arg in args:
            testcmd = Popen('which %s' % arg, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True)
            testcmd.wait()
            exitcode = testcmd.poll()
            if exitcode != 0:
                defectlist.append(arg)
        if len(defectlist) > 0:
            RunTest.packageinstall(defectlist)

    @staticmethod
    def _pretesttool(testitem, tooltar, testtool,  homepath):
        setup = TestSetup()
        url = u"%s"%testtool["address"]
        print url
        tarfilepath = setup.testtooldownload(url, tooltar, homepath)
        testbindir = setup.decompressfile(tarfilepath, testitem, homepath)
        return testbindir
                        

    @staticmethod
    def _dotest(executable, cmd, runtimes):
        homedir = os.getcwd()
        for root, dirs, files in os.walk(homedir):
            if executable in files:
                executable = os.path.join(root, executable)
                break
        cmds = [executable, cmd]
        finalcmd = os.path.join(' ', ' '.join(cmds))
        print finalcmd
        for runonce in range(int(runtimes)):
            test = Popen(finalcmd, stdout=PIPE, stderr=PIPE, shell=True, preexec_fn=RunTest.restore_signals)
            stdout = test.communicate()[0]
            print stdout
        print("test for run test")

    @staticmethod
    def _runtest(executable, cmd, runtimes):
        homedir = os.getcwd()
        for root, dirs, files in os.walk(homedir):
            if executable in files:
                executable = os.path.join(root, executable)
                break
        cmds = [executable, cmd]
        finalcmd = os.path.join(' ', ' '.join(cmds))
        print finalcmd
        for runonce in range(int(runtimes)):
            try:
                retcode = call(finalcmd, shell=True)
                if retcode < 0:
                    print >> sys.stderr, "Child was terminated by signal", -retcode
                else:
                    print >>sys.stderr, "Child returned", retcode
            except OSError as e:
                print >>sys.stderr, "Execution failed:", e

    @staticmethod
    def restore_signals():
        signals = ('SIGPIPE', 'SIGXFZ', 'SIGXFSZ')
        for sig in signals:
            if hasattr(signal, sig):
                signal.signal(getattr(signal, sig), signal.SIG_DFL)

#call("./Run -c 4 -i 100 context1", shell=True, preexec_fn=restore_signals)
    @staticmethod
    def _test(executable, cmd, runtimes):
        homedir = os.getcwd()
        for root, dirs, files in os.walk(homedir):
            if executable in files:
                executable = os.path.join(root, executable)
                break
        cmds = [executable, cmd]
        finalcmd = os.path.join(' ', ' '.join(cmds))
        print finalcmd
        for runonce in range(int(runtimes)):
            returncode = subprocess.call(finalcmd, shell=True, preexec_fn=RunTest.restore_signals)

#RunTest._pretesttool('Testsetup_sample.xml', 'Test_parameter.xml', 'Perf_cpu')
