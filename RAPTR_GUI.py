# (the example applies equally well to PySide)
import GUI_Utils
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from GUI_Utils import *
import sys

    
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = GUI_Utils.MainWindow()
    window.show()
    sys.exit(app.exec_())
