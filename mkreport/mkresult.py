#/usr/bin/env python
# coding: utf-8
import os
import sys
sys.path.append('..')
from common import *
from mk_html import *
from data_operation import *

def mk_current_report():
   typelist = get_aftertest_typelist()
   testlist = get_aftertest_itemlist(typelist[0])
   mk_html_main("current-report/test.md", ["test"], testlist)

#mk_current_report()


    
