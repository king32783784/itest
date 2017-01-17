#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog
from common import *

class PerfcpuSet(QDialog):

    def __init__(self, parent=None):
        super(PerfcpuSet, self).__init__(parent)
        self.setWindowTitle(u"CPU运算性能")
        self.resize(450, 550)
        palette1 = QtGui.QPalette()
        palette1.setColor(self.backgroundRole(), QColor("#cccddc"))
        self.setPalette(palette1)
        self.setAutoFillBackground(True)
        self.argstemp = {}
        print("test cpu set")
        self.createcheckbox()
        self.createbutton()
        self.Layout()
        self.initstatus()
    
    def createcheckbox(self):
        self.checkbox_spec0 = QtGui.QCheckBox(u'speccpu-2000')
        self.connect(self.checkbox_spec0, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_spec0)
        self.checkbox_spec6 = QtGui.QCheckBox(u'speccpu-2006')
        self.connect(self.checkbox_spec6, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_spec6)
        self.checkbox_sysbench = QtGui.QCheckBox(u'sysbench-cpu')
        self.connect(self.checkbox_sysbench, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_sysbench)

    def createbutton(self):
        self.spec0setbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.spec0setbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetsepc0)
        self.spec6setbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.spec6setbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetspec6)
        self.sysbenchsetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.sysbenchsetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetsysbench)
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
        baseLayout.addWidget(self.checkbox_spec0, 0,0)
        baseLayout.addWidget(self.checkbox_spec6, 1,0)
        baseLayout.addWidget(self.checkbox_sysbench, 2,0)

        baseLayout.addWidget(self.spec0setbutton, 0,3)
        baseLayout.addWidget(self.spec6setbutton, 1,3)
        baseLayout.addWidget(self.sysbenchsetbutton, 2,3)
        
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
        testargs = self.readsetting("perfcpu-user/")
        if testargs["spec0cpu"] == "E":
            self.checkbox_spec0.setChecked(True)
        if testargs["spec6cpu"] == "E":
            self.checkbox_spec6.setChecked(True)
        if testargs["sysbenchcpu"] == "E":
            self.checkbox_sysbench.setChecked(True)
   
    def readsetting(self, setmode):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["spec0cpu"] = self.config.value(QString(setmode) + "spec0cpu").toString()[0:]
        testargs["spec6cpu"] = self.config.value(QString(setmode) + "spec6cpu").toString()[0:]
        testargs["sysbenchcpu"] = self.config.value(QString(setmode) + "sysbenchcpu").toString()[0:]
        return testargs

    def updatesetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("perfcpu-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def Oncheckbox_spec0(self):
        if self.checkbox_spec0.isChecked():
            self.argstemp["spec0cpu"] = "E"
        else:
            self.argstemp["spec0cpu"] = "D"

    def Oncheckbox_spec6(self):
        if self.checkbox_spec6.isChecked():
            self.argstemp["spec6cpu"] = "E"
        else:
            self.argstemp["spec6cpu"] = "D"

    def Oncheckbox_sysbench(self):
        if self.checkbox_sysbench.isChecked():
            self.argstemp["sysbenchcpu"] = "E"
        else:
            self.argstemp["sysbenchcpu"] = "D"

    def Onsetsepc0(self):
        pass

    def Onsetspec6(self):
        pass

    def Onsetsysbench(self):
        setsysbench = SysbenchSet()
        setsysbench.exec_()
       
    def Ondefault(self):
        defaultset = self.readsetting("perfcpu-default/")
        if defaultset["spec0cpu"] == "E":
            self.checkbox_spec0.setChecked(True)
        else:
            self.checkbox_spec0.setChecked(False)
        if defaultset["spec6cpu"] == "E":
            self.checkbox_spec6.setChecked(True)
        else:
            self.checkbox_spec6.setChecked(False)
        if defaultset["sysbenchcpu"] == "E":
            self.checkbox_sysbench.setChecked(True)
        else:
            self.checkbox_sysbench.setChecked(False)    
        self.argstemp = defaultset

    def Onhelp(self):
        helpdialog = HelpPerfcpu()
        helpdialog.exec_()
    
    def Onset(self):
        self.updatesetting()
        self.close()

    def Onsetall(self):
        self.checkbox_spec0.setChecked(True)
        self.checkbox_spec6.setChecked(True)
        self.checkbox_sysbench.setChecked(True)
        self.argstemp["spec0cpu"] = "E"
        self.argstemp["spec6cpu"] = "E"
        self.argstemp["sysbenchcpu"] = "E"

# sysbench-cpu测试设置

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


# speccpu设置部分，待补
class SpeccpuSet(QDialog):

    pass
# HELP

class HelpSyscpu(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""sysbench cpu test 设置说明"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)


class HelpPerfcpu(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""Perfcpu 包含3种处理器运算性能的测试，分别为spec2000、spec2006、sysbench."""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

# test
#app = QApplication(sys.argv)
#form = PerfcpuSet()
#form.show()
#app.exec_()
