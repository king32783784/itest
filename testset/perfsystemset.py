#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog

class PerfsystemSet(QDialog):

    def __init__(self, parent=None):
        super(PerfsystemSet, self).__init__(parent)
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
        self.checkbox_unixbench = QtGui.QCheckBox(u'unixbench')
        self.connect(self.checkbox_unixbench, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_unixbench)

    def createbutton(self):
        self.unixbenchsetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.unixbenchsetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetunixbench)
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
        baseLayout.addWidget(self.checkbox_unixbench, 0,0)

        baseLayout.addWidget(self.unixbenchsetbutton, 0,3)
        
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
        testargs = self.readsetting("perfsystem-user/")
        if testargs["unixbench"] == "E":
            self.checkbox_unixbench.setChecked(True)
   
    def readsetting(self, setmode):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        testargs = {}
        testargs["unixbench"] = self.config.value(QString(setmode) + "unixbench").toString()[0:]
        return testargs

    def updatesetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.beginGroup("perfsystem-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def Oncheckbox_unixbench(self):
        if self.checkbox_system.isChecked():
            self.argstemp["unixbench"] = "E"
        else:
            self.argstemp["unixbench"] = "D"

    def Onsetunixbench(self):
        setunixbench = UnixbenchSet()
        setunixbench.exec_()

    def Ondefault(self):
        defaultset = self.readsetting("perfsystem-default/")
        if defaultset["unixbench"] == "E":
            self.checkbox_unixbench.setChecked(True)
        else:
            self.checkbox_unixbench.setChecked(False)
        self.argstemp = defaultset

    def Onhelp(self):
        helpdialog = HelpPerfsystem()
        helpdialog.exec_()
    
    def Onset(self):
        self.updatesetting()
        self.close()

    def Onsetall(self):
        self.checkbox_unixbench.setChecked(True)
        self.argstemp["unixbench"] = "E"

# unixbench测试设置

class UnixbenchSet(QDialog):
    
    def __init__(self, parent=None):
        super(UnixbenchSet, self).__init__(parent)
        self.setWindowTitle("unixbench设置")
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
        self.timeslabel = QLabel(self.tr("参数次数"))
        self.timesshow = QLabel("")
        self.timesshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)

    def createbutton(self):
        self.threadbutton = QPushButton(u"自定义")
        self.connect(self.threadbutton, QtCore.SIGNAL("clicked()"), self.Onthreadbutton)
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
        baseLayout.addWidget(self.threadlabel, 0,0)
        baseLayout.addWidget(self.timeslabel, 1,0)
        baseLayout.addWidget(self.threadshow, 0,1)
        baseLayout.addWidget(self.timesshow, 1,1)
        
        baseLayout.addWidget(self.threadbutton, 0,3)
        baseLayout.addWidget(self.timesbutton, 1,3)

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
        self.timesshow.setText(str(testargs["args"]))

    def updatesetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.beginGroup("unixbench-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        testargs = {}
        testargs["argt"] = self.config.value(QString("unixbench-user/") + "argt").toString()[0:]
        testargs["args"] = self.config.value(QString("unixbench-user/") + "args").toInt()[0]
        return testargs

    def Onthreadbutton(self):
        list_argt = QStringList()
        list_argt.append(self.tr("1"))
        list_argt.append(self.tr("1,4"))
        list_argt.append(self.tr("1,4,8"))
        argt, ok = QInputDialog.getItem(self, self.tr(u'参数thread'),
                                        self.tr(u"请输入参数thread的值:以,分隔"),
                                        list_argt)
        if ok:
            self.threadshow.setText(argt)
            self.argstemp['argt'] = str(argt)

    def Ontimesbutton(self):
        args, ok = QInputDialog.getInteger(self, 
                                           self.tr(u'参数times'),
                                           self.tr(u"请输入参数次数：默认为3"),
                                           int(self.timesshow.text()),1,10)
        if ok:
            self.timesshow.setText(str(args))
            self.argstemp['args'] = str(args)

    def Onhelpbutton(self):
        helpdialog = HelpSystem()
        helpdialog.exec_()

    def Ondefaultbutton(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.argstemp["argt"] = self.config.value(QString("unixbench-default/") + "argt").toString()[0:]
        self.argstemp["args"] = self.config.value(QString("unixbench-default/") + "args").toInt()[0]
        self.threadshow.setText(self.argstemp["argt"])
        self.timesshow.setText(str(self.argstemp["args"]))

    def Onsetbutton(self):
        self.updatesetting()
        self.close()


# HELP

class HelpUnixbench(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u""" unixbench test 设置说明"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

class HelpSystem(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""系统基准测试目前只包含unixbench测试"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

# test
# app = QApplication(sys.argv)
# form = PerfsystemSet()
# form.show()
# app.exec_()
