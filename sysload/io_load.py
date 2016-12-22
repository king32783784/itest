# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

try:
    str = unicode
except NameError:
    pass

import os, io,sys,time
from subprocess import Popen, PIPE
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class IoLoadWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self.collectMachineLoad)
        self.loads = []
        self.rular = 128
        self.maxLength = 400 # 表长
        self.pointDistance = 4 # 网格之间的间隔
        self.updateInterval = 500 # 变化的时间间隔
        self.timer.setInterval(self.updateInterval)
        self.timer.start()
        self.machineLoad = MachineLoad()
        self.boxWidth = 90 # 柱状图宽度

    def finalize(self):
        self.timer.stop()
        self.loads = []

    def collectMachineLoad(self):
        rate = self.machineLoad.getLoad()
        self.loads.insert(0, rate)
        if len(self.loads) > self.maxLength:
            self.loads.pop( - 1)
        if self.isVisible():
            self.update() # 刷新

    def paintEvent(self, event):
        QWidget.paintEvent(self, event)
        width, height = self.width(), self.height() #设置 宽度 高度
        # rx折线
        polygon = QPolygon()  # 初始图形
        for i, data in enumerate(self.loads):
            rxdate = data[0]
            rate = rxdate / self.rular
            x = width - i * self.pointDistance #x位置
            y = height - rate * height  # 根据rate计算高度
            if y < 0:
                y = 5
            if x < self.boxWidth:
                break
            polygon.append(QPoint(x, y))

        # tx 折线
        polygon1= QPolygon()  # 初始图形
        for i, data in enumerate(self.loads):
            txdate = data[1]
            rate = txdate / self.rular
            x = width - i * self.pointDistance # x位置
            y = height - rate * height   # 根据rate计算高度
            if y < 0:
                y = 5
            if x < self.boxWidth:
                break
            polygon1.append(QPoint(x, y))
        painter = QPainter(self)
        pen = QPen()   # 生成画笔对象
        pen1 = QPen()  # 
        pen.setColor(Qt.white) # 设置画笔颜色为白色
        pen1.setColor(Qt.black) #
        painter.setPen(pen1)   # 选择画笔
        painter.setRenderHint(QPainter.Antialiasing, True) # 设置反走样
        #画网格
        painter.setOpacity(0.5) # 透明度
        gridSize = self.pointDistance * 4 # 网格宽度
        deltaX = (width - self.boxWidth) % gridSize  + self.boxWidth  # x线初始坐标
        deltaY = height % gridSize # y线初始坐标（空余）
        for i in range(int(width / gridSize)):   # 网格数 
            x = deltaX + gridSize * i        # x坐标
            painter.drawLine(x, 0, x, height) # 画经线
        for j in range(int(height / gridSize)):  
            y = j * gridSize + deltaY  # y坐标
            painter.drawLine(self.boxWidth, y, width, y) # 画维线

        #画折线
        pen.setColor(Qt.darkBlue)  # 改变画笔颜色
        pen.setWidth(2)     # 设置线宽
        painter.setPen(pen)  # 确定画笔
        painter.setOpacity(1)  # 透明度
        painter.drawPolyline(polygon) # 画折线
        # 画第二条折线
        pen.setColor(Qt.red) # 改变画笔颜色
        pen.setWidth(2)     # 设置线宽
        painter.setPen(pen)  # 确定画笔
        painter.setOpacity(1)  # 透明度
        painter.drawPolyline(polygon1) # 画折线
        #画展示框
        if len(self.loads) > 0:
            rate = self.loads[0]
        else:
            rate = 1.0 
        rect1 = QRect(4, height * 0.05, self.boxWidth - 9, height * 0.8) # 柱状图位置
        rect2 = QRect(4, height * 0.8, self.boxWidth - 9, height * 0.2) # 数字
        pen.setColor(Qt.red)  
        painter.setPen(pen)
#        painter.drawText(rect2, Qt.AlignHCenter | Qt.AlignVCenter, str(rate[0]) + " MB/s" + "\n Read") # 数字显示
        pen.setColor(Qt.darkBlue)  
        painter.setPen(pen)
 #       painter.drawText(rect1, Qt.AlignHCenter | Qt.AlignVCenter, str(rate[1]) + " MB/s" + "\n Write") # 数字显示

class MachineLoad(object):
    def getLoad(self):
        iotmpdata = []
        iodata = []
        iorate = []
        try:
            test = Popen("iostat -d 1 1", stdout=PIPE, shell=True)
            tmplist = test.communicate()[0].split('\n')
            for i, io in enumerate(tmplist):
                if i >= 3 and io != "":
                    iotmpdata.append(io)
            for i, io in enumerate(iotmpdata):
                iodata.append(io.split())
            ioread = 0
            iowrite = 0
            for io in iodata:
                ioread += float(io[2])
                iowrite += float(io[3])
            iorate.append(ioread / 1024)
            iorate.append(iowrite / 1024)
            return iorate
        except:
            iorate = [0,0]
            return iorate


app = QApplication(sys.argv)
platform = IoLoadWidget()
platform.show()
sys.exit(app.exec_())

