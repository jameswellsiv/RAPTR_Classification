import threading
import sys, time, operator
import glob
from test_script import test_script
from PyQt5 import QtCore, QtGui, QtWidgets
import psutil
import os
import cv2
import time

class subwindow(QtWidgets.QWidget):
    def createWindow(self,WindowWidth,WindowHeight, parent=None):
       super(subwindow,self).__init__(parent)
       self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
       self.resize(WindowWidth,WindowHeight)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.main_layout = QtGui.QVBoxLayout()

        ok_button = QtGui.QPushButton("Run")
        ok_button.clicked.connect(self.OK)      
        self.main_layout.addWidget(ok_button)       

        cancel_button = QtGui.QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel)      
        self.main_layout.addWidget(cancel_button)

        central_widget = QtGui.QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def myEvenListener(self,stop_event):
        state=True
        old_size = -1
        classification = 'none'
        while state and not stop_event.isSet():
            new_size = get_dir_size()
            print(new_size)
            if(old_size == -1):
                old_size = new_size
            elif(new_size != old_size):
                print('triggered!')
                old_size = new_size
                list_of_files = glob.glob('C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Trigger_Folder\\*.jpg') # * means all if need specific format then *.jpg
                lastest_image = get_youngest_file(list_of_files) 
                head, tail = os.path.split(lastest_image)
                print(tail)
                print('youngest: C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Trigger_Folder\\' + tail)
                classification, img_filename = test_script('C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Trigger_Folder\\' + tail)
                self.createsASubwindow(img_filename) 

    def createsASubwindow(self, img_filename):
        self.mySubwindow=subwindow()
        self.mySubwindow.createWindow(500,400, parent=self)
        #make pyqt items here for your subwindow
        #for example self.mySubwindow.button=QtGui.QPushButton(self.mySubwindow)
        print(img_filename)
        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(img_filename)
        label.setPixmap(pixmap)
        label.show()
        time.sleep(60)

    def OK(self):
        self.stop_event=threading.Event()
        self.c_thread=threading.Thread(target=self.myEvenListener, args=(self.stop_event,))
        self.c_thread.start()       

    def cancel(self):
        print('cancelled!')
        self.stop_event.set()
        self.close() 

    def open_popup(self):
        print("Opening a new popup window...")
        w1 = QtWidgets.QLabel("Window 1")
        w1.show()
        c2.waitKey(0)
        #self.w.append(MyPopup())
        #self.w.setGeometry(QRect(100, 100, 400, 200))
        #self.w.show()   

def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.resize(480, 320)
    window.show()
    app.exec_()


def kill_proc_tree(pid, including_parent=True):    
    parent = psutil.Process(pid)
    if including_parent:
        parent.kill()

def get_dir_size(start_path = 'C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Trigger_Folder'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size = total_size + 1
    return total_size

def get_oldest_file(files, _invert=False):
    """ Find and return the oldest file of input file names.
    Only one wins tie. Values based on time distance from present.
    Use of `_invert` inverts logic to make this a youngest routine,
    to be used more clearly via `get_youngest_file`.
    """
    gt = operator.lt if _invert else operator.gt
    # Check for empty list.
    if not files:
        return None
    # Raw epoch distance.
    now = time.time()
    # Select first as arbitrary sentinel file, storing name and age.
    oldest = files[0], now - os.path.getctime(files[0])
    # Iterate over all remaining files.
    for f in files[1:]:
        age = now - os.path.getctime(f)
        print(f + ' and age: ' + str(age))
        if gt(age, oldest[1]):
            # Set new oldest.
            oldest = f, age
    # Return just the name of oldest file.
    return oldest[0]

def get_youngest_file(files):
    return get_oldest_file(files, _invert=True)

