#*-*coding=utf-8*-*

import sys

from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from common import *
from mkresult import *
from PyQt4.QtWebKit import QWebSettings, QWebPage


class SearchResult(QtGui.QWidget):
    def __init__(self, parent=None):
        super(SearchResult, self).__init__(parent)
        self.resultslist = getresultslist()
        self.createwebview()
        # combobox
        self.createcombobox()
        logger.info("result check")
        # vertical box layout
        namelabel = QtGui.QLabel(u"选择报告")
        hlayout = QtGui.QVBoxLayout()
        hlayout.addWidget(namelabel)
        hlayout.addWidget(self.combobox)
        hlayout.addLayout(self.weblayout)
        hlayout.addWidget(self.webview)
        self.setLayout(hlayout)

    def createwebview(self):
        self.webview = QtWebKit.QWebView(self)
        self.search = None
        resultaddress = getcurrentresult()
        # 导航至测试结果
       # self.webview.load(QtCore.QUrl(resultaddress["address"]))
        # 搜索框
        self.search = QtGui.QLineEdit(self)
        #  signals
        self.search.textEdited.connect(self.search_edited)
        self.search.returnPressed.connect(self.search_entered)
        #  search label
        label_search = QtGui.QLabel(u'内容查找', self)
        label_search.setBuddy(self.search)
        # 结果保存
        self.weblayout = QtGui.QHBoxLayout()
        self.weblayout.addWidget(label_search)
        self.weblayout.addWidget(self.search)

    def search_edited(self, text):
        # finds all occurrences of the specified string
        find_flags = QWebPage.HighlightAllOccurrences | QWebPage.FindWrapsAroundDocument
        self.webview.findText('', find_flags)
        self.webview.findText(text, find_flags)

    def search_entered(self):
        # goes to the next occurrence of the specified string when the ENTER key is pressed
        find_flags = QWebPage.FindWrapsAroundDocument
        self.webview.findText(self.search.text(), find_flags)

    def createcombobox(self):
        self.combobox = QtGui.QComboBox()
        self.namelist = []
        self.addresslist = []
        for name, address in self.resultslist.iteritems():
            self.namelist.append(name)
            self.addresslist.append(address)
        self.combobox.addItems(self.namelist)
        if len(self.addresslist) > 0:
            self.webview.load(QtCore.QUrl(self.addresslist[0]))
            self.combobox.activated.connect(self.setCurrentIndex)

    def setCurrentIndex(self, index):
        self.combobox.setCurrentIndex(index)
        self.labelindex = index
        self.webview.load(QtCore.QUrl(self.addresslist[index]))
        print(self.labelindex)


