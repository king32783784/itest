import os
from parsing_xml import Parsing_XML


class ParameterAnalysis():

    @staticmethod
    def baseparameter(doitem, testxml):
        itembasecmd = Parsing_XML.parsing_label_list(doitem, testxml)
        test = itembasecmd[0].split(' ')
        itembasecmd = {}
        for pertest in test:
            testa = pertest.split('=')
            itembasecmd[testa[0]] = testa[1]
        return itembasecmd

    def specificparameter(self):
        pass

    def test_reboot(self):
        pass

    def run_cmd(self):
        pass

# testcase
# test = ParameterAnalysis()
# a = test.baseparameter('Perf_io', 'Test_parameter.xml')
# print a
