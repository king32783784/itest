#!/usr/bin/env python
# *-* coding=utf-8 *-*
import sys

from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebSettings, QWebPage
from common import *
from mkreport.data_operation import *


class SaveResult(QtGui.QDialog):
    def __init__(self):
        super(SaveResult,self).__init__()
        self.setWindowTitle(u'结果设置')
        self.setMinimumSize(360, 200)
        self.gridlayout = QtGui.QGridLayout()
        self.label0 = QtGui.QLabel(u"是否保存报告:")
        self.label1 = QtGui.QLabel(u"输入结果名称:" )
        self.gridlayout.addWidget(self.label0, 1, 0)
        self.gridlayout.addWidget(self.label1, 0, 0)
        self.textField = QtGui.QLineEdit()     #　创建单行文本框
        self.gridlayout.addWidget(self.textField, 0,1) # 添加文本框到布局组件
        self.radio1 = QtGui.QCheckBox(u"")
        self.gridlayout.addWidget(self.radio1, 1,1)
        self.okButton = QtGui.QPushButton(u"导入")  # 创建OK按钮
        self.gridlayout.addWidget(self.okButton, 3,0)   #添加按钮到布局组件　　
        self.cancelButton = QtGui.QPushButton(u"取消") # 创建cancel按钮
        self.gridlayout.addWidget(self.cancelButton, 3, 1)
        self.setLayout(self.gridlayout)

        self.connect(self.okButton, QtCore.SIGNAL('clicked()'), self.OnOk)
        self.connect(self.cancelButton, QtCore.SIGNAL('clicked()'), self.OnCancel)

    def save_report(self,dst):
        homepath = getlocatepath()
        reportrepository = os.path.join(homepath, "ReportRepository")
        dst = str(dst)
        report_path = os.path.join(reportrepository, dst)
        shutil.move("current-report", report_path) # 移动当前报告到报告仓库
        report_url = "file://" + "%s" % report_path + "/test.html"
        config = QSettings(".resultseting.ini", QSettings.IniFormat)
        config.remove("currentresult")
        config.remove("ontime")
        config.beginGroup("totalresults")
        config.setValue(dst, report_url)
        config.endGroup()

    def save_result(self,dst):
        dst = str(dst)
        update_database('test', dst)
        append_database_list('OSLIST', dst)

    def OnOk(self):
        resultlist = read_database('OSLIST')
        self.text = self.textField.text()  # 获取文本框中的内容
        if self.text in resultlist:
            QtGui.QMessageBox.warning(self, "警告",
            '名称已存在，请重新输入',
            QtGui.QMessageBox.Yes,
            QtGui.QMessageBox.No)
        else:
            self.save_result(self.text)
            if self.radio1.isChecked():
                self.save_report(self.text)
        self.done(1)

    def OnCancel(self):
        self.done(0)


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
        resultaddress = getcurrentresult()
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
        saveresult = SaveResult()
        saveresult.exec_()

    def search_edited(self, text):
        # finds all occurrences of the specified string
        find_flags = QWebPage.HighlightAllOccurrences | QWebPage.FindWrapsAroundDocument
        self.webview.findText('', find_flags)
        self.webview.findText(text, find_flags)

    def search_entered(self):
        # goes to the next occurrence of the specified string when the ENTER key is pressed
        find_flags = QWebPage.FindWrapsAroundDocument
        self.webview.findText(self.search.text(), find_flags)

#def main():
#    application = QtGui.QApplication(sys.argv)
#
#    # web browser
#    web_browser = CurentReport()
#    web_browser.show()
#    sys.exit(application.exec_())


#if __name__ == '__main__':
#    main()
