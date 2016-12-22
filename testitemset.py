#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from aqua.qsshelper import QSSHelper
from testset.perfcpuset import *
from testset.perfmemset import *
from testset.perfioset import *
from testset.perfthreadset import *
from testset.perfsystemset import *
from testset.perfkernelset import *
from testset.perfbrowserset import *
from testset.perfjavaset import *
from testset.perf2dset import *
from testset.perf3dset import *

class TestitemSet(QToolBox):

    """ 
              support test list
        info test :
        0:CPU 1:MEM 2:HDD 3:Graphic 4:kernel
        func test:
        0:ltp-kernel 1:ltp-cmds 2:ltp-service 3:ltp-others
        perf test:
        0:perf-cpu 1:perf-mem 2:perf-io 3:perf-thread 4:perf-system
        5:perf-kernel 6:perf-browser 7:perf-java 8:2d 9:3d 10:net
        stress test:
        0:cpu 1:mem 2:io 3:system 4:2d 5:3d 6:net   
        
    """
    def __init__(self, parent=None):
        super(TestitemSet, self).__init__(parent)

        self.setWindowTitle(u"普华测试套件")
        self.mkperfsignalist()
        self.mkpcheckslotlist()
        self.mkinfosignalist()
        self.mkfuncsignalist()
        self.mkstresssignalist()
        self.create_group_items()
        self.create_toolBox()

    def create_group_items(self):
        self.group_list = []
        group_info = [[u"CPU", "images/info.png"],
                             ["MEM", "images/info.png"],
                             ["HDD", "images/info.png"],
                             ["Graphic", "images/info.png"],
                             ["Kernel", "images/info.png"]]

        group_func = [["Ltp-kernel", "images/function.ico"],
                             ["Ltp-cmds", "images/function.ico"],
                             ["Ltp-service", "images/function.ico"],
                             ["Ltp-others", "images/function.ico"]]

        group_perf = [[u"CPU运算", "images/performance.gif"],
                      [u"MEM操作", "images/performance.gif"],
                      [u"I/O操作", "images/performance.gif"],
                      [u"线程管理", "images/performance.gif"],
                      [u"系统基准", "images/performance.gif"],
                      [u"内核", "images/performance.gif"],
                      [u"浏览器", "images/performance.gif"],
                      [u"JAVA", "images/performance.gif"],
                      [u"2D", "images/performance.gif"],
                      [u"3D", "images/performance.gif"],
                      [u"网络", "images/performance.gif"]]

        group_stre = [["CPU","images/stress.gif"],
                      ["MEM","images/stress.gif"],
                      ["THREAD","images/stress.gif"],
                      ["IO", "images/stress.gif"],
                      ["2D", "images/stress.gif"],
                      ["3D", "images/stress.gif"],
                      ["Net", "images/stress.gif"]]

        self.group_list.append(group_info)
        self.group_list.append(group_func)
        self.group_list.append(group_perf)
        self.group_list.append(group_stre)

    def create_toolBox(self):
        self.toolbox_list = []
        self.checkbox_list = []
        self.toolbox_info_list = []
        self.toolbox_func_list = []
        self.toolbox_perf_list = []
        self.toolbox_stress_list = []
        self.checkbox_info_list = []
        self.checkbox_func_list = []
        self.checkbox_perf_list = []
        self.checkbox_stress_list = []
        for i,group in  enumerate(self.group_list):
            if i == 0:
                for j, item in enumerate(group):
                    toolButton = QToolButton()
                    toolButton.setText(self.tr(item[0]))
                    toolButton.setIcon(QIcon(item[1]))
                    toolButton.setIconSize(QSize(45,45))
                    toolButton.setAutoRaise(True)
                    toolButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                    toolButton.pressed.connect(self.infosingallist[j])
                    self.toolbox_info_list.append(toolButton)
                    check = QtGui.QCheckBox('')
                    self.checkbox_info_list.append(check)
            elif i == 1:
                for j, item in enumerate(group):
                    toolButton = QToolButton()
                    toolButton.setText(self.tr(item[0]))
                    toolButton.setIcon(QIcon(item[1]))
                    toolButton.setIconSize(QSize(45,45))
                    toolButton.setAutoRaise(True)
                    toolButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                    toolButton.pressed.connect(self.funcsingallist[j])
                    self.toolbox_func_list.append(toolButton)
                    check = QtGui.QCheckBox('')
                    self.checkbox_func_list.append(check)
            elif i == 2:
                for j, item in enumerate(group):
                    toolButton = QToolButton()
                    toolButton.setText(self.tr(item[0]))
                    toolButton.setIcon(QIcon(item[1]))
                    toolButton.setIconSize(QSize(45, 45))
                    toolButton.setAutoRaise(True)
                    toolButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                    toolButton.pressed.connect(self.perfsingallist[j])
                    self.toolbox_perf_list.append(toolButton)
                    check = QtGui.QCheckBox('')
                    check.clicked.connect(self.pcheckslotlist[j])
                    self.checkbox_perf_list.append(check)
            elif i == 3:
                for j, item in enumerate(group):
                    toolButton = QToolButton()
                    toolButton.setText(self.tr(item[0]))
                    toolButton.setIcon(QIcon(item[1]))
                    toolButton.setIconSize(QSize(45,45))
                    toolButton.setAutoRaise(True)
                    toolButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                    toolButton.pressed.connect(self.stresssingallist[j])
                    self.toolbox_stress_list.append(toolButton)
                    check = QtGui.QCheckBox('')
                    self.checkbox_stress_list.append(check)
            else:
                pass
        self.toolbox_list.append(self.toolbox_info_list)
        self.toolbox_list.append(self.toolbox_func_list)
        self.toolbox_list.append(self.toolbox_perf_list)
        self.toolbox_list.append(self.toolbox_stress_list)
        self.checkbox_list.append(self.checkbox_info_list)
        self.checkbox_list.append(self.checkbox_func_list)
        self.checkbox_list.append(self.checkbox_perf_list)
        self.checkbox_list.append(self.checkbox_stress_list)
  
        group_name_list = [u"信息",u"功能", u"性能", u"压力"]
        self.groupbox_list = []
        for index,group_toolbox in enumerate(self.toolbox_list): 
            groupbox = QGroupBox()
            vlayout = QGridLayout(groupbox)
            vlayout.setMargin(10)
            vlayout.setAlignment(Qt.AlignCenter)
            for i, toolbutton in enumerate(group_toolbox):
                x = (i / 3) * 2
                y = i % 3
                z = (i / 3) * 2 + 1
                vlayout.addWidget(toolbutton,x,y)
                vlayout.addWidget(self.checkbox_list[index][i],z,y)
            self.addItem(groupbox, self.tr(group_name_list[index]))
            groupbox.contentHorizontalAlignment = 0

    def mkinfosignalist(self):
        self.infosingallist = []
        self.infosingallist.append(self.setinfocpu)
        self.infosingallist.append(self.setinfomem)
        self.infosingallist.append(self.setinfohdd)
        self.infosingallist.append(self.setinfographic)
        self.infosingallist.append(self.setinfokernel)

    def mkfuncsignalist(self):
        self.funcsingallist = []
        self.funcsingallist.append(self.setfunckernel)
        self.funcsingallist.append(self.setfunccmds)
        self.funcsingallist.append(self.setfuncservice)
        self.funcsingallist.append(self.setfuncothers)

    def mkperfsignalist(self):
        self.perfsingallist = []
        self.perfsingallist.append(self.setperfcpu)
        self.perfsingallist.append(self.setperfmem)
        self.perfsingallist.append(self.setperfio)
        self.perfsingallist.append(self.setperfthread)
        self.perfsingallist.append(self.setperfsystem)
        self.perfsingallist.append(self.setperfkernel)
        self.perfsingallist.append(self.setperfbrowser)
        self.perfsingallist.append(self.setperfjava)
        self.perfsingallist.append(self.setperf2d)
        self.perfsingallist.append(self.setperf3d)
        self.perfsingallist.append(self.setperfnet)

    def mkpcheckslotlist(self):
        self.pcheckslotlist = []
        self.pcheckslotlist.append(self.checkperfcpu)
        self.pcheckslotlist.append(self.checkperfmem)
        self.pcheckslotlist.append(self.checkperfio)
        self.pcheckslotlist.append(self.checkperfthread)
        self.pcheckslotlist.append(self.checkperfsystem)
        self.pcheckslotlist.append(self.checkperfkernel)
        self.pcheckslotlist.append(self.checkperfbrowser)
        self.pcheckslotlist.append(self.checkperfjava)
        self.pcheckslotlist.append(self.checkperf2d)
        self.pcheckslotlist.append(self.checkperf3d)
        self.pcheckslotlist.append(self.checkperfnet)

    def mkstresssignalist(self):
        self.stresssingallist = []
        self.stresssingallist.append(self.setstresscpu)
        self.stresssingallist.append(self.setstressmem)
        self.stresssingallist.append(self.setstressio)
        self.stresssingallist.append(self.setstresssystem)
        self.stresssingallist.append(self.setstress2d)
        self.stresssingallist.append(self.setstress3d)
        self.stresssingallist.append(self.setstressnet)

    # Info-test slot
    @pyqtSlot()
    def setinfocpu(self):
        pass

    @pyqtSlot()
    def setinfomem(self):
        pass
    
    @pyqtSlot()
    def setinfohdd(self):
        pass

    @pyqtSlot()
    def setinfographic(self):
        pass

    @pyqtSlot()
    def setinfokernel(self):
        pass

    # Func-test slot
    @pyqtSlot()
    def setfunckernel(self):
        pass

    @pyqtSlot()
    def setfunccmds(self):
        pass

    @pyqtSlot()
    def setfuncservice(self):
        pass

    @pyqtSlot()
    def setfuncothers(self):
        pass

    # Perf-test slot
    @pyqtSlot()
    def setperfcpu(self):
        cpu = PerfcpuSet()
        qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
        cpu.setStyleSheet(qss)
        cpu.exec_()

    @pyqtSlot()
    def setperfmem(self):
        mem = PerfmemSet()
        qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
        mem.setStyleSheet(qss)
        mem.exec_()
   
    @pyqtSlot()
    def setperfio(self):
        io = PerfioSet()
        qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
        io.setStyleSheet(qss)
        io.exec_()

    @pyqtSlot()
    def setperfthread(self):
        thread = PerfthreadSet()
        qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
        thread.setStyleSheet(qss)
        thread.exec_()

    @pyqtSlot()
    def setperfsystem(self):
        system = PerfsystemSet()
        qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
        system.setStyleSheet(qss)
        system.exec_()

    @pyqtSlot()
    def setperfkernel(self):
        kernel = PerfkernelSet()
        qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
        kernel.setStyleSheet(qss)
        kernel.exec_()

    @pyqtSlot()
    def setperfbrowser(self):
        browser = PerfbrowserSet()
        qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
        browser.setStyleSheet(qss)
        browser.exec_()

    @pyqtSlot()
    def setperfjava(self):
        java = PerfjavaSet()
        qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
        java.setStyleSheet(qss)
        java.exec_()

    @pyqtSlot()
    def setperf2d(self):
        test2d = Perf2dSet()
        qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
        test2d.setStyleSheet(qss)
        test2d.exec_()

    @pyqtSlot()
    def setperf3d(self):
        test3d = Perf3dSet()
        qss = QSSHelper.open_qss(os.path.join('aqua', 'aqua.qss'))
        test3d.setStyleSheet(qss)
        test3d.exec_()

    @pyqtSlot()
    def setperfnet(self):
        pass

    # perf-check slot
    @pyqtSlot()
    def checkperfcpu(self):
        if self.checkbox_perf_list[0].isChecked():
            self.addcheck("perfcpu", "perf_testlists")
        else:
            self.removecheck("perfcpu", "perf_testlists")

    @pyqtSlot()
    def checkperfmem(self):
        if self.checkbox_perf_list[1].isChecked():
            self.addcheck("perfmem", "perf_testlists")
        else:
            self.removecheck("perfmem", "perf_testlists")

    @pyqtSlot()
    def checkperfio(self):
        if self.checkbox_perf_list[2].isChecked():
            self.addcheck("perfio", "perf_testlists")
        else:
            self.removecheck("perfio", "perf_testlists")

    @pyqtSlot()
    def checkperfthread(self):
        if self.checkbox_perf_list[3].isChecked():
            self.addcheck("perfthread", "perf_testlists")
        else:
            self.removecheck("perfthread", "perf_testlists")

    @pyqtSlot()
    def checkperfsystem(self):
        if self.checkbox_perf_list[4].isChecked():
            self.addcheck("perfsystem", "perf_testlists")
        else:
            self.removecheck("perfsystem", "perf_testlists")
   
    @pyqtSlot()
    def checkperfkernel(self):
        if self.checkbox_perf_list[5].isChecked():
            self.addcheck("perfkernel", "perf_testlists")
        else:
            self.removecheck("perfkernel", "perf_testlists")

    @pyqtSlot()
    def checkperfbrowser(self):
        if self.checkbox_perf_list[6].isChecked():
            self.addcheck("perfbrowser", "perf_testlists")
        else:
            self.removecheck("perfbrowser", "perf_testlists")

    @pyqtSlot()
    def checkperfjava(self):
        if self.checkbox_perf_list[7].isChecked():
            self.addcheck("perfjava", "perf_testlists")
        else:
            self.removecheck("perfjava", "perf_testlists")

    @pyqtSlot()
    def checkperf2d(self):
        if self.checkbox_perf_list[8].isChecked():
            self.addcheck("perf2d", "perf_testlists")
        else:
            self.removecheck("perf2d", "perf_testlists")


    @pyqtSlot()
    def checkperf3d(self):
        if self.checkbox_perf_list[9].isChecked():
            self.addcheck("perf3d", "perf_testlists")
        else:
            self.removecheck("perf3d", "perf_testlists")

    @pyqtSlot()
    def checkperfnet(self):
        if self.checkbox_perf_list[10].isChecked():
            self.addcheck("perfnet", "perf_testlists")
        else:
            self.removecheck("perfnet", "perf_testlists")

    # stress-test Slot
    @pyqtSlot()
    def setstresscpu(self):
        pass

    @pyqtSlot()
    def setstressmem(self):
        pass

    @pyqtSlot()
    def setstressio(self):
        pass

    @pyqtSlot()
    def setstresssystem(self):
        pass

    @pyqtSlot()
    def setstress2d(self):
        pass

    @pyqtSlot()
    def setstress3d(self):
        pass

    @pyqtSlot()
    def setstressnet(self):
        pass

    def addcheck(self, testitem, testgroup):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
      #  self.config.beginGroup("perf_testlists")
        self.config.beginGroup(testgroup)
        self.config.setValue(testitem,"")
        self.config.endGroup()

    def removecheck(self, testitem, testgroup):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.beginGroup(testgroup)
        self.config.remove(testitem)
        self.config.endGroup()
    
def main():
    app = QApplication(sys.argv)
    form = TestitemSet()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

