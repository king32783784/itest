#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os 
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog

class SetTool(QDialog):
    def __init__(self, parent=None):
        super(SetTool, self).__init__(parent)
        self.resize(30,440)
        self.setWindowTitle(u"工具来源")
        self.label_main = QLabel(self.tr(u"选择测试工具获取方式"))
        self.localradio = QtGui.QRadioButton(u"从本地地址获取")
        self.remoteradio = QtGui.QRadioButton(u"从远程地址获取")
        self.argstmp = {}
        self.setlocaldefault()
        self.localexpend()
        self.remotexpend()
        self.initstatus()
        self.lineEdit_name = QLineEdit()
        self.Layout()
        self.ConnectSignalSlot()
    
    def initstatus(self):
        status = self.readsetting()
        if status["status"] == "R":
            self.remoteradio.setChecked(True)
            self.remoteWidget.show()
        else:
            self.localradio.setChecked(True)
            self.localWidget.show()
               

    def localexpend(self):
        localdir = self.readsetting()["localdir"]
        self.label_localdir = QLabel(self.tr("当前路径:"))
        self.lineEdit_dir = QLineEdit(localdir)
        self.localWidget = QWidget()
        self.localWidget.hide()
 
    def remotexpend(self):
        remoteip = self.readsetting()["remoteip"]
        self.label_remote = QLabel(self.tr(u"远程地址:"))
        self.lineEdit_address = QLineEdit(remoteip)
        self.remoteWidget = QWidget()
        self.remoteWidget.hide()

    def Layout(self):
        baseLayout = QGridLayout()
        baseLayout.addWidget(self.label_main, 0, 0)
        baseLayout.addWidget(self.localradio, 1, 0)
        baseLayout.addWidget(self.remoteradio, 2, 0)

        localLayout = QGridLayout(self.localWidget)
        localLayout.addWidget(self.label_localdir, 0,0)
        localLayout.addWidget(self.lineEdit_dir, 0, 1,)
        
        remoteLayout = QGridLayout(self.remoteWidget)
        remoteLayout.addWidget(self.label_remote, 0,0)
        remoteLayout.addWidget(self.lineEdit_address, 0,1)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(baseLayout)
        mainLayout.addWidget(self.localWidget)
        mainLayout.addWidget(self.remoteWidget)
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.setSpacing(10)

        self.setLayout(mainLayout)

    def ConnectSignalSlot(self):
        self.connect(self.localradio, SIGNAL("clicked()"), self.localradiotest)
        self.connect(self.remoteradio, SIGNAL("clicked()"), self.remoteradiotest)

    def localradiotest(self):
        localdir = self.readsetting()
        if self.localradio.isChecked():
            self.localWidget.show()
            self.remoteWidget.hide()
            self.lineEdit_local = QLineEdit(localdir["localdir"])
        else:
            self.localWidget.hide()

    def remoteradiotest(self):
        remote = self.readsetting()
        if self.remoteradio.isChecked():
            self.remoteWidget.show()
            self.localWidget.hide()
            self.lineEdit_address = QLineEdit(remote["remoteip"])
        else:
            self.remoteWidget.hide()

    def setlocaldefault(self):
        gethome = os.getcwd()
        defaultlocaldir = os.path.join(gethome, "testtool")
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.beginGroup("testtool-default/")
        self.config.setValue("dir", defaultlocaldir)
        return defaultlocaldir

    def readsetting(self):
       self.config = QSettings(".testseting.ini", QSettings.IniFormat)
       testargs = {}
       testargs["localdir"] = self.config.value(QString("testtool-user/") + "dir").toString()[0:]
       testargs["remoteip"] = self.config.value(QString("testtool-user/") + "address").toString()[0:]
       testargs["status"] =  self.config.value(QString("testtool-user/") + "settoolstatus").toString()[0:]
       return testargs

    def updatesetting(self):
       self.config = QSettings(".testseting.ini", QSettings.IniFormat)
       self.config.beginGroup("testtool-user/")
       for key, value in self.argstmp.iteritems():
           self.config.setValue(key, value)
       self.config.endGroup()

    def onset(self):
       if self.remoteradio.isChecked():
           self.argstmp["settoolstatus"] = "R"
       else:
           self.argstmp["settoolstatus"] = "L"
       self.argstmp["dir"] = self.lineEdit_dir.text()
       self.argstmp["address"] = self.lineEdit_address.text() 
       self.updatesetting()

    def ondefault(self):
        self.remoteradio.setChecked(True)
        self.remoteWidget.show()
        self.localWidget.hide()
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
  
    def onhelp(self):
        helpdialog = SetToolhelp()
        helpdialog.exec_()
        

class SetToolhelp(HelpDialog):
        
    def additem(self):
        self.listWidget = QListWidget()
        self.listWidget.insertItem(0, self.tr(u"本地地址说明"))
        self.listWidget.insertItem(1, self.tr(u"远程地址说明"))

    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""激活本地地址获取选项后,\n\n用户需指定存放测试工具的本地路径如"/home",\n\n指定路径后,Lpbs-i会从指定路径查找测试工具"""))
        self.label2 = QLabel(self.tr(u"""激活远程地址获取选项后,\n\n用户需指定存放测试工具的远程地址,\n\n指定地址后,Lpbs-i会从指定远程地址下载测试工具到本地.\n\n注意,请确保网络连接正常."""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)
        self.stack.addWidget(self.label2)
    
#test   
#app = QApplication(sys.argv)
#main = SetTool()
#main.show()
#app.exec_()
    
