#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
sys.path.append('..')
from helpinfo import HelpDialog

class PerfmemSet(QDialog):

    def __init__(self, parent=None):
        super(PerfmemSet, self).__init__(parent)
        self.setWindowTitle(u"内存性能")
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
        self.checkbox_stream = QtGui.QCheckBox(u'stream')
        self.connect(self.checkbox_stream, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_stream)
        self.checkbox_sysbench = QtGui.QCheckBox(u'sysbench-mem')
        self.connect(self.checkbox_sysbench, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_sysbench)

    def createbutton(self):
        self.streamsetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.streamsetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetstream)
        self.sysbenchsetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.sysbenchsetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetsysbench)
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
        baseLayout.addWidget(self.checkbox_stream, 0,0)
        baseLayout.addWidget(self.checkbox_sysbench, 2,0)

        baseLayout.addWidget(self.streamsetbutton, 0,3)
        baseLayout.addWidget(self.sysbenchsetbutton, 2,3)
        
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
        testargs = self.readsetting("perfmem-user/")
        if testargs["stream"] == "E":
            self.checkbox_stream.setChecked(True)
        if testargs["sysbenchmem"] == "E":
            self.checkbox_sysbench.setChecked(True)
   
    def readsetting(self, setmode):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        testargs = {}
        testargs["stream"] = self.config.value(QString(setmode) + "stream").toString()[0:]
        testargs["sysbenchmem"] = self.config.value(QString(setmode) + "sysbenchmem").toString()[0:]
        print testargs
        return testargs

    def updatesetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.beginGroup("perfmem-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def Oncheckbox_stream(self):
        if self.checkbox_stream.isChecked():
            self.argstemp["stream"] = "E"
        else:
            self.argstemp["stream"] = "D"

    def Oncheckbox_sysbench(self):
        if self.checkbox_sysbench.isChecked():
            self.argstemp["sysbenchmem"] = "E"
        else:
            self.argstemp["sysbenchmem"] = "D"

    def Onsetstream(self):
        setstream = StreamSet()
        setstream.exec_()

    def Onsetsysbench(self):
        setsysbench = SysbenchSet()
        setsysbench.exec_()
       
    def Ondefault(self):
        defaultset = self.readsetting("perfmem-default/")
        if defaultset["stream"] == "E":
            self.checkbox_stream.setChecked(True)
        else:
            self.checkbox_stream.setChecked(False)
        if defaultset["sysbenchmem"] == "E":
            self.checkbox_sysbench.setChecked(True)
        else:
            self.checkbox_sysbench.setChecked(False)    
        self.argstemp = defaultset

    def Onhelp(self):
        helpdialog = HelpPerfmem()
        helpdialog.exec_()
    
    def Onset(self):
        self.updatesetting()
        self.close()

    def Onsetall(self):
        self.checkbox_stream.setChecked(True)
        self.checkbox_sysbench.setChecked(True)
        self.argstemp["stream"] = "E"
        self.argstemp["sysbenchmem"] = "E"

# sysbench-cpu测试设置

class SysbenchSet(QDialog):
    
    def __init__(self, parent=None):
        super(SysbenchSet, self).__init__(parent)
        self.setWindowTitle("sysbench设置")
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
        self.memblocklabel = QLabel(self.tr("参数memory-block-size"))
        self.memblockshow = QLabel("")
        self.memblockshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.memsizelabel = QLabel(self.tr("参数memory-total-size"))
        self.memsizeshow = QLabel("")
        self.memsizeshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)

    def createbutton(self):
        self.threadbutton = QPushButton(u"自定义")
        self.connect(self.threadbutton, QtCore.SIGNAL("clicked()"), self.Onthreadbutton)
        self.memblockbutton = QPushButton(u"自定义")
        self.connect(self.memblockbutton, QtCore.SIGNAL("clicked()"), self.Onmemblockbutton)
        self.memsizebutton = QPushButton(u"自定义")
        self.connect(self.memsizebutton, QtCore.SIGNAL("clicked()"), self.Onmemsizebutton)
        self.helpbutton = QPushButton(u"帮助")
        self.connect(self.helpbutton, QtCore.SIGNAL("clicked()"), self.Onhelpbutton)
        self.defaultbutton = QPushButton(u"默认")
        self.connect(self.defaultbutton, QtCore.SIGNAL("clicked()"), self.Ondefaultbutton)
        self.setbutton = QPushButton(u"确认")
        self.connect(self.setbutton, QtCore.SIGNAL("clicked()"), self.Onsetbutton)

    def Layout(self):
        baseLayout = QGridLayout()
        baseLayout.addWidget(self.threadlabel, 0,0)
        baseLayout.addWidget(self.memblocklabel, 1,0)
        baseLayout.addWidget(self.memsizelabel, 2,0)
        baseLayout.addWidget(self.threadshow, 0,1)
        baseLayout.addWidget(self.memblockshow, 1,1)
        baseLayout.addWidget(self.memsizeshow, 2,1)
        
        baseLayout.addWidget(self.threadbutton, 0,3)
        baseLayout.addWidget(self.memblockbutton, 1,3)
        baseLayout.addWidget(self.memsizebutton, 2,3)

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
        self.memblockshow.setText(str(testargs["argb"]))
        self.memsizeshow.setText(str(testargs["args"]))

    def updatesetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.beginGroup("sysbenchmem-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        testargs = {}
        testargs["argt"] = self.config.value(QString("sysbenchmem-user/") + "argt").toString()[0:]
        testargs["argb"] = self.config.value(QString("sysbenchmem-user/") + "argb").toInt()[0]
        testargs["args"] = self.config.value(QString("sysbenchmem-user/") + "args").toInt()[0]
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

    def Onmemblockbutton(self):
        argb, ok = QInputDialog.getInteger(self, 
                                           self.tr(u'参数memory-block-size'),
                                           self.tr(u"请输入参数memory-block-size:一般为1024的倍数"),
                                           int(self.memblockshow.text()),1,1073741824)
        if ok:
            self.memblockshow.setText(str(argb))
            self.argstemp['argb'] = str(argb)

    def Onmemsizebutton(self):
        args, ok = QInputDialog.getInteger(self, 
                                           self.tr(u'参数memory-total-size'),
                                           self.tr(u"请输入参数memory-total-size:单位为G"),
                                           int(self.memsizeshow.text()),1,1024)
        if ok:
            self.memsizeshow.setText(str(args))
            self.argstemp['args'] = str(args)

    def Onhelpbutton(self):
        helpdialog = HelpSysmem()
        helpdialog.exec_()

    def Ondefaultbutton(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.argstemp["argt"] = self.config.value(QString("sysbenchmem-default/") + "argt").toString()[0:]
        self.argstemp["argb"] = self.config.value(QString("sysbenchmem-default/") + "argb").toInt()[0]
        self.argstemp["args"] = self.config.value(QString("sysbenchmem-default/") + "args").toInt()[0]
        self.threadshow.setText(self.argstemp["argt"])
        self.memblockshow.setText(str(self.argstemp["argb"]))
        self.memsizeshow.setText(str(self.argstemp["args"]))

    def Onsetbutton(self):
        self.updatesetting()
        self.close()


# stream设置
class StreamSet(QDialog):

    def __init__(self, parent=None):
        super(StreamSet, self).__init__(parent)
        self.setWindowTitle("stream设置")
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
        self.timeslabel = QLabel(self.tr("测试次数t(times)"))
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
        self.config.beginGroup("stream-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        testargs = {}
        testargs["argt"] = self.config.value(QString("stream-user/") + "argt").toString()[0:]
        testargs["args"] = self.config.value(QString("stream-user/") + "args").toInt()[0]
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
                                           self.tr(u"请输入参数times:默认为3"),
                                           int(self.timesshow.text()),1,10)
        if ok:
            self.timesshow.setText(str(args))
            self.argstemp['args'] = str(args)

    def Onhelpbutton(self):
        helpdialog = HelpStream()
        helpdialog.exec_()

    def Ondefaultbutton(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.argstemp["argt"] = self.config.value(QString("stream-default/") + "argt").toString()[0:]
        self.argstemp["args"] = self.config.value(QString("stream-default/") + "args").toInt()[0]
        self.threadshow.setText(self.argstemp["argt"])
        self.timesshow.setText(str(self.argstemp["args"]))

    def Onsetbutton(self):
        self.updatesetting()
        self.close()


# HELP

class HelpSysmem(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""sysbench mem test 设置说明"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

class HelpStream(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""stream test 设置说明"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

class HelpPerfmem(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""Perfmem 包含2种内存性能的测试，分别为stream、sysbench."""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

# test
# app = QApplication(sys.argv)
# form = PerfmemSet()
# form.show()
# app.exec_()
