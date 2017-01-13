#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog
from common import *

class Perf2dSet(QDialog):

    def __init__(self, parent=None):
        super(Perf2dSet, self).__init__(parent)
        self.setWindowTitle(u"2D")
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
        self.checkbox_x11perf = QtGui.QCheckBox(u'unixbench-x11perf')
        self.connect(self.checkbox_x11perf, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_x11perf)
        self.checkbox_qtperf = QtGui.QCheckBox(u'qtperf')
        self.connect(self.checkbox_qtperf, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_qtperf)

    def createbutton(self):
        self.x11perfsetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.x11perfsetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetx11perf)
        self.qtperfsetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.qtperfsetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetqtperf)
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
        baseLayout.addWidget(self.checkbox_x11perf, 0,0)
        baseLayout.addWidget(self.checkbox_qtperf, 1,0)

        baseLayout.addWidget(self.x11perfsetbutton, 0,3)
        baseLayout.addWidget(self.qtperfsetbutton, 1,3)
        
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
        testargs = self.readsetting("perf2d-user/")
        if testargs["x11perf"] == "E":
            self.checkbox_x11perf.setChecked(True)
        if testargs["qtperf"] == "E":
            self.checkbox_qtperf.setChecked(True)
   
    def readsetting(self, setmode):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["x11perf"] = self.config.value(QString(setmode) + "x11perf").toString()[0:]
        testargs["qtperf"] = self.config.value(QString(setmode) + "qtperf").toString()[0:]
        return testargs

    def updatesetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("perf2d-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def Oncheckbox_x11perf(self):
        if self.checkbox_x11perf.isChecked():
            self.argstemp["x11perf"] = "E"
        else:
            self.argstemp["x11perf"] = "D"

    def Oncheckbox_qtperf(self):
        if self.checkbox_qtperf.isChecked():
            self.argstemp["qtperf"] = "E"
        else:
            self.argstemp["qtperf"] = "D"

    def Onsetx11perf(self):
        setx11perf = X11perfSet()
        setx11perf.exec_()

    def Onsetqtperf(self):
        setqtperf = QtperfSet()
        setqtperf.exec_()
       
    def Ondefault(self):
        defaultset = self.readsetting("perf2d-default/")
        if defaultset["x11perf"] == "E":
            self.checkbox_x11perf.setChecked(True)
        else:
            self.checkbox_qtperf.setChecked(False)
        if defaultset["qtperf"] == "E":
            self.checkbox_qtperf.setChecked(True)
        else:
            self.checkbox_qtperf.setChecked(False)    
        self.argstemp = defaultset

    def Onhelp(self):
        helpdialog = HelpPerf2d()
        helpdialog.exec_()
    
    def Onset(self):
        self.updatesetting()
        self.close()

    def Onsetall(self):
        self.checkbox_x11perf.setChecked(True)
        self.checkbox_qtperf.setChecked(True)
        self.argstemp["x11perf"] = "E"
        self.argstemp["qtperf"] = "E"

# unixbench-x11perf测试设置

class X11perfSet(QDialog):
    
    def __init__(self, parent=None):
        super(X11perfSet, self).__init__(parent)
        self.setWindowTitle("x11perf设置")
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
        self.timeslabel = QLabel(self.tr("测试次数"))
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
        
        baseLayout.addWidget(self.timesbutton, 0,3)

        footer1Layout = QHBoxLayout()
        acer1 = QtGui.QSpacerItem(30,160)
        acer2 = QtGui.QSpacerItem(50,10)

        footer2Layout = QHBoxLayout()
        footer1Layout.addWidget(self.helpbutton)
        footer1Layout.addWidget(self.defaultbutton)
        baseLayout.addItem(acer1, 2,0)
        baseLayout.addItem(acer2, 3,1)
        footer2Layout.addWidget(self.setbutton)

       # baseLayout.setSizeConstraint(QLayout.SetFixedSize)
       # baseLayout.setSpacing(10)
        baseLayout.addLayout(footer1Layout,3,0)
        baseLayout.addLayout(footer2Layout,3,3)
        self.setLayout(baseLayout)

    def initstatus(self):
        testargs = self.readsetting()
        self.timesshow.setText(str(testargs["argt"]))

    def updatesetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("x11perf-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["argt"] = self.config.value(QString("x11perf-user/") + "argt").toInt()[0]
        return testargs

    def Ontimesbutton(self):
        argt, ok = QInputDialog.getInteger(self, 
                                           self.tr(u'测试测试'),
                                           self.tr(u"请输入测试次数"),
                                           int(self.timesshow.text()),1,10)
        if ok:
            self.timesshow.setText(str(argt))
            self.argstemp['argt'] = str(argt)

    def Onhelpbutton(self):
        helpdialog = HelpX11perf()
        helpdialog.exec_()

    def Ondefaultbutton(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.argstemp["argt"] = self.config.value(QString("x11perf-default/") + "argt").toInt()[0]
        self.timesshow.setText(self.argstemp["argt"])

    def Onsetbutton(self):
        self.updatesetting()
        self.close()


# qtperf设置
class QtperfSet(QDialog):

    def __init__(self, parent=None):
        super(QtperfSet, self).__init__(parent)
        self.setWindowTitle("Qtperf设置")
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

        baseLayout.addWidget(self.timesbutton, 0,3)

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
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("qtperf-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["args"] = self.config.value(QString("qtperf-user/") + "args").toInt()[0]
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
        helpdialog = HelpX11perf()
        helpdialog.exec_()

    def Ondefaultbutton(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.argstemp["args"] = self.config.value(QString("qtperf-default/") + "args").toInt()[0]
        self.timesshow.setText(str(self.argstemp["args"]))

    def Onsetbutton(self):
        self.updatesetting()
        self.close()


# HELP

class HelpX11perf(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""sysbench mem test 设置说明"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

class HelpQtperf(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""stream test 设置说明"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

class HelpPerf2d(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""Perfmem 包含2种内存性能的测试，分别为stream、sysbench."""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

# test
# app = QApplication(sys.argv)
# form = Perf2dSet()
# form.show()
# app.exec_()
