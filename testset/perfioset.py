#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog
from common import *

class PerfioSet(QDialog):

    def __init__(self, parent=None):
        super(PerfioSet, self).__init__(parent)
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
        self.checkbox_iozone = QtGui.QCheckBox(u'iozone')
        self.connect(self.checkbox_iozone, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_iozone)

    def createbutton(self):
        self.iozonesetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.iozonesetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetiozone)
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
        baseLayout.addWidget(self.checkbox_iozone, 0,0)

        baseLayout.addWidget(self.iozonesetbutton, 0,3)
        
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
        testargs = self.readsetting("perfio-user/")
        if testargs["iozone"] == "E":
            self.checkbox_iozone.setChecked(True)
   
    def readsetting(self, setmode):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["iozone"] = self.config.value(QString(setmode) + "iozone").toString()[0:]
        return testargs

    def updatesetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("perfio-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def Oncheckbox_iozone(self):
        if self.checkbox_iozone.isChecked():
            self.argstemp["iozone"] = "E"
        else:
            self.argstemp["iozone"] = "D"

    def Onsetiozone(self):
        iozone = IozoneSet()
        iozone.exec_()

    def Ondefault(self):
        defaultset = self.readsetting("perfio-default/")
        if defaultset["iozone"] == "E":
            self.checkbox_iozone.setChecked(True)
        else:
            self.checkbox_iozone.setChecked(False)
        self.argstemp = defaultset

    def Onhelp(self):
        helpdialog = HelpPerfio()
        helpdialog.exec_()
    
    def Onset(self):
        self.updatesetting()
        self.close()

    def Onsetall(self):
        self.checkbox_iozone.setChecked(True)
        self.argstemp["iozone"] = "E"

# iozone设置
class IozoneSet(QDialog):

    def __init__(self, parent=None):
        super(IozoneSet, self).__init__(parent)
        self.setWindowTitle("Iozone")
        self.resize(450,550)
        palette1 = QtGui.QPalette()
        palette1.setColor(self.backgroundRole(), QColor("#cccddc"))  # 设置背景色
        self.setPalette(palette1)
        self.setAutoFillBackground(True)
        self.argstemp = {}

        self.label_0 = QLabel(self.tr(u"参数s(GB)"))
        self.label_1 = QLabel(self.tr(u"参数i(Mode)"))
        self.label_2 = QLabel(self.tr(u"参数t(Threads)"))
        self.label_3 = QLabel(self.tr(u"参数r(Mb)"))
        self.label_4 = QLabel(self.tr(u"参数次数(times)"))

        self.setargsprint()
        self.btn_args = QPushButton(u"自定义")
        self.btn_argi = QPushButton(u"自定义")
        self.btn_argt = QPushButton(u"自定义")
        self.btn_argr = QPushButton(u"自定义")
        self.btn_argtime = QPushButton(u"自定义")

        self.defaultbutton = QPushButton(u"默认")
        self.helpbutton = QPushButton(u"帮助")
        self.setbutton = QPushButton(u"应用")

        self.Layout()
        self.ConnectSignalSlot()
 #       self.writesetting()
 #       self.retranslateUi()

    def setargsprint(self):
        printargs = self.readsetting("iozone-user/")
        self.label_args_0 = QLabel("%d" % printargs["args"])
        self.label_args_0.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.label_argi_0 = QLabel(printargs["argi"])
        self.label_argi_0.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.label_argt_0 = QLabel("%d" % printargs["argt"])
        self.label_argt_0.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.label_argr_0 = QLabel("%d" % printargs["argr"])
        self.label_argr_0.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.label_argtime = QLabel("%s" % printargs["times"])
        self.label_argtime.setFrameStyle(QFrame.Panel|QFrame.Sunken)

    def updatesetting(self, argstmp):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("iozone-user")
        for key, value in argstmp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self, argstype):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["args"] = (self.config.value(QString(argstype) + "args").toInt()[0])
        testargs["argi"] = (self.config.value(QString(argstype) + "argi").toString()[0:])
        testargs["argt"] = (self.config.value(QString(argstype) + "argt").toInt()[0])
        testargs["argr"] = (self.config.value(QString(argstype) + "argr").toInt()[0])
        testargs["times"] = (self.config.value(QString(argstype) + "times").toInt()[0])
        return testargs

    def Layout(self):
        layout=QGridLayout()
        layout.addWidget(self.label_0, 0, 0)
        layout.addWidget(self.label_args_0, 0, 1)
        layout.addWidget(self.btn_args, 0, 5)
        layout.addWidget(self.label_1, 1, 0)
        layout.addWidget(self.label_argi_0, 1, 1)
        layout.addWidget(self.btn_argi, 1, 5)
        layout.addWidget(self.label_2, 2, 0)
        layout.addWidget(self.label_argt_0, 2, 1)
        layout.addWidget(self.btn_argt, 2, 5)
        layout.addWidget(self.label_3, 3, 0)
        layout.addWidget(self.label_argr_0, 3, 1)
        layout.addWidget(self.btn_argr, 3, 5)
        layout.addWidget(self.label_4, 4,0)
        layout.addWidget(self.btn_argtime, 4,5)
        layout.addWidget(self.label_argtime, 4,1)
        layout.addWidget(self.helpbutton, 5,0)
        layout.addWidget(self.defaultbutton, 5,1)
        layout.addWidget(self.setbutton, 5,6)
        self.setLayout(layout)

    def ConnectSignalSlot(self):
        self.connect(self.btn_args, SIGNAL("clicked()"), self.slotargs)
        self.connect(self.btn_argi, SIGNAL("clicked()"), self.slotargi)
        self.connect(self.btn_argt, SIGNAL("clicked()"), self.slotargt)
        self.connect(self.btn_argr, SIGNAL("clicked()"), self.slotargr)
        self.connect(self.btn_argtime, SIGNAL("clicked()"), self.slotargtime)
        self.connect(self.setbutton, SIGNAL("clicked()"), self.slotset)
        self.connect(self.defaultbutton, SIGNAL("clicked()"), self.slotdefault)
        self.connect(self.helpbutton, SIGNAL("clicked()"), self.slothelp)

    def slotargs(self):
        args,ok = QInputDialog.getInteger(self,
                                          self.tr(u"参数s"),
                                          self.tr(u"请输入参数s的值:"),
                                          int(self.label_args_0.text()), 1, 256)
        if ok:
            self.label_args_0.setText(str(args))
            self.argstemp['args'] = str(args)

    def slotargi(self):
        list_argi = QStringList()
        list_argi.append(self.tr("0"))
        list_argi.append(self.tr("0,1"))
        list_argi.append(self.tr("0,1,2"))
        argi,ok = QInputDialog.getItem(self,self.tr(u"参数i"),
                                      self.tr(u"请输入参数i的值:仅支持0,1,2"),
                                      list_argi)
        if ok:
            self.label_argi_0.setText(argi)
            self.argstemp['argi'] = str(argi)

    def slotargt(self):
        argt,ok = QInputDialog.getInteger(self,
                                         self.tr(u"参数t"),
                                         self.tr(u"请输入参数t的值:"),
                                         int(self.label_argt_0.text()), 1, 1024)
        if ok:
            self.label_argt_0.setText(str(argt))
            self.argstemp['argt'] = str(argt)

    def slotargr(self):
        argr,ok = QInputDialog.getInteger(self,
                                            self.tr(u"参数r"),
                                            self.tr(u"请输入r的值:"),
                                            int(self.label_argr_0.text()), 1, 2048)
        if ok:
            self.label_argr_0.setText(str(argr))
            self.argstemp['argr'] = str(argr)

    def slotargtime(self):
        argtime,ok = QInputDialog.getInteger(self,
                                            self.tr(u"参数次数"),
                                            self.tr(u"请输入time的值:"),
                                            int(self.label_argtime.text()), 1, 10)
        if ok:
            self.label_argtime.setText(str(argtime))
            self.argstemp['times'] = str(argtime)

    def slotset(self):
        self.updatesetting(self.argstemp)
        self.close()

    def slothelp(self):
        helpdialog = HelpDialog()
        helpdialog.exec_()

    def slotdefault(self):
        defaultargs = self.readsetting('iozone-default/')
        self.argstemp = defaultargs
        self.label_argi_0.setText(defaultargs["argi"])
        self.label_args_0.setText("%d" % defaultargs["args"])
        self.label_argt_0.setText("%d" % defaultargs["argt"])
        self.label_argr_0.setText("%d" % defaultargs["argr"])
        self.label_argrtime.setText("%d" % defaultargs["times"])
        self.setargsprint()

    def retranslateUi(self):
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = unicode(styleSheet, encoding='utf8')
        QtGui.qApp.setStyleSheet(styleSheet)


