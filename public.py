import os
import linecache
import time
from parsing_xml import Parsing_XML

class ReadSysinfo(object):
    @staticmethod
    def os_name():
        f = open('/etc/os-release', 'r')
        theline = linecache.getline("/etc/os-release", 5)
        osname_line = theline[13:-2]
        osname = osname_line.replace(' ', '_')
        return osname
    
class ReadPublicinfo():

    def __init__(self, setupxml, testparameterxml):
        self.setupxml = setupxml
        self.testparameterxml = testparameterxml
        self.setupinfo = self.setup_info()
        self.dotestlist = self.testlists()

    def os_name(self):
        f = open('/etc/os-release', 'r')
        theline = linecache.getline("/etc/os-release", 5)
        osname_line = theline[13:-2]
        osname = osname_line.replace(' ', '_')
        return osname

    def setup_info(self):
        '''
           test_setup_info is Dictionary.
           'xml_list': ['testqurey', 'testtype', 'default',
            'defperf', 'definfo', 'defstab', 'deffun', 'cusperf',
            'cusinfo', 'cusstab', 'cusfun']
            'xml_dict': {'testqurey': ['yes'], 'testtype': ['default'],
            'default':['performance'], 'defperf':['Perf_cpu'],
            'definfo':['Hwinfo'], 'dfstab':['Stb_cpu'], 'deffun':
            ['Fun_kernel'], 'cusperf':['Perf_cpu'],'cusinfo':[],'cusstab'
            :[],'cusfun':[]
        '''
        test_setup_info = Parsing_XML.specific_elements('testtype', self.setupxml)
        return test_setup_info

    def testlists(self):
        tmpdict = self.setupinfo['xml_dict']
        dotestlist = {}
        testtypelist = tmpdict['Performance'][0].split(' ')
        dotestlist['performance']=testtypelist
        return dotestlist
# TEST
# a=ReadPublicinfo()
# testtypelist = a.setupinfo['xml_dict']['defperf'][0].split(' ')
# print testtypelist
# print a.setupinfo
# testlist = a.testlists()
# print testlist
