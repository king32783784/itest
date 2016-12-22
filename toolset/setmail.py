#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
import sys


class InputDialog(QDialog):

    def __init__(self, parent=None):
        super(InputDialog, self).__init__(parent)
        self.setWindowTitle(u"邮件订阅")
        self.resize(550,440)
        palette1 = QtGui.QPalette()
        palette1.setColor(self.backgroundRole(), QColor("#cccddc"))  # 设置背景色
        self.setPalette(palette1)
        self.setAutoFillBackground(True)
        self.argstemp = {}
        self.setFixedSize(self.width(), self.height())

        self.label_0 = QLabel(self.tr("定制邮件列表"))
        self.creatsetbox()
       # self.creatbutton()
        self.mailedit = TableDialog()
        self.mailedit.setEditTriggers(QAbstractItemView.NoEditTriggers)# 默认不可编辑
        self.mailedit.setHorizontalScrollBarPolicy(True) # 去掉水平滚动条
        self.mailedit.setShowGrid(True)
        self.readsetting()
        self.Layout()
        self.retranslateUi()

    def creatbutton(self):
        self.defaultbutton = QPushButton(u"默认")
        self.connect(self.defaultbutton, SIGNAL('clicked()'), self.ondefault)
        self.helpbutton = QPushButton(u"帮助")
        self.connect(self.helpbutton, SIGNAL('clicked()'), self.onhelp)
        self.setbutton = QPushButton(u"应用")
        self.connect(self.setbutton, SIGNAL('clicked()'), self.onset)

        
    def creatsetbox(self):
        self.check = QtGui.QCheckBox(u'启用邮件订阅功能')
        self.connect(self.check, QtCore.SIGNAL('clicked()'),
                     self.Oncheck)

    def Oncheck(self):
        if self.check.isChecked():
            self.mailedit.setEditTriggers(QAbstractItemView.CurrentChanged)
        else:
            self.mailedit.setEditTriggers(QAbstractItemView.NoEditTriggers)

 
    def updatesetting(self, mailadress):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.beginGroup("mailtotal")
        self.config.setValue("total", mailadress["total"])
        self.config.endGroup()
        self.config.beginGroup("maillist")
        for key, value in mailadress.iteritems():
            if key is not "total":
                self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.readset = QSettings(".testseting.ini", QSettings.IniFormat)
        totalmails = self.readset.value(QString("mailtotal/") + "total").toInt()[0]
        for i in range(totalmails):
            mail = self.readset.value(QString("maillist/") + "No%d"%i).toString()[0:]
            self.mailedit.setItem(i,0,QTableWidgetItem(self.tr(mail)))
        if self.readset.value(QString("mailstatus/") + "setting").toString()[0] == "E":
            self.check.setChecked(True)
            self.mailedit.setEditTriggers(QAbstractItemView.CurrentChanged)
        else:
            self.check.setChecked(False)

    def Layout(self):
        layout=QGridLayout()
        layout.addWidget(self.check, 0,0)
        layout.addWidget(self.label_0,1,0)
       # layout.addWidget(self.helpbutton, 11,0)
       # layout.addWidget(self.defaultbutton, 11,1)
       # layout.addWidget(self.setbutton, 11,10)
        layout.addWidget(self.mailedit, 2,0,6,12)
        self.setLayout(layout)


    def onset(self):
        maillists = {}
        total = 0
        for i in range(25):
            if self.mailedit.item(i,0):
                a = "No%s" % i
                maillists[a] = self.mailedit.item(i,0).text()
                total += 1
        maillists["total"] = total
        print maillists
        self.updatesetting(maillists)
        if self.check.isChecked():
            self.config = QSettings(".testseting.ini", QSettings.IniFormat)
            self.config.beginGroup("mailstatus")
            self.config.setValue("setting", "E")
            self.config.endGroup()
        else:
            self.config = QSettings(".testseting.ini", QSettings.IniFormat)
            self.config.beginGroup("mailstatus")
            self.config.setValue("setting", "D")
            self.config.endGroup()
#        self.close()

    def onhelp(self):
        helpdialog = HelpDialog()
        helpdialog.exec_()

   
    def ondefault(self):
        print "set default"
        self.mailedit.clear()
        self.check.setChecked(False)
        self.mailedit.setHorizontalHeaderLabels([u'邮箱地址'])
    
    def retranslateUi(self):
        file = QtCore.QFile('css.qss')
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = unicode(styleSheet, encoding='utf8')
        QtGui.qApp.setStyleSheet(styleSheet)

class TableDialog(QTableWidget):

    def __init__(self, parent=None):
        super(TableDialog, self).__init__(parent)

        self.setWindowTitle(u"订阅列表")
        self.resize(360,400)
        self.create_table()
        self.setHorizontalHeaderLabels([u'邮箱地址'])

    def create_table(self):
        self.setColumnCount(1)
        self.setColumnWidth(0,500)
        self.setRowCount(25)


# help窗口
class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super(HelpDialog,self).__init__(parent)
        self.setWindowTitle(self.tr(u"帮助"))
        self.resize(300,250)
        
        listWidget = QListWidget()
        listWidget.insertItem(0, self.tr(u"说明"))

        label1 = QLabel(self.tr(u"""启用该功能后，并且输入订阅邮箱地址。\n\n测试结束后会邮件寄送测试结果"""))

        stack = QStackedWidget()
        stack.addWidget(label1)

        mainLayout = QHBoxLayout(self)
        mainLayout.setMargin(5)
        mainLayout.setSpacing(5)
        mainLayout.addWidget(listWidget)
        mainLayout.addWidget(stack, 0, Qt.AlignHCenter)
        mainLayout.setStretchFactor(listWidget,1)
        mainLayout.setStretchFactor(stack,3)
        self.connect(listWidget,SIGNAL("currentRowChanged(int)"),stack,SLOT("setCurrentIndex(int)"))

# test
# app = QApplication(sys.argv)
# form = InputDialog()
# form.show()
# app.exec_()
