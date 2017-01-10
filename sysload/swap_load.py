# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

try:
    str = unicode
except NameError:
    pass

import os, io,sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from collections import OrderedDict

__all__ = ["SwapLoadWidget"]

class SwapLoadWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self.collectMachineLoad)
        self.loads = []
        self.maxLength = 400
        self.pointDistance = 5 #每点之间的间隔
        self.updateInterval = 1000 #更新的时间间隔
        self.timer.setInterval(self.updateInterval)
        self.timer.start()
        self.machineLoad = MachineLoad.getInstance()
        self.boxWidth = 60

    def finalize(self):
        self.timer.stop()
        self.loads = []

    def collectMachineLoad(self):
        rate = self.machineLoad.getLoad()
        self.loads.insert(0, rate)
        if len(self.loads) > self.maxLength:
            self.loads.pop( - 1)
        if self.isVisible():
            self.update()

    def paintEvent(self, event):
        QWidget.paintEvent(self, event)
        width, height = self.width(), self.height()
        polygon = QPolygon()
        for i, rate in enumerate(self.loads):
            x = width - i * self.pointDistance
            y = height - rate * height
            if x < self.boxWidth:
                break
            polygon.append(QPoint(x, y))
        painter = QPainter(self)
        pen = QPen()
        pen.setColor(Qt.white)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing, True)
        #画网格
        painter.setOpacity(0.7)
        gridSize = self.pointDistance * 4
        deltaX = (width - self.boxWidth) % gridSize + self.boxWidth
        deltaY = height % gridSize
        for i in range(int(width / gridSize)):
            x = deltaX + gridSize * i
            painter.drawLine(x, 0, x, height)
        for j in range(int(height / gridSize)):
            y = j * gridSize + deltaY
            painter.drawLine(self.boxWidth, y, width, y)
        #画折线
        pen.setColor(Qt.darkCyan)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setOpacity(1)
        painter.drawPolyline(polygon)
        #画展示框
        if len(self.loads) > 0:
            rate = self.loads[0]
        else:
            rate = 1.0
        rect1 = QRect(4, height * 0.05, self.boxWidth - 9, height * 0.7)
        rect2 = QRect(4, height * 0.8, self.boxWidth - 9, height * 0.2)
        centerX = int(rect1.width() / 2) + 1
        pen.setWidth(1)
        for i in range(rect1.height()):
            if i % 4 == 0:
                continue
            if (rect1.height() - i) / rect1.height() > rate:
                pen.setColor(Qt.white)
            else:
                pen.setColor(Qt.green)
            painter.setPen(pen)
            for j in range(rect1.width()):
                if centerX - 1 <= j <= centerX + 1:
                    continue
                painter.drawPoint(rect1.x() + j, rect1.y() + i)
        pen.setColor(Qt.black)
        painter.setPen(pen)
        painter.drawText(rect2, Qt.AlignHCenter | Qt.AlignVCenter, str(int(rate * 100)) + "%")

if os.path.exists("/proc/meminfo"):
    class MachineLoad:
        _instance = None

        @staticmethod
        def getInstance():
            if MachineLoad._instance is None:
                MachineLoad._instance = MachineLoad()
            return MachineLoad._instance

        def getLoad(self):
            try:
                ifstat = open('/proc/swaps').readlines()
                for i , interface in enumerate(ifstat):
                    stat = interface.split()
                    if i == 1:
                        swap = stat
                return float(swap[3]) / float(swap[2])
            except:
                return 0

else:
    class MachineLoad:
        _instance = None

        @staticmethod
        def getInstance():
            if MachineLoad._instance is None:
                MachineLoad._instance = MachineLoad()
            return MachineLoad._instance

        def getLoad(self):
            return 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    platform = SwapLoadWidget()
    platform.show()
    sys.exit(app.exec_())

