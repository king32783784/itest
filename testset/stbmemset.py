#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog
from common import *

class StbmemSet(QDialog):

    def __init__(self, parent=None):
        super(StbmemSet, self).__init__(parent)
        self.setWindowTitle(u"MEM稳定性")
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
        self.checkbox_stressappmem = QtGui.QCheckBox(u'stressapptest')
        self.connect(self.checkbox_stressappmem, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_stressappmem)

    def createbutton(self):
        self.stressappmemsetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.stressappmemsetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetstressappmem)
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
        baseLayout.addWidget(self.checkbox_stressappmem, 0,0)

        baseLayout.addWidget(self.stressappmemsetbutton, 0,3)
        
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
        testargs = self.readsetting("stressmem-user/")
        if testargs["stressappmem"] == "E":
            self.checkbox_stressappmem.setChecked(True)
   
    def readsetting(self, setmode):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["stressappmem"] = self.config.value(QString(setmode)
                                   + "stressappmem").toString()[0:]
        return testargs

    def updatesetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("stressmem-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def Oncheckbox_stressappmem(self):
        if self.checkbox_stressappmem.isChecked():
            self.argstemp["stressappmem"] = "E"
        else:
            self.argstemp["stressappmem"] = "D"

    def Onsetstressappmem(self):
        setstressappmem = StressappmemSet()
        setstressappmem.exec_()
       
    def Ondefault(self):
        defaultset = self.readsetting("stressmem-default/")
        if defaultset["stressappmem"] == "E":
            self.checkbox_stressappmem.setChecked(True)
        else:
            self.checkbox_stressappmem.setChecked(False)    
        self.argstemp = defaultset

    def Onhelp(self):
        helpdialog = HelpPerfcpu()
        helpdialog.exec_()
    
    def Onset(self):
        self.updatesetting()
        self.close()

    def Onsetall(self):
        self.checkbox_stressappmem.setChecked(True)
        self.argstemp["stressappmem"] = "E"

# stressapp-cpu测试设置

class StressappmemSet(QDialog):
    
    def __init__(self, parent=None):
        super(StressappmemSet, self).__init__(parent)
        self.setWindowTitle("stressapptest设置")
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
        self.memlabel = QLabel(self.tr("内存负载(%)"))
        self.memshow = QLabel("10")
        self.memshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)

    def createbutton(self):
        self.timebutton = QPushButton(u"自定义")
        self.connect(self.timebutton, QtCore.SIGNAL("clicked()"), self.Ontimebutton)
        self.membutton = QPushButton(u"自定义")
        self.connect(self.membutton, QtCore.SIGNAL("clicked()"), self.Onmembutton)
        self.helpbutton = QPushButton(u"帮助")
        self.connect(self.helpbutton, QtCore.SIGNAL("clicked()"), self.Onhelpbutton)
        self.defaultbutton = QPushButton(u"默认")
        self.connect(self.defaultbutton, QtCore.SIGNAL("clicked()"), self.Ondefaultbutton)
        self.setbutton = QPushButton(u"确认")
        self.connect(self.setbutton, QtCore.SIGNAL("clicked()"), self.Onsetbutton)

    def Layout(self):
        baseLayout = QGridLayout()
        baseLayout.addWidget(self.timelabel, 0,0)
        baseLayout.addWidget(self.memlabel, 1,0)
        baseLayout.addWidget(self.timeshow, 0,1)
        baseLayout.addWidget(self.memshow, 1,1)
        
        baseLayout.addWidget(self.timebutton, 0,3)
        baseLayout.addWidget(self.membutton, 1,3)

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
        self.timeshow.setText(str(testargs["argt"]))
        self.memshow.setText(str(testargs["argl"]))

    def updatesetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("stressappmem-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["argt"] = self.config.value(QString("stressappmem-user/") + "argt").toInt()[0]
        testargs["argl"] = self.config.value(QString("stressappmem-user/") + "argl").toInt()[0]
        return testargs

    def Ontimebutton(self):
        argt, ok = QInputDialog.getInteger(self,
                                           self.tr(u"测试时间"),
                                           self.tr(u"请输入测试小时数:"),
                                           int(self.timeshow.text()), 1, 168)
        if ok:
            self.timeshow.setText(str(argt))
            self.argstemp['argt'] = str(argt)

    def Onmembutton(self):
        argl, ok = QInputDialog.getInteger(self, 
                                        self.tr(u'内存负载'),
                                        self.tr(u"请输入内存负载百分比:"),
                                        int(self.memshow.text()), 1, 90)
        if ok:
            self.memshow.setText(str(argl))
            self.argstemp['argl'] = str(argl)

    def Onhelpbutton(self):
        helpdialog = HelpSyscpu()
        helpdialog.exec_()

    def Ondefaultbutton(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.argstemp["argt"] = self.config.value(QString("stressappmem-default/") + "argt").toInt()[0]
        self.argstemp["argl"] = self.config.value(QString("stressappmem-default/") + "argl").toInt()[0]
        self.timeshow.setText(str(self.argstemp["argt"]))
        self.memshow.setText(str(self.argstemp["argl"]))

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
