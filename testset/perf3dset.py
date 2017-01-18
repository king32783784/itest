#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog
from common import *

class Perf3dSet(QDialog):

    def __init__(self, parent=None):
        super(Perf3dSet, self).__init__(parent)
        self.setWindowTitle(u"3D")
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
        self.checkbox_ubgears = QtGui.QCheckBox(u'unixbench-ubgears')
        self.connect(self.checkbox_ubgears, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_ubgears)
        self.checkbox_glmark = QtGui.QCheckBox(u'glmark')
        self.connect(self.checkbox_glmark, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_glmark)

    def createbutton(self):
        self.ubgearssetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.ubgearssetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetubgears)
        self.glmarksetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.glmarksetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetglmark)
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
        baseLayout.addWidget(self.checkbox_ubgears, 0,0)
        baseLayout.addWidget(self.checkbox_glmark, 1,0)

        baseLayout.addWidget(self.ubgearssetbutton, 0,3)
        baseLayout.addWidget(self.glmarksetbutton, 1,3)
        
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
        testargs = self.readsetting("perf3d-user/")
        if testargs["ubgears"] == "E":
            self.checkbox_ubgears.setChecked(True)
        if testargs["glmark"] == "E":
            self.checkbox_glmark.setChecked(True)
   
    def readsetting(self, setmode):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["ubgears"] = self.config.value(QString(setmode) + "ubgears").toString()[0:]
        testargs["glmark"] = self.config.value(QString(setmode) + "glmark").toString()[0:]
        return testargs

    def updatesetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("perf3d-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def Oncheckbox_ubgears(self):
        if self.checkbox_ubgears.isChecked():
            self.argstemp["ubgears"] = "E"
        else:
            self.argstemp["glmark"] = "D"

    def Oncheckbox_glmark(self):
        if self.checkbox_glmark.isChecked():
            self.argstemp["glmark"] = "E"
        else:
            self.argstemp["glmark"] = "D"

    def Onsetubgears(self):
        setubgears = UbgearsSet()
        setubgears.exec_()

    def Onsetglmark(self):
        setglmark = GlmarkSet()
        setglmark.exec_()
       
    def Ondefault(self):
        defaultset = self.readsetting("perf3d-default/")
        if defaultset["ubgears"] == "E":
            self.checkbox_ubgears.setChecked(True)
        else:
            self.checkbox_ubgears.setChecked(False)
        if defaultset["glmark"] == "E":
            self.checkbox_glmark.setChecked(True)
        else:
            self.checkbox_glmark.setChecked(False)    
        self.argstemp = defaultset

    def Onhelp(self):
        helpdialog = HelpPerf3d()
        helpdialog.exec_()
    
    def Onset(self):
        self.updatesetting()
        self.close()

    def Onsetall(self):
        self.checkbox_ubgears.setChecked(True)
        self.checkbox_glmark.setChecked(True)
        self.argstemp["ubgears"] = "E"
        self.argstemp["glmark"] = "E"

# unixbench-ubgears测试设置

class UbgearsSet(QDialog):
    
    def __init__(self, parent=None):
        super(UbgearsSet, self).__init__(parent)
        self.setWindowTitle("ubgears设置")
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
        self.config.beginGroup("ubgears-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["argt"] = self.config.value(QString("ubgears-user/") + "argt").toInt()[0]
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
        self.argstemp["argt"] = self.config.value(QString("ubgears-default/") + "argt").toInt()[0]
        self.timesshow.setText(self.argstemp["argt"])

    def Onsetbutton(self):
        self.updatesetting()
        self.close()


# glmark设置
class GlmarkSet(QDialog):

    def __init__(self, parent=None):
        super(GlmarkSet, self).__init__(parent)
        self.setWindowTitle("Glmark设置")
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
        self.widthlabel = QLabel(self.tr("水平像数"))
        self.widthshow = QLabel("")
        self.widthshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.heightlabel = QLabel(self.tr("垂直像数"))
        self.heightshow = QLabel("")
        self.heightshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.windowlabel = QLabel(self.tr("模式(0窗口1全屏)"))
        self.windowshow = QLabel("")
        self.windowshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)       
        self.bpplabel = QLabel(self.tr("像素深度"))
        self.bppshow = QLabel("")
        self.bppshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)


    def createbutton(self):
        self.timesbutton = QPushButton(u"自定义")
        self.connect(self.timesbutton, QtCore.SIGNAL("clicked()"), self.Ontimesbutton)
        self.widthbutton = QPushButton(u"自定义")
        self.connect(self.widthbutton, QtCore.SIGNAL("clicked()"), self.Onwidthbutton)
        self.heightbutton = QPushButton(u"自定义")
        self.connect(self.heightbutton, QtCore.SIGNAL("clicked()"), self.Onheightbutton)
        self.windowbutton = QPushButton(u"自定义")
        self.connect(self.windowbutton, QtCore.SIGNAL("clicked()"), self.Onwindowbutton)
        self.bppbutton = QPushButton(u"自定义")
        self.connect(self.bppbutton, QtCore.SIGNAL("clicked()"), self.Onbppbutton)
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
        baseLayout.addWidget(self.widthlabel, 1,0)
        baseLayout.addWidget(self.widthshow, 1,1)
        baseLayout.addWidget(self.widthbutton, 1,3)
        baseLayout.addWidget(self.heightlabel, 2,0)
        baseLayout.addWidget(self.heightshow, 2,1)
        baseLayout.addWidget(self.heightbutton, 2,3)
        baseLayout.addWidget(self.bpplabel, 3,0)
        baseLayout.addWidget(self.bppshow, 3,1)
        baseLayout.addWidget(self.bppbutton, 3,3)
        baseLayout.addWidget(self.windowlabel, 4,0)
        baseLayout.addWidget(self.windowshow, 4,1)
        baseLayout.addWidget(self.windowbutton,4,3)

        footer1Layout = QHBoxLayout()
        acer1 = QtGui.QSpacerItem(30,160)
        acer2 = QtGui.QSpacerItem(50,10)

        footer2Layout = QHBoxLayout()
        footer1Layout.addWidget(self.helpbutton)
        footer1Layout.addWidget(self.defaultbutton)
        baseLayout.addItem(acer1, 5,0)
        baseLayout.addItem(acer2, 6,1)
        footer2Layout.addWidget(self.setbutton)

       # baseLayout.setSizeConstraint(QLayout.SetFixedSize)
       # baseLayout.setSpacing(10)
        baseLayout.addLayout(footer1Layout,6,0)
        baseLayout.addLayout(footer2Layout,6,3)
        self.setLayout(baseLayout)

    def initstatus(self):
        testargs = self.readsetting()
        self.timesshow.setText(str(testargs["args"]))
        self.widthshow.setText(str(testargs["argw"]))
        self.heightshow.setText(str(testargs["argh"]))
        self.windowshow.setText(str(testargs["argm"]))
        self.bppshow.setText(str(testargs["argb"]))

    def updatesetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.config.beginGroup("glmark-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        testargs = {}
        testargs["args"] = self.config.value(QString("glmark-user/") + "args").toInt()[0]
        testargs["argw"] = self.config.value(QString("glmark-user/") + "argw").toInt()[0]
        testargs["argh"] = self.config.value(QString("glmark-user/") + "argh").toInt()[0]
        testargs["argm"] = self.config.value(QString("glmark-user/") + "argm").toInt()[0]
        testargs["argb"] = self.config.value(QString("glmark-user/") + "argb").toInt()[0]
        return testargs

    def Ontimesbutton(self):
        args, ok = QInputDialog.getInteger(self,
                                           self.tr(u'参数times'),
                                           self.tr(u"请输入参数times:默认为3"),
                                           int(self.timesshow.text()),1,10)
        if ok:
            self.timesshow.setText(str(args))
            self.argstemp['args'] = str(args)

    def Onbppbutton(self):
        argb, ok = QInputDialog.getInteger(self,
                                           self.tr(u'参数bpp'),
                                           self.tr(u"请输入参数bpp:默认为32"),
                                           int(self.timesshow.text()),1,256)
        if ok:
            self.timesshow.setText(str(argb))
            self.argstemp['argb'] = str(argb)


    def Onwidthbutton(self):
        argw, ok = QInputDialog.getInteger(self,
                                           self.tr(u'水平像素'),
                                           self.tr(u"请输入水平像素的值:默认为1024"),
                                           int(self.widthshow.text()),1,10240)
        if ok:
            self.widthshow.setText(str(argw))
            self.argstemp['argw'] = str(argw)

    def Onheightbutton(self):
        argh, ok = QInputDialog.getInteger(self,
                                           self.tr(u'垂直像素'),
                                           self.tr(u"请输入垂直像素的值:默认为768"),
                                           int(self.heightshow.text()),1,10240)
        if ok:
            self.heightshow.setText(str(argh))
            self.argstemp['argh'] = str(argh)

    def Onwindowbutton(self):
        argm, ok = QInputDialog.getInteger(self,
                                           self.tr(u'窗口模式'),
                                           self.tr(u"请输入窗口模式:0全屏1窗口"),
                                           int(self.windowshow.text()),0,1)
        if ok:
            self.windowshow.setText(str(argm))
            self.argstemp['argm'] = str(argm)



    def Onhelpbutton(self):
        helpdialog = HelpGlmark()
        helpdialog.exec_()

    def Ondefaultbutton(self):
        self.config = QSettings(SET_FILE, QSettings.IniFormat)
        self.argstemp["args"] = self.config.value(QString("glmark-default/") + "args").toInt()[0]
        self.argstemp["argw"] = self.config.value(QString("glmark-default/") + "argw").toInt()[0]
        self.argstemp["argh"] = self.config.value(QString("glmark-default/") + "argh").toInt()[0]
        self.argstemp["argm"] = self.config.value(QString("glmark-default/") + "argm").toInt()[0]
        self.argstemp["argb"] = self.config.value(QString("glmark-default/") + "argb").toInt()[0]
        self.timesshow.setText(str(self.argstemp["args"]))
        self.widthshow.setText(str(self.argstemp["argw"]))
        self.heightshow.setText(str(self.argstemp["argh"]))
        self.windowshow.setText(str(self.argstemp["argm"]))
        self.bppshow.setText(str(self.argstemp["argb"]))

    def Onsetbutton(self):
        self.updatesetting()
        self.close()


# HELP

class HelpUbgears(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""sysbench mem test 设置说明"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

class HelpGlmark(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""stream test 设置说明"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

class HelpPerf3d(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""Perfmem 包含2种内存性能的测试，分别为stream、sysbench."""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

# test
# app = QApplication(sys.argv)
# form = Perf3dSet()
# form.show()
# app.exec_()
