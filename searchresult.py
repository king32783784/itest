#*-*coding=utf-8*-*

import sys

from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4.QtCore import *
from common import *

class SearchResult(QtGui.QWidget):
    def __init__(self, parent=None):
        super(SearchResult, self).__init__(parent)
        self.resultslist = getresultslist()
        self.createwebview()
        # combobox
        self.createcombobox()
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
        resultaddress = self.getcurrentresult()
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

    def getcurrentresult(self):
        config = QSettings(".resultseting.ini", QSettings.IniFormat)
        result_address = {}
        result_address["address"] = config.value("currentresult/" + "resultaddress").toString()[0:]
        result_address["name"] = config.value("currentresult/" + "resultname").toString()[0:]
        return result_address

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
        self.webview.load(QtCore.QUrl(self.addresslist[0]))
        self.combobox.activated.connect(self.setCurrentIndex)

    def setCurrentIndex(self, index):
        self.combobox.setCurrentIndex(index)
        self.labelindex = index
        self.webview.load(QtCore.QUrl(self.addresslist[index]))
        print(self.labelindex)

#application = QtGui.QApplication(sys.argv)

# window
#window = SearchResult()
#window.setWindowTitle('Stacked Widget')
#window.resize(280, 260)
#window.show()

#sys.exit(application.exec_())
