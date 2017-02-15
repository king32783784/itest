#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog
from common import *

class StbthreadSet(QDialog):

    def __init__(self, parent=None):
        super(StbthreadSet, self).__init__(parent)
        self.setWindowTitle(u"多线程稳定性")
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
        self.checkbox_thread = QtGui.QCheckBox(u'stress')
        self.connect(self.checkbox_thread, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_thread)

    def createbutton(self):
        self.threadsetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.threadsetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetthread)
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
        baseLayout.addWidget(self.checkbox_thread, 0,0)

        baseLayout.addWidget(self.threadsetbutton, 0,3)
        
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
        testargs = self.readsetting("stressthread-user/")
        if testargs["stress"] == "E":
            self.checkbox_thread.setChecked(True)
   
    def readsetting(self, setmode):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["stress"] = self.config.value(QString(setmode)
                                   + "stress").toString()[0:]
        return testargs

    def updatesetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("stressthread-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def Oncheckbox_thread(self):
        if self.checkbox_thread.isChecked():
            self.argstemp["stress"] = "E"
        else:
            self.argstemp["stress"] = "D"

    def Onsetthread(self):
        setstressthread = StressthreadSet()
        setstressthread.exec_()
       
    def Ondefault(self):
        defaultset = self.readsetting("stressthread-default/")
        if defaultset["stress"] == "E":
            self.checkbox_stressthread.setChecked(True)
        else:
            self.checkbox_stressthread.setChecked(False)    
        self.argstemp = defaultset

    def Onhelp(self):
        helpdialog = HelpPerfcpu()
        helpdialog.exec_()
    
    def Onset(self):
        self.updatesetting()
        self.close()

    def Onsetall(self):
        self.checkbox_stressthread.setChecked(True)
        self.argstemp["stress"] = "E"

# stressapp-cpu测试设置

class StressthreadSet(QDialog):
    
    def __init__(self, parent=None):
        super(StressthreadSet, self).__init__(parent)
        self.setWindowTitle("stress设置")
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
        self.timelabel = QLabel(self.tr("测试时间(hours)"))
        self.timeshow = QLabel("1")
        self.timeshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.threadlabel = QLabel(self.tr("线程数量(threads)"))
        self.threadshow = QLabel("12")
        self.threadshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)

    def createbutton(self):
        self.timebutton = QPushButton(u"自定义")
        self.connect(self.timebutton, QtCore.SIGNAL("clicked()"), self.Ontimebutton)
        self.threadbutton = QPushButton(u"自定义")
        self.connect(self.threadbutton, QtCore.SIGNAL("clicked()"), self.Onmembutton)
        self.helpbutton = QPushButton(u"帮助")
        self.connect(self.helpbutton, QtCore.SIGNAL("clicked()"), self.Onhelpbutton)
        self.defaultbutton = QPushButton(u"默认")
        self.connect(self.defaultbutton, QtCore.SIGNAL("clicked()"), self.Ondefaultbutton)
        self.setbutton = QPushButton(u"确认")
        self.connect(self.setbutton, QtCore.SIGNAL("clicked()"), self.Onsetbutton)

    def Layout(self):
        baseLayout = QGridLayout()
        baseLayout.addWidget(self.timelabel, 0,0)
        baseLayout.addWidget(self.threadlabel, 1,0)
        baseLayout.addWidget(self.timeshow, 0,1)
        baseLayout.addWidget(self.threadshow, 1,1)
        
        baseLayout.addWidget(self.timebutton, 0,3)
        baseLayout.addWidget(self.threadbutton, 1,3)

        footer1Layout = QHBoxLayout()
        acer1 = QtGui.QSpacerItem(30,240)
        acer2 = QtGui.QSpacerItem(50,10)

        footer2Layout = QHBoxLayout()
        footer1Layout.addWidget(self.helpbutton)
        footer1Layout.addWidget(self.defaultbutton)
        baseLayout.addItem(acer1, 3,0)
        baseLayout.addItem(acer2, 4,1)
        footer2Layout.addWidget(self.setbutton)

        baseLayout.addLayout(footer1Layout,4,0)
        baseLayout.addLayout(footer2Layout,4,3)
        self.setLayout(baseLayout)

    def initstatus(self):
        testargs = self.readsetting()
        self.timeshow.setText(str(testargs["args"]))
        self.threadshow.setText(str(testargs["argt"]))

    def updatesetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("stress-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["args"] = self.config.value(QString("stress-user/") + "args").toInt()[0]
        testargs["argt"] = self.config.value(QString("stress-user/") + "argt").toInt()[0]
        return testargs

    def Ontimebutton(self):
        args, ok = QInputDialog.getInteger(self,
                                           self.tr(u"测试时间"),
                                           self.tr(u"请输入测试小时数:"),
                                           int(self.timeshow.text()), 1, 168)
        if ok:
            self.timeshow.setText(str(args))
            self.argstemp['args'] = str(args)

    def Onmembutton(self):
        argt, ok = QInputDialog.getInteger(self, 
                                        self.tr(u'线程数量'),
                                        self.tr(u"请输入线程数量（4的倍数）:"),
                                        int(self.threadshow.text()), 4, 128)
        if ok:
            self.threadshow.setText(str(argt))
            self.argstemp['argt'] = str(argt)

    def Onhelpbutton(self):
        helpdialog = HelpSyscpu()
        helpdialog.exec_()

    def Ondefaultbutton(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.argstemp["args"] = self.config.value(QString("stress-default/") + "args").toInt()[0]
        self.argstemp["argt"] = self.config.value(QString("stress-default/") + "argt").toInt()[0]
        self.timeshow.setText(str(self.argstemp["args"]))
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
