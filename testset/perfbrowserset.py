#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from helpinfo import HelpDialog

class PerfbrowserSet(QDialog):

    def __init__(self, parent=None):
        super(PerfbrowserSet, self).__init__(parent)
        self.setWindowTitle(u"浏览器")
        self.resize(450, 550)
        palette1 = QtGui.QPalette()
        palette1.setColor(self.backgroundRole(), QColor("#cccddc"))
        self.setPalette(palette1)
        self.setAutoFillBackground(True)
        self.argstemp = {}
        self.createlabel()
        self.createcheckbox()
        self.createbutton()
        self.Layout()
        self.initstatus()

    def createlabel(self):
        self.browserlabel = QLabel(self.tr("选择测试浏览器:"))       
        self.mainlabel = QLabel(self.tr("选择测试项目:"))        

    def createcheckbox(self):
        self.checkbox_acid3 = QtGui.QCheckBox(u'acid3')
        self.connect(self.checkbox_acid3, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_acid3)
        self.checkbox_v8test = QtGui.QCheckBox(u'v8test')
        self.connect(self.checkbox_v8test, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_v8test)
        self.checkbox_css4 = QtGui.QCheckBox(u'css4')
        self.connect(self.checkbox_css4, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_css4)
        self.checkbox_octane = QtGui.QCheckBox(u'octane')
        self.connect(self.checkbox_octane, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_octane)
        self.checkbox_html5 = QtGui.QCheckBox(u'html5')
        self.connect(self.checkbox_html5, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_html5)
        self.checkbox_dromaeo = QtGui.QCheckBox(u'dromaeo')
        self.connect(self.checkbox_dromaeo, QtCore.SIGNAL('clicked()'),
                     self.Oncheckbox_dromaeo)
        self.radio_chrome = QtGui.QRadioButton(u'chrome')
        self.connect(self.radio_chrome, QtCore.SIGNAL('clicked()'),
                     self.Onradio_chrome)      
        self.radio_firefox = QtGui.QRadioButton(u'firefox')
        self.connect(self.radio_firefox, QtCore.SIGNAL('clicked()'),
                     self.Onradio_firefox)
        self.radio_all = QtGui.QRadioButton(u'All')
        self.connect(self.radio_all, QtCore.SIGNAL('clicked()'),
                     self.Onradio_all)

    def createbutton(self):
        self.css4setbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.css4setbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetcss4)
        self.acid3setbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.acid3setbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetacid3)
        self.v8testsetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.v8testsetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetv8test)
        self.octanesetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.octanesetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetoctane)
        self.html5setbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.html5setbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsethtml5)
        self.dromaeosetbutton = QtGui.QPushButton(u"参数设置")
        self.connect(self.dromaeosetbutton, QtCore.SIGNAL('clicked()'),
                     self.Onsetdromaeo)
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
        baseLayout.addWidget(self.mainlabel, 0,0)
        baseLayout.addWidget(self.checkbox_css4, 1,0)
        baseLayout.addWidget(self.checkbox_acid3, 2,0)
        baseLayout.addWidget(self.checkbox_v8test, 3,0)
        baseLayout.addWidget(self.checkbox_octane, 4,0)
        baseLayout.addWidget(self.checkbox_html5, 5,0)
        baseLayout.addWidget(self.checkbox_dromaeo, 6,0)
        baseLayout.addWidget(self.browserlabel, 7,0)

        baseLayout.addWidget(self.css4setbutton, 1,3)
        baseLayout.addWidget(self.acid3setbutton, 2,3)
        baseLayout.addWidget(self.v8testsetbutton, 3,3)
        baseLayout.addWidget(self.octanesetbutton, 4,3)
        baseLayout.addWidget(self.html5setbutton, 5,3)
        baseLayout.addWidget(self.dromaeosetbutton, 6,3)
        
        footer1Layout = QHBoxLayout()
        acer1 = QtGui.QSpacerItem(10,100)
        acer2 = QtGui.QSpacerItem(40,10)
        
        browserLayout = QHBoxLayout()
        browserLayout.addWidget(self.radio_chrome)
        browserLayout.addWidget(self.radio_firefox)
        browserLayout.addWidget(self.radio_all)

        footer2Layout = QHBoxLayout()
        footer1Layout.addWidget(self.helpbutton)
        footer1Layout.addWidget(self.defaultbutton)
        baseLayout.addItem(acer1, 9,0)
        baseLayout.addItem(acer2, 10,1)
        footer2Layout.addWidget(self.setallbutton)
        footer2Layout.addWidget(self.setbutton)

       # baseLayout.setSizeConstraint(QLayout.SetFixedSize)
       # baseLayout.setSpacing(10)
        baseLayout.addLayout(browserLayout,8,0)
        baseLayout.addLayout(footer1Layout,10,0)
        baseLayout.addLayout(footer2Layout,10,3)
        self.setLayout(baseLayout)

    def initstatus(self):
        testargs = self.readsetting("perfbrowser-user/")
        if testargs["css4"] == "E":
            self.checkbox_css4.setChecked(True)
        if testargs["acid3"] == "E":
            self.checkbox_acid3.setChecked(True)
        if testargs["v8test"] == "E":
            self.checkbox_v8test.setChecked(True)
        if testargs["octane"] == "E":
            self.checkbox_octane.setChecked(True)
        if testargs["html5"] == "E":
            self.checkbox_html5.setChecked(True)
        if testargs["dromaeo"] == "E":
            self.checkbox_dromaeo.setChecked(True)
        if testargs["browser"] == "C":
            self.radio_chrome.setChecked(True)
        elif testargs["browser"] == "F":
            self.radio_firefox.setChecked(True)
        else:
            self.radio_all.setChecked(True)
   
    def readsetting(self, setmode):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        testargs = {}
        testargs["css4"] = self.config.value(QString(setmode) + "css4").toString()[0:]
        testargs["acid3"] = self.config.value(QString(setmode) + "acid3").toString()[0:]
        testargs["v8test"] = self.config.value(QString(setmode) + "v8test").toString()[0:]
        testargs["octane"] = self.config.value(QString(setmode) + "octane").toString()[0:]
        testargs["html5"] = self.config.value(QString(setmode) + "html5").toString()[0:]
        testargs["dromaeo"] = self.config.value(QString(setmode) + "dromaeo").toString()[0:]
        testargs["browser"] = self.config.value(QString(setmode) + "browser").toString()[0:]
        return testargs

    def updatesetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.beginGroup("perfbrowser-user")
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def Oncheckbox_css4(self):
        if self.checkbox_css4.isChecked():
            self.argstemp["css4"] = "E"
        else:
            self.argstemp["css4"] = "D"

    def Oncheckbox_acid3(self):
        if self.checkbox_acid3.isChecked():
            self.argstemp["acid3"] = "E"
        else:
            self.argstemp["acid3"] = "D"

    def Oncheckbox_v8test(self):
        if self.checkbox_v8test.isChecked():
            self.argstemp["v8test"] = "E"
        else:
            self.argstemp["v8test"] = "D"

    def Oncheckbox_octane(self):
        if self.checkbox_octane.isChecked():
            self.argstemp["octane"] = "E"
        else:
            self.argstemp["octane"] = "D"

    def Oncheckbox_html5(self):
        if self.checkbox_html5.isChecked():
            self.argstemp["html5"] = "E"
        else:
            self.argstemp["html5"] = "D"

    def Oncheckbox_dromaeo(self):
        if self.checkbox_dromaeo.isChecked():
            self.argstemp["dromaeo"] = "E"
        else:
            self.argstemp["dromaeo"] = "D"
 
    def Onradio_chrome(self):
        if self.radio_chrome.isChecked():
            self.argstemp["browser"] = "C"
    
    def Onradio_firefox(self):
        if self.radio_firefox.isChecked():
            self.argstemp["browser"] = "F"
    
    def Onradio_all(self):
        if self.radio_all.isChecked():
            self.argstemp["browser"] = "A"

    def Onsetcss4(self):
        setcss4 = BrowserSet("css4")
        setcss4.exec_()

    def Onsetacid3(self):
        setacid3 = BrowserSet("acid3")
        setacid3.exec_()

    def Onsetv8test(self):
        setv8test = BrowserSet("v8test")
        setv8test.exec_()
       
    def Onsetoctane(self):
        setoctane = BrowserSet("octane")
        setoctane.exec_()

    def Onsetdromaeo(self):
        setdromaeo = BrowserSet("dromaeo")
        setdromaeo.exec_()

    def Onsethtml5(self):
        sethtml5 = BrowserSet("html5")
        sethtml5.exec_()

    def Ondefault(self):
        defaultset = self.readsetting("perfbrowser-default/")
        if defaultset["css4"] == "E":
            self.checkbox_css4.setChecked(True)
        else:
            self.checkbox_css4.setChecked(False)
        if defaultset["acid3"] == "E":
            self.checkbox_acid3.setChecked(True)
        else:
            self.checkbox_acid3.setChecked(False)
        if defaultset["v8test"] == "E":
            self.checkbox_v8test.setChecked(True)
        else:
            self.checkbox_v8test.setChecked(False)
        if defaultset["octane"] == "E":
            self.checkbox_octane.setChecked(True)
        else:
            self.checkbox_octane.setChecked(False) 
        if defaultset["html5"] == "E":
            self.checkbox_html5.setChecked(True)
        else:
            self.checkbox_html5.setChecked(False)
        if defaultset["dromaeo"] == "E":
            self.checkbox_dromaeo.setChecked(True)
        else:
            self.checkbox_dromaeo.setChecked(False) 
        if defaultset["browser"] == "A":
            self.radio_all.setChecked(True)
        elif defaultset["browser"] == "C":
            self.radio_chrome.setChecked(True)
        else:
            self.radio_firefox.setChecked(True)    
        self.argstemp = defaultset

    def Onhelp(self):
        helpdialog = HelpBrowser()
        helpdialog.exec_()
    
    def Onset(self):
        self.updatesetting()
        self.close()

    def Onsetall(self):
        self.checkbox_css4.setChecked(True)
        self.checkbox_acid3.setChecked(True)
        self.checkbox_v8test.setChecked(True)
        self.checkbox_octane.setChecked(True)
        self.checkbox_html5.setChecked(True)
        self.checkbox_dromaeo.setChecked(True)
        self.radio_all.setChecked(True)
        self.argstemp["css4"] = "E"
        self.argstemp["acid3"] = "E"
        self.argstemp["v8test"] = "E"
        self.argstemp["octane"] = "E"
        self.argstemp["html5"] = "E"
        self.argstemp["dromaeo"] = "E"
        self.argstemp["browser"] = "A"


