#!/usr/bin/env python
# *-* coding=utf-8 *-*
# Author: lipeng

import os
import time
import sys  # provides interaction with the Python interpreter

from PyQt4 import QtGui  # provides the graphic elements
from PyQt4.QtCore import Qt  # provides Qt identifiers
from subprocess import Popen, PIPE
from aqua.qsshelper import QSSHelper

from testitemset import *
from toolset.mainset import *
from helpinfo import HelpDialog
from sysload.machine_load import MachineLoadWidget
from sysload.mem_load import MemLoadWidget
from sysload.swap_load import SwapLoadWidget
from sysload.net_load import NetLoadWidget
from signals_window import SignalsWindow
from resulttab import *
from testdrive import *
from common import *
from mkresult import *
from mkreport.data_capture import *

from testset.perfmemset import *


class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.startstatus = "E"
        self.logstatus = "D"
        self.loadstatus = "D"
        self.resultstatus = "D"
        self.initcheck()
        # LCD number
        self.lcdnumber = QtGui.QLCDNumber()
        self.lcdnumber.setNumDigits(10)
        self.lcdnumber.display("2016")

        # toolbox
        self.window_load = LoadWindow()
        self.window_load.hide()
        self.createlogwindow()
        self.window_log.hide()
        self.createprogressbar()
        self.createbutton()
        self.createlabel()
        self.window_item = TestitemSet()
        self.setlayout()
 
    def createlogwindow(self):
        self.window_log = QtGui.QPlainTextEdit()
        self.window_log.setReadOnly(True)
        self.window_log.setStyleSheet('QPlainTextEdit { background-color: #102a21; color: white; }')

    def createbutton(self):
        self.startbutton = QToolButton()
        self.startbutton.setText(u"开始测试")
        self.startbutton.setIcon(QIcon("images/start.ico"))
        self.startbutton.setIconSize(QSize(25, 25))
        self.startbutton.setAutoRaise(True)
        self.startbutton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.startbutton.pressed.connect(self.starttest)
        
        self.mkresultbutton = QToolButton()
        self.mkresultbutton.setText(u"查看结果")
        self.mkresultbutton.setIcon(QIcon("images/results.ico"))
        self.mkresultbutton.setIconSize(QSize(25,25))
        self.mkresultbutton.setAutoRaise(True)
        self.mkresultbutton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.mkresultbutton.pressed.connect(self.resultwindow)

        self.logbutton = QToolButton()
        self.logbutton.setText(u"查看日志")
        self.logbutton.setIcon(QIcon("images/window.ico"))
        self.logbutton.setIconSize(QSize(25,25))
        self.logbutton.setAutoRaise(True)
        self.logbutton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.logbutton.pressed.connect(self.logwindow)

        self.loadbutton = QToolButton()
        self.loadbutton.setText(u"查看负载")
        self.loadbutton.setIcon(QIcon("images/load_72px.png"))
        self.loadbutton.setIconSize(QSize(25,25))
        self.loadbutton.setAutoRaise(True)
        self.loadbutton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.loadbutton.pressed.connect(self.loadwindow)

    def createprogressbar(self):
        self.progressbar = QtGui.QProgressBar()
        self.progressbar.setValue(0)

    def createdial(self):
        # 进度圈
        self.dial = QtGui.QDial()
        
    def createlabel(self):
        # 创建测试列表标签
        self.label_itemlist = QtGui.QLabel(u'选择测试项')
        self.label_log = QtGui.QLabel(u"查看日志")


    # 设置layout
    def setlayout(self):

        # 上部空白
        vspacer_left = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)

        # 右边空白区
        vspacer_right = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        
        # 上部layout
        vlayout_left = QtGui.QVBoxLayout()
        vlayout_left.addWidget(self.label_itemlist)
        vlayout_left.addWidget(self.window_item)

        #底部layout
        self.vlayout_footer = QtGui.QHBoxLayout()
        self.vlayout_footer.addWidget(self.startbutton)
        self.vlayout_footer.addWidget(self.mkresultbutton)
        self.vlayout_footer.addWidget(self.logbutton)
        self.vlayout_footer.addWidget(self.loadbutton)
        
        self.mainlayout = QtGui.QVBoxLayout()
        self.mainlayout.addLayout(vlayout_left)
        self.mainlayout.addLayout(self.vlayout_footer)
        self.mainlayout.addWidget(self.progressbar)
        self.mainlayout.addWidget(self.window_log)

       #   横向布局
        self.hlayout = QtGui.QHBoxLayout()
        self.hlayout.addLayout(self.mainlayout)
        self.hlayout.addWidget(self.window_load)

        # central widget
        central = QtGui.QWidget()
        central.setLayout(self.hlayout)
        self.setCentralWidget(central)

    @pyqtSlot()
    def resultwindow(self):
        self.window_result = ResultWindow()
        self.window_result.show()
    
    @pyqtSlot()
    def loadwindow(self):
        if self.loadstatus == "D":
            self.window_load.show()
            self.loadstatus = "E"
        else:
            self.window_load.hide()
            self.loadstatus = "D"

    @pyqtSlot()
    def starttest(self):
        if self.startstatus == "E":
            sumtestnum = sumtests()
            if sumtestnum > 0:
                self.window_log.appendPlainText("start")
                self.startbutton.setEnabled(False) # button禁用
              #  self.startbutton.setText(u"停止测试")
              #  self.startbutton.setIcon(QIcon("images/stop.ico"))
                self.createdial()
                save_testitem_args() # 保存当前测试项目及参数
                self.startstatus = "D"
                self.progress_num = 0
                self.progressbar.setValue(self.progress_num)
                self.progress_interval = 100 / sumtestnum
                self.window_log.show()
                writeconfig(".resultseting.ini", "ontime", "resultdirontime", "test")
                test = TestThread(self)
                test.setup(self.window_log)
                test.trigger.connect(self.update_text)
                test.start()
                runwindow = ResultWindow()
                runwindow.show()
            else:
                QtGui.QMessageBox.about(self, u"提示",
                u"至少选中一个测试项目")
             
        else:
            self.window_log.hide()
           # self.startbutton.setText(u"开始测试")
           # self.startbutton.setIcon(QIcon("images/start.ico"))
            self.startstatus = "E"
            self.progressbar.setValue(0)

    def update_text(self, info):
        if "finish" in info:
            self.progress_num += self.progress_interval
            self.progressbar.setValue(self.progress_num)
        self.window_log.appendPlainText("%s" % info)
        if info == "All tests end":
            self.progressbar.setValue(100)
            save_current_data()
            mk_current_report()
            self.write_result_config()

    # 写入当前报告地址
    def write_result_config(self):
        homepath = getlocatepath()
        defaultresult = os.path.join(homepath, "current-report/test.html")
        defaultresult = "file://" + defaultresult
        writeconfig(".resultseting.ini", "currentresult", 
                    "resultaddress", defaultresult)
        
    @pyqtSlot()
    def logwindow(self):
        pass

    def initcheck(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.remove("perf_testlists")

# 测试线程
class TestThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(TestThread, self).__init__(parent)

    def setup(self, testwindow):
        self.testwindow = testwindow
    
    def run(self):
        todotestlist = readtestlist()
        print(todotestlist)
        for testtype, todotest in todotestlist.items():
            for testitem in todotest:
                self.trigger.emit("Now test is %s" % testitem)
                testlist = getitemlist(testitem)
                for item in testlist:
                    self.trigger.emit("%s test start" % item)
                    testthread = TestDrive(testtype, item)
                    testthread.dotest()
                    self.trigger.emit("%s test finish" % item)
                self.trigger.emit("%s part test end" % testitem)
        self.trigger.emit("All tests end")

# 监控窗口
class LoadWindow(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self, parent)
        self.createloadcheck()
        self.setlayout()

    def setlayout(self):
    
       # 监控窗口布局
        self.vlayout_right = QtGui.QVBoxLayout()
        self.vlayout_right.addWidget(self.label_sysload)
        self.vlayout_right.addWidget(self.toolbox1)
        self.vlayout_right.addWidget(self.toolbox2)
        self.vlayout_right.addWidget(self.toolbox3)
        self.setLayout(self.vlayout_right)

    def createloadcheck(self):
        self.label_sysload = QtGui.QLabel(u'系统负载监控')
        # 创建资源监控窗口
        window_cpu = MachineLoadWidget()
        window_mem = MemLoadWidget()
        window_swap = SwapLoadWidget()
        window_net = NetLoadWidget()
        self.toolbox1 = QtGui.QToolBox()
        self.toolbox1.addItem(window_cpu, u"CPU负载")
        self.toolbox2 = QtGui.QToolBox()
        self.toolbox2.addItem(window_mem, u"MEM负载")
        self.toolbox2.addItem(window_swap, u"SWAP负载")
        self.toolbox3 = QtGui.QToolBox()
        self.toolbox3.addItem(window_net, u"网络负载")


class RuningWindow(QtGui.QWidget):
    def __init__(self):
        super(RuningWindow,self).__init__()
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

# 工具栏

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.main_widget = Window()
        self.setCentralWidget(self.main_widget)
 #       self.setFixedSize(self.width(), self.height()); #　禁用窗口大小调整

        self.menubar = self.menuBar() # 获得窗口的菜单条
        self.addmenu()

    def addmenu(self):

        self.settingmenu = self.menubar.addMenu(u'&设置')
        self.settingrun = self.settingmenu.addAction(u'运行项目')
        self.settingmenu.addSeparator()  # 添加分隔符
        self.settingbasic = self.settingmenu.addAction(u'基础配置')

        self.testitemmenu = self.menubar.addMenu(u'&测试项')
        self.testiteminfo = self.testitemmenu.addAction(u'测试项说明')

        self.helpmenu = self.menubar.addMenu(u'&帮助')
        self.helpuse = self.helpmenu.addAction(u'&使用说明')
        self.helpabout = self.helpmenu.addAction(u'关于')
        self.filemenu = self.menubar.addMenu(u'关闭') # 添加文件菜单
        self.filemenuexit = self.filemenu.addAction(u'终止退出') # 添加退出命令
        self.creatmenuaction()

    def creatmenuaction(self):
        self.connect(self.filemenuexit, QtCore.SIGNAL('triggered()'), self.Onmenuexit)
        self.connect(self.settingrun, QtCore.SIGNAL('triggered()'), self.Onsettingrun)
        self.connect(self.settingbasic, QtCore.SIGNAL('triggered()'), self.Onsettingbasic)
        self.connect(self.testiteminfo, QtCore.SIGNAL('triggered()'), self.Ontestiteminfo)
        self.connect(self.helpabout, QtCore.SIGNAL('triggered()'), self.Onhelpabout)
        self.connect(self.helpuse, QtCore.SIGNAL('triggered()'), self.Onhelpuse)

    def Onmenuexit(self):
        message = QtGui.QMessageBox.question(self, u'提示:', u'确认要退出?',
                                   QtGui.QMessageBox.Yes,
                                   QtGui.QMessageBox.No,
                                   QtGui.QMessageBox.Cancel)
        if message == QtGui.QMessageBox.Yes:
            self.close()

    def Onsettingrun(self):
        print("setting run")

    def Onsettingbasic(self):
        basicset = StackDialog()
        basicset.show()
        basicset.exec_()

    def Ontestiteminfo(self):
        print("testitem info")

    def Onhelpabout(self):
        print("test help")
        QtGui.QMessageBox.about(self, u'关于Lpbs-i', '\n\n  Lpbs-i是一个Linux系统评测工具，主要包括linux系统的信息检测、性能评测、稳定性检测、基本能稳定性检测主要包括处理器&内存高负载压力测试、IO高负载压力测试、网络高负载压力测试、显示高负载压力测试、线程高负载压力测试、内核高负载压力测试。\n\n  基本功能检测主要包括ltp功能测试，具体测试项见ltp。\n\n  Lpbs-i的测试内容在不断完善和更新。\n\n\n\n 版本：V1.0 \n\n作者：peng.lee \n\nBug:https://github.com/')

    def Onhelpuse(self):
        print("test use")

class SetHelp(HelpDialog):

    def additem(self):
        self.listWidget = QListWidget()
        self.listWidget.insertItem(0, self.tr(u"Lpbs-i帮助"))

    def addlabel(self):
        self.label1 = QLabel(self.tr(u"""使用说明(待补)"""))
        self.stack = QStackedWidget()
        self.stack.addWidget(sefl.label1)

def main():
    # 清除之前的temp文件
    initenv()
    # 创建应用，并接收命令行参数
    application = QtGui.QApplication(sys.argv)

    # 创建窗口，并设置基本属性
    window = MainWindow() # 生成Window对象
    window.setWindowTitle(u'普华Linux测试')  # 窗口标题
    window.resize(900, 600)  # 窗口大小

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("images/title.ico"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
    window.setWindowIcon(icon)

    # 导入和设置Qt风格
    qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
    window.setStyleSheet(qss)
   # window.setWindowFlags(Qt.FramelessWindowHint)
    window.setWindowFlags(Qt.WindowTitleHint)
    window.setWindowFlags(Qt.WindowMinimizeButtonHint)

    window.show()  #窗口显示

    # 运行应用并等待返回结束
    sys.exit(application.exec_())


if __name__ == '__main__':
    createresultdir()
    createdatarepository()
    main()
