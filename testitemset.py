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
from testset.stbcpuset import *
from testset.stbmemset import *
from testset.stbsystemset import *
from testset.stbioset import *
from testset.stbthreadset import *
from testset.stb2dset import *
from testset.stb3dset import *
from common import *

class TestitemSet(QToolBox):

    """ 
              support test list
        info test :
        0:HW 1:SW 2:ALL
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
        self.mkperfsignalist()
        self.mkpcheckslotlist()
        self.mkinfosignalist()
        self.mkicheckslotlist()
        self.mkfuncsignalist()
        self.mkfcheckslotlist()
        self.mkstresssignalist()
        self.mkscheckslotlist()
        self.create_group_items()
        self.create_toolBox()

    def create_group_items(self):
        self.group_list = []
        group_info = [[u"HW", "images/info.png"],
                             ["SW", "images/info.png"],
                             ["ALL", "images/info.png"]]

        group_func = [["Ltp-kernel", "images/function.ico"]]

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

        group_stre = [["SYSTEM", "images/stress.gif"],
                      ["CPU","images/stress.gif"],
                      ["MEM","images/stress.gif"],
                      ["THREAD","images/stress.gif"],
                      ["IO", "images/stress.gif"],
                      ["2D", "images/stress.gif"],
                      ["3D", "images/stress.gif"]]

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
                    check = QtGui.QRadioButton('')
                    check.clicked.connect(self.icheckslotlist[j])
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
                    check.clicked.connect(self.fcheckslotlist[j])
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
                    check.clicked.connect(self.scheckslotlist[j])
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

    # 信息检查项目设置信号
    def mkinfosignalist(self):
        self.infosingallist = []
        self.infosingallist.append(self.setinfohw)
        self.infosingallist.append(self.setinfosw)
        self.infosingallist.append(self.setinfoall)

    # 信息检查项目选中信号
    def mkicheckslotlist(self):
        self.icheckslotlist = []
        self.icheckslotlist.append(self.checkhwinfo)
        self.icheckslotlist.append(self.checkswinfo)
        self.icheckslotlist.append(self.checkallinfo)
      
    # 功能项目设置信号
    def mkfuncsignalist(self):
        self.funcsingallist = []
        self.funcsingallist.append(self.setfunckernel)

    # 功能项目选中信号
    def mkfcheckslotlist(self):
        self.fcheckslotlist = []
        self.fcheckslotlist.append(self.checkkernelfun)

    # 性能项目设置信号
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

    # 性能项目选中信号
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

    # 压力项目设置信号
    def mkstresssignalist(self):
        self.stresssingallist = []
        self.stresssingallist.append(self.setstresssystem)
        self.stresssingallist.append(self.setstresscpu)
        self.stresssingallist.append(self.setstressmem)
        self.stresssingallist.append(self.setstressthread)
        self.stresssingallist.append(self.setstressio)
        self.stresssingallist.append(self.setstress2d)
        self.stresssingallist.append(self.setstress3d)
    
    # 压力项目选中信号
    def mkscheckslotlist(self):
        self.scheckslotlist = []
        self.scheckslotlist.append(self.checkstresssystem)
        self.scheckslotlist.append(self.checkstresscpu)
        self.scheckslotlist.append(self.checkstressmem)
        self.scheckslotlist.append(self.checkstressthread)
        self.scheckslotlist.append(self.checkstressio)
        self.scheckslotlist.append(self.checkstress2d)
        self.scheckslotlist.append(self.checkstress3d)

    # Info-test slot
    @pyqtSlot()
    def setinfohw(self):
        pass

    @pyqtSlot()
    def setinfosw(self):
        pass
    
    @pyqtSlot()
    def setinfoall(self):
        pass

    # Info-check slot
    @pyqtSlot()
    def checkhwinfo(self):
        if self.checkbox_info_list[0].isChecked():
            self.addcheck("info", "info_testlists")
            self.infoinit()
            writeconfig(SET_FILE, "info-user" , "hw", "E")
        else:
            self.removecheck("info", "info_testlists")
            self.removecheck("hw", "info_user")

    @pyqtSlot()
    def checkswinfo(self):
        if self.checkbox_info_list[1].isChecked():
            self.addcheck("info", "info_testlists")
            self.infoinit()
            writeconfig(SET_FILE, "info-user" , "sw", "E")
        else:
            self.removecheck("info", "info_testlists")
            self.removecheck("sw", "info_user")

    @pyqtSlot()
    def checkallinfo(self):
        if self.checkbox_info_list[2].isChecked():
            self.config = QSettings(".testseting.ini", QSettings.IniFormat)
            self.infoinit()
            self.addcheck("info", "info_testlists")
            writeconfig(SET_FILE, "info-user" , "all", "E")
        else:
            self.removecheck("info", "info_testlists")
            self.removecheck("all", "info-user")

    # Func-test slot
    @pyqtSlot()
    def setfunckernel(self):
        pass

   # Func-check slot
    @pyqtSlot()
    def checkkernelfun(self):
        if self.checkbox_func_list[0].isChecked():
            print("test check func")
            self.addcheck("ltpbasic", "func_testlists")
        else:
            self.removecheck("ltpbasic", "func_testlists")

    # Perf-test slot
    @pyqtSlot()
    def setperfcpu(self):
        cpu = PerfcpuSet()
        cpu.exec_()

    @pyqtSlot()
    def setperfmem(self):
        mem = PerfmemSet()
        mem.exec_()
   
    @pyqtSlot()
    def setperfio(self):
        io = PerfioSet()
        io.exec_()

    @pyqtSlot()
    def setperfthread(self):
        thread = PerfthreadSet()
        thread.exec_()

    @pyqtSlot()
    def setperfsystem(self):
        system = PerfsystemSet()
        system.exec_()

    @pyqtSlot()
    def setperfkernel(self):
        kernel = PerfkernelSet()
        kernel.exec_()

    @pyqtSlot()
    def setperfbrowser(self):
        browser = PerfbrowserSet()
        browser.exec_()

    @pyqtSlot()
    def setperfjava(self):
        java = PerfjavaSet()
        java.exec_()

    @pyqtSlot()
    def setperf2d(self):
        test2d = Perf2dSet()
        test2d.exec_()

    @pyqtSlot()
    def setperf3d(self):
        test3d = Perf3dSet()
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
    def setstresssystem(self):
        testsystem = StbsystemSet()
        testsystem.exec_()

    @pyqtSlot()
    def setstresscpu(self):
        testcpu = StbcpuSet()
        testcpu.exec_()

    @pyqtSlot()
    def setstressmem(self):
        testmem = StbmemSet()
        testmem.exec_()

    @pyqtSlot()
    def setstressio(self):
        testio = StbioSet()
        testio.exec_()

    @pyqtSlot()
    def setstressthread(self):
        testthread = StbthreadSet()
        testthread.exec_()

    @pyqtSlot()
    def setstress2d(self):
        test2d = Stb2dSet()
        test2d.exec_()

    @pyqtSlot()
    def setstress3d(self):
        test3d = Stb3dSet()
        test3d.exec_()

    # stress-check slot
    @pyqtSlot()
    def checkstresssystem(self):
        if self.checkbox_stress_list[0].isChecked():
            self.addcheck("stresssystem", "stress_testlists")
        else:
            self.removecheck("stresssystem", "stress_testlists")

    @pyqtSlot()
    def checkstresscpu(self):
        if self.checkbox_stress_list[1].isChecked():
            self.addcheck("stresscpu", "stress_testlists")
        else:
            self.removecheck("stresssystem", "stress_testlists")

    @pyqtSlot()
    def checkstressmem(self):
        if self.checkbox_stress_list[2].isChecked():
            self.addcheck("stressmem", "stress_testlists")
        else:
            self.removecheck("stresssystem", "stress_testlists")

    @pyqtSlot()
    def checkstressio(self):
        if self.checkbox_stress_list[4].isChecked():
            self.addcheck("stressio", "stress_testlists")
        else:
            self.removecheck("stresssystem", "stress_testlists")

    @pyqtSlot()
    def checkstressthread(self):
        if self.checkbox_stress_list[3].isChecked():
            self.addcheck("stressthread", "stress_testlists")
        else:
            self.removecheck("stressthread", "stress_testlists")

    @pyqtSlot()
    def checkstress2d(self):
        if self.checkbox_stress_list[5].isChecked():
            self.addcheck("stress2d", "stress_testlists")
        else:
            self.removecheck("stress2d", "stress_testlists")

    @pyqtSlot()
    def checkstress3d(self):
        if self.checkbox_stress_list[6].isChecked():
            self.addcheck("stress3d", "stress_testlists")
        else:
            self.removecheck("stress3d", "stress_testlists")

    def addcheck(self, testitem, testgroup):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
      #  self.config.beginGroup("perf_testlists")
        self.config.beginGroup(testgroup)
        self.config.setValue(testitem,"")
        self.config.endGroup()

    def infoinit(self):
        self.config = QSettings(".testseting.ini", QSettings.IniFormat)
        self.config.remove("info-user") # 移除info

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