class MakeReport(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MakeReport, self).__init__(parent)
        # vertical box layout
        setlavel1 = QtGui.QLabel(u"设置对比项目:")
        self.checkbox1 = QtGui.QCheckBox(u"项目1")
        self.checkbox2 = QtGui.QCheckBox(u"项目2")
        self.checkbox3 = QtGui.QCheckBox(u"项目3")
        self.checkbox4 = QtGui.QCheckBox(u"项目4")
        self.checkbox5 = QtGui.QCheckBox(u"项目5")
        self.checkitems = {"item1": self.checkbox1, "item2": self.checkbox2,
                           "item3": self.checkbox3, "item4": self.checkbox4,
                           "item5": self.checkbox5}
        setlavel2 = QtGui.QLabel(u"选择报告类型:")
        self.combobox1 = self.create_combox()
        self.combobox1.activated.connect(self.setCurrentIndex1)
        self.combobox2 = self.create_combox()
        self.combobox2.activated.connect(self.setCurrentIndex2)
        self.combobox3 = self.create_combox()
        self.combobox3.activated.connect(self.setCurrentIndex3)
        self.combobox4 = self.create_combox()
        self.combobox4.activated.connect(self.setCurrentIndex4)
        self.combobox5 = self.create_combox()
        self.combobox5.activated.connect(self.setCurrentIndex5)
        if self.oslist is not None:
            self.OSLIST = {"item1":self.oslist[0], "item2":self.oslist[0],
                           "item3":self.oslist[0], "item4":self.oslist[0],
                           "item5": self.oslist[0]}
        self.report_type1 = QtGui.QCheckBox(u"HTML格式")
        self.report_type2 = QtGui.QCheckBox(u"XLS格式")
        makebutton = QtGui.QPushButton("开始制作")
        self.connect(makebutton, QtCore.SIGNAL('clicked()'), self.OnStart)
        cancelbutton = QtGui.QPushButton("取消")
        self.connect(cancelbutton, QtCore.SIGNAL('clicked()'), self.OnCancel)
        self.namefield = QtGui.QLineEdit() # 报告名称输入区
        setlavel3 = QtGui.QLabel(u"输入报名名称:")
        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(setlavel1)
        hlayout1 = QtGui.QHBoxLayout()
        hlayout2 = QtGui.QHBoxLayout()
        hlayout3 = QtGui.QHBoxLayout()
        hlayout1.addWidget(self.report_type1)
        hlayout1.addWidget(self.report_type2)
        hlayout2.addWidget(makebutton)
        hlayout2.addWidget(cancelbutton)
        hlayout3.addWidget(setlavel3)
        hlayout3.addWidget(self.namefield)
        vlayout.addWidget(self.checkbox1)
        vlayout.addWidget(self.combobox1)
        vlayout.addWidget(self.checkbox2)
        vlayout.addWidget(self.combobox2)
        vlayout.addWidget(self.checkbox3)
        vlayout.addWidget(self.combobox3)
        vlayout.addWidget(self.checkbox4)
        vlayout.addWidget(self.combobox4)
        vlayout.addWidget(self.checkbox5)
        vlayout.addWidget(self.combobox5)
        vlayout.addWidget(setlavel2)
        vlayout.addLayout(hlayout1)
        vlayout.addLayout(hlayout3)
        vlayout.addLayout(hlayout2)
        self.setLayout(vlayout)

    def create_combox(self):
        combobox = QtGui.QComboBox()
        self.oslist = get_result_oslist()
        if self.oslist is not None:
            combobox.addItems(self.oslist)
        return combobox

    def setCurrentIndex1(self, index):
        self.combobox1.setCurrentIndex(index)
        self.OSLIST["item1"] = self.oslist[index]

    def setCurrentIndex2(self, index):
        self.combobox2.setCurrentIndex(index)
        self.OSLIST["item2"] = self.oslist[index]

    def setCurrentIndex3(self, index):
        self.combobox3.setCurrentIndex(index)
        self.OSLIST["item3"] = self.oslist[index]

    def setCurrentIndex4(self, index):
        self.combobox4.setCurrentIndex(index)
        self.OSLIST["item4"] = self.oslist[index]

    def setCurrentIndex5(self, index):
        self.combobox5.setCurrentIndex(index)
        self.OSLIST["item5"] = self.oslist[index]

    def item_check(self):
        self.domakelist = []
        for key, value in self.checkitems.iteritems():
            if value.isChecked():
                self.domakelist.append(self.OSLIST[key])

    def check_report_name(self):
        self.text = self.namefield.text()
        report_total = getresultslist()
        if not self.text:
            QtGui.QMessageBox.warning(self, "警告",
                '报告名不能为空',
                QtGui.QMessageBox.Yes,
                QtGui.QMessageBox.No)
        elif self.text in report_total.keys():
            QtGui.QMessageBox.warning(self, "警告",
                '该名称已存在，请重新输入',
                 QtGui.QMessageBox.Yes,
                 QtGui.QMessageBox.No)
        else:
            return "TRUE"       
        
    def OnStart(self):
        self.item_check()
        if len(self.domakelist) < 1:
            QtGui.QMessageBox.warning(self, "警告",
            '至少选中一个对比项目',
            QtGui.QMessageBox.Yes,
            QtGui.QMessageBox.No)
        else:
            if self.report_type1.isChecked() or self.report_type2.isChecked():
                if self.report_type1.isChecked():
                    if self.check_report_name() is "TRUE":
                        mkhtml_custom_report(self.domakelist, self.text)
                        QtGui.QMessageBox.information(self, "提示", u"报告制作完毕")
                if self.report_type2.isChecked():
                    print("xls")
            else:
                QtGui.QMessageBox.warning(self, "警告",
                '至少选中一种报告类型',
                QtGui.QMessageBox.Yes,
                QtGui.QMessageBox.No)

    def OnCancel(self):
        self.close()


if __name__ == '__main__':
    application = QtGui.QApplication(sys.argv)
# window
    window = MakeReport()
    window.setWindowTitle('Stacked Widget')
    window.resize(280, 260)
    window.show()
    sys.exit(application.exec_())
