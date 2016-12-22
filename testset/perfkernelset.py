#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog

class PerfkernelSet(QDialog):

    def __init__(self, parent=None):
        super(PerfkernelSet, self).__init__(parent)
        self.setWindowTitle(u"系统基准")
        self.resize(450, 550)
        palette1 = QtGui.QPalette()
        palette1.setColor(self.backgroundRole(), QColor("#cccddc"))
        self.setPalette(palette1)
        self.setAutoFillBackground(True)
        self.argstemp = {}
        self.createcheckbox()
        self.createbutton()
        self.Layout()
        self.initstatus()
    
    def createcheckbox(self):
        self.checkbox_lmbench = QtGui.QCheckBox(u'lmbench')
        self.connect(self.checkbox_lmbench, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_lmbench)

    def createbutton(self):
        self.lmbenchsetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.lmbenchsetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetlmbench)
        self.defaultbutton = QtGui.QPushButton(u"默认")
        self.connect(self.defaultbutton, QtCore.SIGNAL('clicked()'),
                     self.Ondefault)
        self.helpbutton = QtGui.QPushButton(u"帮助")
        self.connect(self.helpbutton, QtCore.SIGNAL('clicked()'),
                     self.Onhelp)
        self.setbutton = QtGui.QPushButton(u"确认")
        self.connect(self.setbutton, QtCore.SIGNAL('clicked()'),
                     self.Onset)
        self.setallbutton = QtGui.QPushButton(u"全选")
        self.connect(self.setallbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetall)
    
    def Layout(self):
        baseLayout = QGridLayout()
        baseLayout.addWidget(self.checkbox_lmbench, 0,0)

        baseLayout.addWidget(self.lmbenchsetbutton, 0,3)
        
        footer1Layout = QHBoxLayout()
        acer1 = QtGui.QSpacerItem(30,160)
        acer2 = QtGui.QSpacerItem(100,10)
        
        footer2Layout = QHBoxLayout()
        footer1Layout.addWidget(self.helpbutton)
        footer1Layout.addWidget(self.defaultbutton)
        baseLayout.addItem(acer1, 3,0)
        baseLayout.addItem(acer2, 4,1)
        footer2Layout.addWidget(self.setallbutton)
        footer2Layout.addWidget(self.setbutton)

       # baseLayout.setSizeConstraint(QLayout.SetFixedSize)
       # baseLayout.setSpacing(10)
        baseLayout.addLayout(footer1Layout,4,0)
        baseLayout.addLayout(footer2Layout,4,3)
        self.setLayout(baseLayout)

    def initstatus(self):
        testargs = self.readsetting("perfkernel-user/")
        if testargs["lmbench"] == "E":
            self.checkbox_lmbench.setChecked(True)
   
    def readsetting(self, setmode):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        testargs = {}
        testargs["lmbench"] = self.config.value(QString(setmode) + "lmbench").toString()[0:]
        return testargs

    def updatesetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.beginGroup("perfkernel-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def Oncheckbox_lmbench(self):
        if self.checkbox_lmbench.isChecked():
            self.argstemp["lmbench"] = "E"
        else:
            self.argstemp["lmbench"] = "D"

    def Onsetlmbench(self):
        lmbench = LmbenchSet()
        lmbench.exec_()

    def Ondefault(self):
        defaultset = self.readsetting("perfkernel-default/")
        if defaultset["lmbench"] == "E":
            self.checkbox_lmbench.setChecked(True)
        else:
            self.checkbox_lmbench.setChecked(False)
        self.argstemp = defaultset

    def Onhelp(self):
        helpdialog = HelpPerfkernel()
        helpdialog.exec_()
    
    def Onset(self):
        self.updatesetting()
        self.close()

    def Onsetall(self):
        self.checkbox_lmbench.setChecked(True)
        self.argstemp["lmbench"] = "E"

# unixbench设置
class LmbenchSet(QDialog):

    def __init__(self, parent=None):
        super(LmbenchSet, self).__init__(parent)
        self.setWindowTitle("Lmbench设置")
        self.resize(450,550)
        palette1 = QtGui.QPalette()
        palette1.setColor(self.backgroundRole(), QColor("#cccddc"))
        self.setPalette(palette1)
        self.setAutoFillBackground(True)
        self.argstemp = {}
        self.createlabels()
        self.initstatus()
        self.createbutton()
        self.Layout()

    def createlabels(self):
        self.timeslabel = QLabel(self.tr("测试次数t(times)"))
        self.timesshow = QLabel("")
        self.timesshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)

    def createbutton(self):
        self.timesbutton = QPushButton(u"自定义")
        self.connect(self.timesbutton, QtCore.SIGNAL("clicked()"), self.Ontimesbutton)
        self.helpbutton = QPushButton(u"帮助")
        self.connect(self.helpbutton, QtCore.SIGNAL("clicked()"), self.Onhelpbutton)
        self.defaultbutton = QPushButton(u"默认")
        self.connect(self.defaultbutton, QtCore.SIGNAL("clicked()"), self.Ondefaultbutton)
        self.setbutton = QPushButton(u"确认")
        self.connect(self.setbutton, QtCore.SIGNAL("clicked()"), self.Onsetbutton)

    def Layout(self):
        baseLayout = QGridLayout()
        baseLayout.addWidget(self.timeslabel, 0,0)
        baseLayout.addWidget(self.timesshow, 0,1)

        baseLayout.addWidget(self.timesbutton, 0,2)

        footer1Layout = QHBoxLayout()
        acer1 = QtGui.QSpacerItem(30,160)
        acer2 = QtGui.QSpacerItem(50,10)

        footer2Layout = QHBoxLayout()
        footer1Layout.addWidget(self.helpbutton)
        footer1Layout.addWidget(self.defaultbutton)
        baseLayout.addItem(acer1, 3,0)
        baseLayout.addItem(acer2, 4,1)
        footer2Layout.addWidget(self.setbutton)

       # baseLayout.setSizeConstraint(QLayout.SetFixedSize)
       # baseLayout.setSpacing(10)
        baseLayout.addLayout(footer1Layout,4,0)
        baseLayout.addLayout(footer2Layout,4,3)
        self.setLayout(baseLayout)

    def initstatus(self):
        testargs = self.readsetting()
        self.timesshow.setText(str(testargs["args"]))

    def updatesetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.beginGroup("lmbench-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        testargs = {}
        testargs["args"] = self.config.value(QString("lmbench-user/") + "args").toInt()[0]
        return testargs

    def Ontimesbutton(self):
        args, ok = QInputDialog.getInteger(self,
                                           self.tr(u'参数times'),
                                           self.tr(u"请输入参数times:默认为3"),
                                           int(self.timesshow.text()),1,10)
        if ok:
            self.timesshow.setText(str(args))
            self.argstemp['args'] = str(args)

    def Onhelpbutton(self):
        helpdialog = HelpLmbench()
        helpdialog.exec_()

    def Ondefaultbutton(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.argstemp["args"] = self.config.value(QString("lmbench-default/") + "args").toInt()[0]
        self.timesshow.setText(str(self.argstemp["args"]))

    def Onsetbutton(self):
        self.updatesetting()
        self.close()


# HELP

class HelpLmbench(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""Lmbench test 设置说明"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

class HelpPerfkernel(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""系统基准性能目前收录了lmbench一种测试工具"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

# test
# app = QApplication(sys.argv)
# form = PerfkernelSet()
# form.show()
# app.exec_()
