#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os 
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog

class SetLogmode(QDialog):
    def __init__(self, parent=None):
        super(SetLogmode, self).__init__(parent)
        self.resize(30,440)
        self.setWindowTitle(u"日志窗口")
        self.argstmp = {}
        self.createcheckbox()
        self.initstatus()
        self.Layout()

    def createcheckbox(self):
        self.maincheck = QtGui.QCheckBox(u'启用日志窗口显示')
        self.connect(self.maincheck, QtCore.SIGNAL('clicked()'),
                     self.Oncheck)

    def initstatus(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        logmode = self.config.value(QString("logmode-user/") + "logmodestatus").toString()[0:]
        if logmode == "E":
            self.maincheck.setChecked(True)
        else:
            self.maincheck.setChecked(False)

    def Layout(self):
        baseLayout = QGridLayout()
        baseLayout.addWidget(self.maincheck,0,0)
        
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(baseLayout)
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.setSpacing(10)

        self.setLayout(mainLayout)

    def updatesetting(self):
       self.config = QSettings(".testseting.ini", QSettings.IniFormat)
       self.config.beginGroup("logmode-user/")
       for key, value in self.argstmp.iteritems():
           self.config.setValue(key, value)
       self.config.endGroup()

    def Oncheck(self):
        if self.maincheck.isChecked():
            self.argstmp["logmodestatus"] = "E"
        else:
            self.argstmp["logmodestatus"] = "D"

    def onset(self):
        self.updatesetting()

    def ondefault(self):
        self.maincheck.setChecked(True)
        self.argstmp["Logmodestatus"] = "E"
        
    def onhelp(self):
        helpdialog = Setreporthelp()
        helpdialog.exec_()
        

class Setreporthelp(HelpDialog):
        
    def additem(self):
        self.listWidget = QListWidget()
        self.listWidget.insertItem(0, self.tr(u"日志显示窗口"))

    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""激活日志显示窗口后,\n会出现一个窗口实时打印后台测试信息"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)
    
# test   
# app = QApplication(sys.argv)
# main = SetLogmode()
# main.show()
# app.exec_()
