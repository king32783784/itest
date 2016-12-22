import os
import sys

from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSlot


class SignalsWindow(QtGui.QWidget, object):
    def __init__(self, parent=None):
        super(SignalsWindow, self).__init__(parent)
        self.resize(600, 800)

        # plain text edit
        self.output_text = QtGui.QPlainTextEdit()
        self.output_text.setReadOnly(True)  # read-only
        self.output_text.setStyleSheet('QPlainTextEdit { background-color: #0a0c00; color: white; }')

        # instructions label
        self.instructions_label = QtGui.QLabel()
        self.instructions_label.setTextFormat(Qt.PlainText)
        self.instructions_label.setWordWrap(True)
        self.instructions_label.setEnabled(False)

        # icons
        clean_icon = QtGui.QIcon(os.path.join('images', 'clean_icon.png'))

        # clean button
        clean_button = QtGui.QToolButton()
        clean_button.setIcon(clean_icon)
     #   clean_button.setToolTip('Clean all')
     #   clean_button.clicked.connect(self.clean_button_clicked)  # clicked signal

        # horizontal box layout
        hlayout = QtGui.QHBoxLayout()
        hlayout.addStretch()
      #  hlayout.addWidget(clean_button)

        # vertical box layout
        self.vlayout = QtGui.QVBoxLayout()
        self.vlayout.setDirection(QtGui.QBoxLayout.BottomToTop)
        self.vlayout.addLayout(hlayout)
        self.vlayout.addWidget(self.output_text)
        self.setLayout(self.vlayout)

    def scroll_to_end(self):
        self.output_text.moveCursor(QtGui.QTextCursor.End)

    # *** SLOTS ***
    # clicked slot
    @pyqtSlot()
    def clean_button_clicked(self):
        self.output_text.clear()


#if __name__ == '__main__':
#    application = QtGui.QApplication(sys.argv)

    # window
#    window = SignalsWindow()
#    window.setWindowTitle('Signals window')
#    window.resize(320, 800)
#    window.show()

 #   sys.exit(application.exec_())
