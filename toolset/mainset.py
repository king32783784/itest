#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore

from setmail import *
from settool import *
from setreport import *
from setlogmode import *


class StackDialog(QDialog):
    def __init__(self, parent=None):
        super(StackDialog,self).__init__(parent)
        self.labelindex = 0
        self.setWindowTitle(self.tr(u"基础设置"))
        self.resize(680,550)
        self.setFixedSize(self.width(), self.height())
        self.CreateStackDialog()
        self.Layout()
        self.ConcentSignalSlot()

    def CreateStackDialog(self):
        self.mainSplitter = QSplitter(Qt.Horizontal)
        self.mainSplitter.setOpaqueResize(True)

        self.listWidget = QListWidget(self.mainSplitter)
        self.listWidget.insertItem(1, self.tr(u"邮件订阅"))
        self.listWidget.insertItem(0, self.tr(u"工具来源"))
        self.listWidget.insertItem(2, self.tr(u"报告设置"))
        self.listWidget.insertItem(3, self.tr(u"日志显示"))

        self.frame = QFrame(self.mainSplitter)
        self.stack = QStackedWidget()
        self.stack.setFrameStyle(QFrame.Panel|QFrame.Raised)
 
        self.form = InputDialog() # 生成setmail对象
        self.settool = SetTool()  # 生成settoll对象
        self.setreport = SetReport() # 生成setreport对象
        self.setlog = SetLogmode() 
        self.stack.addWidget(self.settool)
        self.stack.addWidget(self.form)
        self.stack.addWidget(self.setreport)
        self.stack.addWidget(self.setlog)

        self.setbutton = QPushButton(self.tr(u"修改"))
        self.defaultbutton = QPushButton(self.tr(u"默认"))
        self.helpbutton = QPushButton(self.tr(u"帮助"))
        self.closebutton = QPushButton(self.tr(u"关闭"))
        self.connect(self.setbutton, QtCore.SIGNAL("clicked()"), self.onset)
        self.connect(self.closebutton, QtCore.SIGNAL("clicked()"), self.close)        
        self.connect(self.helpbutton, QtCore.SIGNAL("clicked()"), self.onhelp)   
        self.connect(self.defaultbutton, QtCore.SIGNAL("clicked()"), self.ondefault)

    def Layout(self):
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(3)
        buttonLayout.addWidget(self.helpbutton)
        buttonLayout.addWidget(self.defaultbutton)
        buttonLayout.addWidget(self.setbutton)
        buttonLayout.addWidget(self.closebutton)

        mainLayout = QVBoxLayout(self.frame)
        mainLayout.setMargin(8)
        mainLayout.setSpacing(16)
        mainLayout.addWidget(self.stack)
        mainLayout.addLayout(buttonLayout)

        layout = QHBoxLayout(self)
        layout.addWidget(self.mainSplitter)
        self.setLayout(layout)

    def ConcentSignalSlot(self):
        self.connect(self.listWidget, SIGNAL("currentRowChanged(int)"), self.setCurrentIndex)
 
    def setCurrentIndex(self,index):
        self.stack.setCurrentIndex(index)
        self.labelindex = index
        print self.labelindex

    def onset(self):
        if self.labelindex == 0:
            print("set no0")
            self.settool.onset()
        elif self.labelindex == 1:
            print("set no1")
            self.form.onset()
        elif self.labelindex == 2:
            print("set no2")
            self.setreport.onset()
        elif self.labelindex == 3:
            print("set no3")
            self.setlog.onset()
        else:
            pass
        
    def onhelp(self):
        if self.labelindex == 0:
            print("set no0")
            self.settool.onhelp()
        elif self.labelindex == 1:
            print("set no1")
            self.form.onhelp()
        elif self.labelindex == 2:
            print("set no2")
            self.setreport.onhelp()
        elif self.labelindex == 3:
            print("set no3")
            self.setlog.onhelp()
        else:
            pass

    def ondefault(self):
        if self.labelindex == 0:
            self.settool.ondefault()
        elif self.labelindex == 1:
            self.form.ondefault()
        elif self.labelindex == 2:
            print("set no 2")
            self.setreport.ondefault()
        elif self.labelindex == 3:
            print("set no 3")
            self.setlog.ondefault()
        else:
            pass

# test
# app = QApplication(sys.argv)
# main = StackDialog()
# main.show()
# app.exec_()
