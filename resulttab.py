#*-*coding=utf-8*-*
import sys
import os   # provides interaction with the Python interpreter
from aqua.qsshelper import QSSHelper
from PyQt4 import QtGui  # provides the graphic elements
from resultshow import *
from searchresult import *
from common import *

class ResultWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ResultWindow, self).__init__(parent)
        self.setWindowTitle(u"结果管理器")
        self.resize(900,540)
        self.setAttribute(Qt.WA_DeleteOnClose)
        Icon = QtGui.QIcon()
        titleico = os.path.join(HOMEPATH, "images/title.ico")
        Icon.addPixmap(QtGui.QPixmap(titleico),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(Icon)
        # 创建tab
        self.tabwidget = QtGui.QTabWidget()

        # adds the tabs to the tabwidget
        self.createtab()

        # creates a vertical box layout for the window
        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(self.tabwidget)  # adds the tabwidget to the layout
        self.setLayout(vlayout)  # sets the window layout

    def createtab(self):
        curentreport = CurentReport()
        searchreport = SearchResult()
        makereport = MakeReport()
        self.tabwidget.addTab(curentreport, u'当前结果')
        self.tabwidget.addTab(searchreport, '报告查询')
#        self.tabwidget.addTab(QtGui.QPlainTextEdit(), '单项结果')
        self.tabwidget.addTab(makereport, '制作报告')


if __name__ == "__main__":
    application = QtGui.QApplication(sys.argv)
    window = ResultWindow()
    window.setWindowTitle('QTabWidget')  # title
    window.resize(1024, 320)  # size
    window.show()  # shows the window
    sys.exit(application.exec_())
