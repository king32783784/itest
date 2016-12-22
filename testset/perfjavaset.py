#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog

class PerfjavaSet(QDialog):

    def __init__(self, parent=None):
        super(PerfjavaSet, self).__init__(parent)
        self.setWindowTitle(u"Java")
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
        self.checkbox_specjvm = QtGui.QCheckBox(u'specjvm2008')
        self.connect(self.checkbox_specjvm, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_specjvm)

    def createbutton(self):
        self.specjvmsetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.specjvmsetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetspecjvm)
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
        baseLayout.addWidget(self.checkbox_specjvm, 0,0)

        baseLayout.addWidget(self.specjvmsetbutton, 0,3)
        
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
        testargs = self.readsetting("perfjava-user/")
        if testargs["specjvm"] == "E":
            self.checkbox_specjvm.setChecked(True)
   
    def readsetting(self, setmode):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        testargs = {}
        testargs["specjvm"] = self.config.value(QString(setmode) + "specjvm").toString()[0:]
        return testargs

    def updatesetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.beginGroup("perfjava-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def Oncheckbox_specjvm(self):
        if self.checkbox_specjvm.isChecked():
            self.argstemp["specjvm"] = "E"
        else:
            self.argstemp["specjvm"] = "D"

    def Onsetspecjvm(self):
        setspecjvm = SpecjvmSet()
        setspecjvm.exec_()

    def Ondefault(self):
        defaultset = self.readsetting("perfjava-default/")
        if defaultset["specjvm"] == "E":
            self.checkbox_specjvm.setChecked(True)
        else:
            self.checkbox_specjvm.setChecked(False)
        self.argstemp = defaultset

    def Onhelp(self):
        helpdialog = HelpPerfjava()
        helpdialog.exec_()
    
    def Onset(self):
        self.updatesetting()
        self.close()

    def Onsetall(self):
        self.checkbox_specjvm.setChecked(True)
        self.argstemp["specjvm"] = "E"

# specjvm测试设置

class SpecjvmSet(QDialog):
    
    def __init__(self, parent=None):
        super(SpecjvmSet, self).__init__(parent)
        self.setWindowTitle("Specjvm2008设置")
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
        self.threadlabel = QLabel(self.tr("参数t(次数)"))
        self.threadshow = QLabel("")
        self.threadshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)

    def createbutton(self):
        self.threadbutton = QPushButton(u"自定义")
        self.connect(self.threadbutton, QtCore.SIGNAL("clicked()"), self.Onthreadbutton)
        self.helpbutton = QPushButton(u"帮助")
        self.connect(self.helpbutton, QtCore.SIGNAL("clicked()"), self.Onhelpbutton)
        self.defaultbutton = QPushButton(u"默认")
        self.connect(self.defaultbutton, QtCore.SIGNAL("clicked()"), self.Ondefaultbutton)
        self.setbutton = QPushButton(u"确认")
        self.connect(self.setbutton, QtCore.SIGNAL("clicked()"), self.Onsetbutton)

    def Layout(self):
        baseLayout = QGridLayout()
        baseLayout.addWidget(self.threadlabel, 0,0)
        baseLayout.addWidget(self.threadshow, 0,1)
        
        baseLayout.addWidget(self.threadbutton, 0,3)

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
        self.threadshow.setText(str(testargs["argt"]))

    def updatesetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.beginGroup("specjvm-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        testargs = {}
        testargs["argt"] = self.config.value(QString("specjvm-user/") + "argt").toString()[0:]
        return testargs

    def Onthreadbutton(self):
        argt, ok = QInputDialog.getInteger(self, 
                                           self.tr(u'参数times'),
                                           self.tr(u"请输入参数次数：默认为3"),
                                           int(self.threadshow.text()),1,10)
        if ok:
            self.threadshow.setText(str(argt))
            self.argstemp['argt'] = str(argt)

    def Onhelpbutton(self):
        helpdialog = HelpSpecjvm()
        helpdialog.exec_()

    def Ondefaultbutton(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.argstemp["argt"] = self.config.value(QString("specjvm-default/") + "argt").toString()[0:]
        self.threadshow.setText(self.argstemp["argt"])

    def Onsetbutton(self):
        self.updatesetting()
        self.close()


# HELP

class HelpSpecjvm(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u""" unixbench test 设置说明"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

class HelpJava(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""系统基准测试目前只包含unixbench测试"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

# test
# app = QApplication(sys.argv)
# form = PerfjavaSet()
# form.show()
# app.exec_()
