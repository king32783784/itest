#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os 
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog

class SetReport(QDialog):
    def __init__(self, parent=None):
        super(SetReport, self).__init__(parent)
        self.resize(30,440)
        self.setWindowTitle(u"报告设置")
        self.argstmp = {}
        self.createlabels()
        self.createcheckbox()
        self.reportexpend()
        self.initstatus()
        self.Layout()

    def createlabels(self):
        self.xlslabel = QtGui.QLabel(u'制作表格版测试报告"') 
        self.htmllabel = QtGui.QLabel(u'制作网页版测试报告"')
 
    def createcheckbox(self):
        self.maincheck = QtGui.QCheckBox(u'启用自动制作报告功能')
        self.connect(self.maincheck, QtCore.SIGNAL('clicked()'),
                     self.Oncheck)
        self.htmlcheck = QtGui.QCheckBox(u'')
        self.connect(self.htmlcheck, QtCore.SIGNAL('clicked()'),
                     self.Onhtml)
        self.xlscheck = QtGui.QCheckBox(u'')
        self.connect(self.xlscheck, QtCore.SIGNAL('clicked()'),
                     self.Onxls)

    def initstatus(self):
        status = self.readsetting()
        self.initreportmode = status
        if status["reportstatus"] == "E":
            self.maincheck.setChecked(True)
            self.showreport()          
        else:
            self.maincheck.setChecked(False)
            self.reportWidget.hide()

    def reportexpend(self):
        self.htmllabel = QtGui.QLabel(u'制作网页版测试报告:')
        self.xlslabel = QtGui.QLabel(u'制作表格版测试报告:')
        self.reportWidget = QWidget()
 
    def showreport(self):
        self.reportWidget.show()
        status = self.readsetting()
        if status["xlsstatus"] == "E":
            self.xlscheck.setChecked(True)
        else:
            self.xlscheck.setChecked(False)
        if status["htmlstatus"] == "E":
            self.htmlcheck.setChecked(True)
        else:
            self.htmlcheck.setChecked(False)

    def Layout(self):
        baseLayout = QGridLayout()
        baseLayout.addWidget(self.maincheck,0,0)
        
        # 伸缩框
        reportLayout = QGridLayout(self.reportWidget)
        reportLayout.addWidget(self.htmllabel, 0,0)
        reportLayout.addWidget(self.xlslabel, 1, 0,)
        reportLayout.addWidget(self.htmlcheck, 0,1)
        reportLayout.addWidget(self.xlscheck, 1,1)
        
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(baseLayout)
        mainLayout.addWidget(self.reportWidget)
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.setSpacing(10)

        self.setLayout(mainLayout)

    def Onhtml(self):
        pass

    def Onxls(self):
        pass  

    def readsetting(self):
       self.config = QSettings(".testseting.ini", QSettings.IniFormat)
       testargs = {}
       testargs["reportstatus"] = self.config.value(QString("testreport-user/") + "reportstatus").toString()[0:]
       testargs["htmlstatus"] = self.config.value(QString("testreport-user/") + "htmlstatus").toString()[0:]
       testargs["xlsstatus"] =  self.config.value(QString("testreport-user/") + "xlsstatus").toString()[0:]
       return testargs

    def updatesetting(self):
       self.config = QSettings(".testseting.ini", QSettings.IniFormat)
       self.config.beginGroup("testreport-user/")
       for key, value in self.argstmp.iteritems():
           self.config.setValue(key, value)
       self.config.endGroup()

    def Oncheck(self):
        if self.maincheck.isChecked():
            self.showreport()
            self.argstmp["reportstatus"] = "E"
        else:
            self.reportWidget.hide()
            self.argstmp["reportstatus"] = "D"

    def readcheckstatus(self):
        if self.htmlcheck.isChecked():
            self.argstmp["htmlstatus"] = "E"
        else:
            self.argstmp["htmlstatus"] = "D"
        if self.xlscheck.isChecked():
            self.argstmp["xlsstatus"] = "E"
        else:
            self.argstmp["xlsstatus"] = "D"

    def onset(self):
        self.readcheckstatus()
        if self.maincheck.isChecked():
            if self.argstmp["htmlstatus"] == "E" or self.argstmp["xlsstatus"] == "E":
                self.argstmp["reportstatus"] = "E"
                self.updatesetting()
            else:
                r = QtGui.QMessageBox.warning(self,"PyQT",u'至少选择一种报告格式')
        else:
            self.initreportmode["reportstatus"] = "D"
            self.argstmp = self.initreportmode
            self.updatesetting()

    def ondefault(self):
        self.maincheck.setChecked(False)
        self.reportWidget.hide()
        self.initreportmode["htmlstatus"] = "E"
        self.initreportmode["xlsstatus"] = "E"
        self.argstmp["reportstatus"] = "D"
  
    def onhelp(self):
        helpdialog = Setreporthelp()
        helpdialog.show()
        helpdialog.exec_()
        

class Setreporthelp(HelpDialog):
        
    def additem(self):
        self.listWidget = QListWidget()
        self.listWidget.insertItem(0, self.tr(u"自动生成报告"))

    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""激活自动生成报告功能后\n用户可以选择报告的格式."""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)
    
# test   
# app = QApplication(sys.argv)
# main = SetReport()
# main.show()
# app.exec_()
