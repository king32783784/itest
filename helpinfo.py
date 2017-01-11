#*-* coding=utf8 *-*
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
import sys

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super(HelpDialog,self).__init__(parent)
        self.setWindowTitle(self.tr(u"帮助"))
        self.resize(450,200)
    #    palette1 = QtGui.QPalette()
    #    palette1.setColor(self.backgroundRole(), QColor("#617a7c"))  # 设置背景色
    #    self.setPalette(palette1)
    #    self.setAutoFillBackground(True)

        self.additem()
        self.addlabel()
        self.setlayout()

    def additem(self):
        self.listWidget = QListWidget()
        self.listWidget.insertItem(0, self.tr(u"说明"))

    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""启用该功能后，并且输入订阅邮箱地址。\n\n测试结束后会邮件寄送测试结果"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

    def setlayout(self):
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setMargin(5)
        self.mainLayout.setSpacing(5)
        self.mainLayout.addWidget(self.listWidget)
        self.mainLayout.addWidget(self.stack, 0, Qt.AlignHCenter)
        self.mainLayout.setStretchFactor(self.listWidget,1)
        self.mainLayout.setStretchFactor(self.stack,3)
        self.connect(self.listWidget,SIGNAL("currentRowChanged(int)"),self.stack,SLOT("setCurrentIndex(int)"))
 #       self.mainLayout.setSizeConstraint(QLayout.SetFixedSize)
 #       self.mainLayout.setSpacing(10)