# HELP
class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super(HelpDialog,self).__init__(parent)
        self.setWindowTitle(self.tr(u"帮助"))
        self.resize(300,250)

        listWidget = QListWidget()
        listWidget.insertItem(0, self.tr(u"支持参数"))
        listWidget.insertItem(1, self.tr(u"其他说明"))

        label1 = QLabel(self.tr(u"""-i  N  用来选择测试项比如Read/Write/Random 比较常用的是0 1 2 \n\n -r  block size  指定一次写入或读出的块大小\n\n-s  file size  测试文件的大小,一般为内存两倍\n\n-t   N  以吞吐量模式运行Iozone,该选项允许用户指定测试时使用多少个线程或者进程."""))
        label2 = QLabel(self.tr(u"""\n  通常情况下,测试的文件大小要求至少是系统内存的两倍以上.如果小于两倍,文件的读写\n\n测试读写的将是cache>的速度,>测试的结果不准确。你应该使用sync选项挂载文件系统\n\n或使用大小为系统内存两倍的文件.如果测试时间太长，可先在grub.conf里把内存调小.\n\n例如:如果把存调>整为256M，使用512M的文件测试."""))

        stack = QStackedWidget()
        stack.addWidget(label1)
        stack.addWidget(label2)

        mainLayout = QHBoxLayout(self)
        mainLayout.setMargin(5)
        mainLayout.setSpacing(5)
        mainLayout.addWidget(listWidget)
        mainLayout.addWidget(stack, 0, Qt.AlignHCenter)
        mainLayout.setStretchFactor(listWidget,1)
        mainLayout.setStretchFactor(stack,3)
        self.connect(listWidget,SIGNAL("currentRowChanged(int)"),stack,SLOT("setCurrentIndex(int)"))


# test
#app = QApplication(sys.argv)
#form = PerfioSet()
#form.show()
#app.exec_()
