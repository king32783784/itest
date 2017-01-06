#!/usr/bin/env python
# *-* coding=utf-8 *-*
import sys

from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import QColor
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebSettings, QWebPage

# window subclass
class CurentReport(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # window properties
        self.setWindowTitle(u'当前结果')
        self.setMinimumSize(400, 400)
        self.resize(600, 500)
        self.showMaximized()

        # 生成网页浏览器
        self.webview = QtWebKit.QWebView(self)
        self.webview.setWindowOpacity(90)
        palette1 = QtGui.QPalette()
        palette1.setColor(self.backgroundRole(), QColor("#57760e"))  # 设置背景色
        self.setPalette(palette1)
        self.setAutoFillBackground(True)

        # toolbar widgets (instantiated in the init_toolbar() method)
        self.search = None

        # toolbar
        self.toolbar = QtGui.QToolBar()
        self.init_toolbar()
        self.addToolBar(self.toolbar)

        # central widget
        self.setCentralWidget(self.webview)

    def init_toolbar(self):

        # 测试结果名称
        resultaddress = self.getcurrentresult()
        self.result_label = QtGui.QLabel(u'结果名称',self)
        self.result_bar = QtGui.QLineEdit(self)
        self.result_bar.setText(u"%s"%resultaddress["name"])
     #   self.address_bar.setReadOnly(True)
        # 导航至测试结果
        self.webview.load(QtCore.QUrl(resultaddress["address"]))
        # 搜索框
        self.search = QtGui.QLineEdit(self)
        self.search.setMaximumWidth(200)
        #  signals
        self.search.textEdited.connect(self.search_edited)
        self.search.returnPressed.connect(self.search_entered)
        #  search label
        label_search = QtGui.QLabel(u'查找', self)
        label_search.setBuddy(self.search)

        # 结果保存
        self.saveresult = QtGui.QPushButton(u"导入结果") 
        self.saveresult.pressed.connect(self.saveresultslot)
        self.toolbar.addWidget(self.result_label)
        self.toolbar.addWidget(self.result_bar)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(label_search)
        self.toolbar.addWidget(self.search)
        self.toolbar.addWidget(self.saveresult)
        self.toolbar.addSeparator()

    def saveresultslot(self):
        pass

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


def main():
    application = QtGui.QApplication(sys.argv)

    # web browser
    web_browser = CurentReport()
    web_browser.show()

    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