# 测试设置

class BrowserSet(QDialog):
    
    def __init__(self,testitem):
        super(BrowserSet, self).__init__()
        self.testitem = testitem
        self.setWindowTitle("%s设置" % self.testitem)
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
        self.threadlabel = QLabel(self.tr("测试次数(times)"))
        self.threadshow = QLabel("")
        self.threadshow.setFrameStyle(QFrame.Panel|QFrame.Sunken)

    def createbutton(self):
        self.threadbutton = QPushButton(u"自定义")
        self.connect(self.threadbutton, QtCore.SIGNAL("clicked()"), self.Onthreadbutton)
        self.helpbutton = QPushButton(u"帮助")
        self.connect(self.helpbutton, QtCore.SIGNAL("clicked()"), self.Onhelpbutton)
        self.defaultbutton = QPushButton(u"默认")
        self.connect(self.defaultbutton, QtCore.SIGNAL("clicked()"), self.Ondefaultbutton)
        self.setbutton = QPushButton(u"确认")
        self.connect(self.setbutton, QtCore.SIGNAL("clicked()"), self.Onsetbutton)

    def Layout(self):
        baseLayout = QGridLayout()
        baseLayout.addWidget(self.threadlabel, 0,0)
        baseLayout.addWidget(self.threadshow, 0,1)
        
        baseLayout.addWidget(self.threadbutton, 0,3)

        footer1Layout = QHBoxLayout()
        acer1 = QtGui.QSpacerItem(10,300)
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

    def updatesetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.beginGroup("%s-user/" %self.testitem)
        for key, value in self.argstemp.iteritems():
            self.config.setValue(key, value)
        self.config.endGroup()

    def readsetting(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        testargs = {}
        testargs["argt"] = self.config.value(QString("%s-user/"%self.testitem) + "argt").toInt()[0]
        return testargs

    def Onthreadbutton(self):
        argt, ok = QInputDialog.getInteger(self,
                                           self.tr(u"次数"),
                                           self.tr(u"请输入测试次数:默认3"),
                                           int(self.threadshow.text()), 1,10)
        if ok:
            self.threadshow.setText(str(argt))
            self.argstemp['argt'] = str(argt)

    def Onhelpbutton(self):
        helpdialog = HelpTime()
        helpdialog.exec_()

    def Ondefaultbutton(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.argstemp["argt"] = self.config.value(QString("browseritem-default/") + "argt").toInt()[0]
        self.threadshow.setText(str(self.argstemp["argt"]))

    def Onsetbutton(self):
        self.updatesetting()
        self.close()

class HelpTime(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""设置测试次数"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)


class HelpBrowser(HelpDialog):
    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""浏览器测试包含6种测试，分别为css4、acid3、v8test、octane、html5、dromaeo."""))
        self.stack = QStackedWidget()
        self.stack.addWidget(self.label1)

# test
# app = QApplication(sys.argv)
# form = PerfbrowserSet()
# form.show()
# app.exec_()
