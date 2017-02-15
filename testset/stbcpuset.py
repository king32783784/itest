#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog
from common import *

class StbcpuSet(QDialog):

    def __init__(self, parent=None):
        super(StbcpuSet, self).__init__(parent)
        self.setWindowTitle(u"CPU稳定性")
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
        self.checkbox_stressappcpu = QtGui.QCheckBox(u'stressapptest')
        self.connect(self.checkbox_stressappcpu, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_stressappcpu)

    def createbutton(self):
        self.stressappcpusetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.stressappcpusetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetstressappcpu)
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
        baseLayout.addWidget(self.checkbox_stressappcpu, 0,0)

        baseLayout.addWidget(self.stressappcpusetbutton, 0,3)
        
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
        testargs = self.readsetting("stresscpu-user/")
        if testargs["stressappcpu"] == "E":
            self.checkbox_stressappcpu.setChecked(True)
   
    def readsetting(self, setmode):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["stressappcpu"] = self.config.value(QString(setmode)
                                   + "stressappcpu").toString()[0:]
        return testargs

    def updatesetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("stresscpu-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def Oncheckbox_stressappcpu(self):
        if self.checkbox_stressappcpu.isChecked():
            self.argstemp["stressappcpu"] = "E"
        else:
            self.argstemp["stressappcpu"] = "D"

    def Onsetstressappcpu(self):
        setstressappcpu = SysbenchSet()
        setstressappcpu.exec_()
       
    def Ondefault(self):
        defaultset = self.readsetting("stresscpu-default/")
        if defaultset["stressappcpu"] == "E":
            self.checkbox_stressappcpu.setChecked(True)
        else:
            self.checkbox_stressappcpu.setChecked(False)    
        self.argstemp = defaultset

    def Onhelp(self):
        helpdialog = HelpPerfcpu()
        helpdialog.exec_()
    
    def Onset(self):
        self.updatesetting()
        self.close()

    def Onsetall(self):
        self.checkbox_stressappcpu.setChecked(True)
        self.argstemp["stressappcpu"] = "E"

# stressapp-cpu测试设置

class SysbenchSet(QDialog):
    
    def __init__(self, parent=None):
        super(SysbenchSet, self).__init__(parent)
        self.setWindowTitle("sysbench设置")
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
        self.threadlabel = QLabel(self.tr("参数t(Threads)"))
        self.threadshow = QLabel("")
        self.threadshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.primelabel = QLabel(self.tr("参数cpu-max-prime"))
        self.primeshow = QLabel("")
        self.primeshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)

    def createbutton(self):
        self.threadbutton = QPushButton(u"自定义")
        self.connect(self.threadbutton, QtCore.SIGNAL("clicked()"), self.Onthreadbutton)
        self.primebutton = QPushButton(u"自定义")
        self.connect(self.primebutton, QtCore.SIGNAL("clicked()"), self.Onprimebutton)
        self.helpbutton = QPushButton(u"帮助")
        self.connect(self.helpbutton, QtCore.SIGNAL("clicked()"), self.Onhelpbutton)
        self.defaultbutton = QPushButton(u"默认")
        self.connect(self.defaultbutton, QtCore.SIGNAL("clicked()"), self.Ondefaultbutton)
        self.setbutton = QPushButton(u"确认")
        self.connect(self.setbutton, QtCore.SIGNAL("clicked()"), self.Onsetbutton)

    def Layout(self):
        baseLayout = QGridLayout()
        baseLayout.addWidget(self.threadlabel, 0,0)
        baseLayout.addWidget(self.primelabel, 1,0)
        baseLayout.addWidget(self.threadshow, 0,1)
        baseLayout.addWidget(self.primeshow, 1,1)
        
        baseLayout.addWidget(self.threadbutton, 0,3)
        baseLayout.addWidget(self.primebutton, 1,3)

        footer1Layout = QHBoxLayout()
        acer1 = QtGui.QSpacerItem(30,240)
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
        self.threadshow.setText(str(testargs["argt"]))
        self.primeshow.setText(str(testargs["argp"]))

    def updatesetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("sysbenchcpu-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["argt"] = self.config.value(QString("sysbenchcpu-user/") + "argt").toInt()[0]
        testargs["argp"] = self.config.value(QString("sysbenchcpu-user/") + "argp").toString()[0:]
        return testargs

    def Onthreadbutton(self):
        argt, ok = QInputDialog.getInteger(self,
                                           self.tr(u"参数t"),
                                           self.tr(u"请输入参数t的值:"),
                                           int(self.threadshow.text()), 1,256)
        if ok:
            self.threadshow.setText(str(argt))
            self.argstemp['argt'] = str(argt)

    def Onprimebutton(self):
        list_argp = QStringList()
        list_argp.append(self.tr("10000"))
        list_argp.append(self.tr("10000,20000"))
        list_argp.append(self.tr("10000,20000,30000"))
        argp, ok = QInputDialog.getItem(self, self.tr(u'参数prime'),
                                        self.tr(u"请输入参数prime的值:以,分隔"),
                                        list_argp)
        if ok:
            self.primeshow.setText(argp)
            self.argstemp['argp'] = str(argp)

    def Onhelpbutton(self):
        helpdialog = HelpSyscpu()
        helpdialog.exec_()

    def Ondefaultbutton(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.argstemp["argt"] = self.config.value(QString("sysbenchcpu-default/") + "argt").toInt()[0]
        self.argstemp["argp"] = self.config.value(QString("sysbenchcpu-default/") + "argp").toString()[0:]
        self.primeshow.setText(self.argstemp["argp"])
        self.threadshow.setText(str(self.argstemp["argt"]))

    def Onsetbutton(self):
        self.updatesetting()
        self.close()


class HelpSyscpu(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""sysbench cpu test 设置说明"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)


class HelpPerfcpu(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""Stbcpu 包含stressapptest测试"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

# test
# app = QApplication(sys.argv)
# form = PerfcpuSet()
# form.show()
# app.exec_()
