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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui

__all__ = ["NetLoadWidget"]

class NetLoadWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self.collectMachineLoad)
        self.num = 0
        self.loads = [[0,0]]
        self.rular = 128
        self.netrate = [0,0]
        self.maxLength = 400 # 表长
        self.pointDistance = 4 # 网格之间的间隔
        self.updateInterval = 1100 # 变化的时间间隔
        self.timer.setInterval(self.updateInterval)
        self.timer.start()
        self.boxWidth = 90 # 柱状图宽度

    def getrate(self, testrate):
        self.netrate = testrate

    def finalize(self):
        self.timer.stop()
        self.loads = []

    def setrular(self):
        if self.loads[0][0] >= self.loads[0][1]:
            tmprular = self.loads[0][0]
        else:
            tmprular = self.loads[0][1]
        if tmprular < 2:
            self.rular = 4
        else:
            self.rular = tmprular * 2
        

    def collectMachineLoad(self):
        self.netload = NetLoad()
        self.netload.trigger.connect(self.getrate)
        self.netload.start()
        self.num += 1
        rate = self.netrate
        self.loads.insert(0, rate)
        if len(self.loads) > self.maxLength:
            self.loads.pop( - 1)
        test = int((self.width() - self.boxWidth))
        if self.num % test == 0:
            self.setrular()
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
                y = 6
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
        pen.setColor(Qt.white) # 设置画笔颜色为白色
        painter.setPen(pen)   # 选择画笔
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
        """
        # 柱状图
        centerX = int(rect1.width() / 2) + 1 # 每个宽度
        pen.setWidth(1) # 线宽
        for i in range(rect1.height()): 
            if i % 4 == 0:
                continue
            if (rect1.height() - i) / rect1.height() > rate: # 根据rate改变画笔颜色
                pen.setColor(Qt.black)  # darkGreen
            else:
                pen.setColor(Qt.green)
            painter.setPen(pen) # 选定画笔
            for j in range(rect1.width()):
                if centerX - 1 <= j <= centerX + 1:
                    continue
                painter.drawPoint(rect1.x() + j, rect1.y() + i)
        """
        pen.setColor(Qt.red)  
        painter.setPen(pen)
        if rate[1] > 1024:
            txdata = rate[1] / 1024
            painter.drawText(rect2, Qt.AlignHCenter | Qt.AlignVCenter, str("%.2f" % txdata) + " MB/s" + "\n Sending") # 数字显示
        else:
            painter.drawText(rect2, Qt.AlignHCenter | Qt.AlignVCenter, str("%.2f" % rate[1]) + " KB/s" + "\n Sending")
        pen.setColor(Qt.darkBlue)  
        painter.setPen(pen)
        if rate[0] > 1024:
            rxdata = rate[0] / 1024
            painter.drawText(rect1, Qt.AlignHCenter | Qt.AlignVCenter, str("%.2f" % rxdata) + "MB/s" + "\n Receiving") # 数字显示
        else:
            painter.drawText(rect1, Qt.AlignHCenter | Qt.AlignVCenter, str("%.2f" % rate[0]) + "KB/s" + "\n Receiving") # 数字显示
            
class NetLoad(QtCore.QThread):
    trigger = QtCore.pyqtSignal(list)
    def __init__(self, parent=None):
        super(NetLoad, self).__init__(parent)

    def rx(self):
        totalrx = []
        try:
            ifstat = open('/proc/net/dev').readlines()
            for i,interface in enumerate(ifstat):
                stat = interface.split()
                if i >= 3:
                    totalrx.append(stat)
            rxdata = 0
            for rxtmp in totalrx:
                rxdata += float(rxtmp[1])
            return rxdata / 512
        except:
            return 0

    def tx(self):
        totaltx = []
        try:
            ifstat = open('/proc/net/dev').readlines()
            for i,interface in enumerate(ifstat):
                stat = interface.split()
                if i >= 3:
                    totaltx.append(stat)
            txdata = 0
            for txtmp in totaltx:
                txdata += float(txtmp[9])
            return txdata / 512
        except:
            return 0

    def run(self):
        beforerx = self.rx()
        beforetx = self.tx()
        time.sleep(0.5)
        afterrx = self.rx()
        aftertx = self.tx()
        netrate = []
        netrate.append(afterrx-beforerx)
        netrate.append(aftertx-beforetx)
        self.trigger.emit(netrate)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    platform = NetLoadWidget()
    platform.show()
    sys.exit(app.exec_())

