import threading
import sys, time, operator
import glob
from test_script import test_script
from PyQt5 import QtCore, QtGui, QtWidgets
import psutil
import os
import cv2
import time

#------------------------------------------------------- Thread Used for Updating GUI and Watchdog for Trigger Folder --------------------------------------- 
class WatchdogWorker(QtCore.QThread):
    
    output = QtCore.pyqtSignal(str, str)     #Signal for calling AddImage function
    finished = QtCore.pyqtSignal()      #Signal for updating GUI    
    terminated = QtCore.pyqtSignal()    #Another signal for updating GUI if user terminates
    cancel = QtCore.pyqtSignal()        #Another signal for updating GUI if user terminates

    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False           #Needed for loop in watchdog
        self.old_size = -1             #Needed for loop in watchdog
        self.new_size = 0              #Needed for loop in watchdog
        self.state = True              #Needed for loop in watchdog
        self.classification = 'none'
        self.img_filename = 'none'

    def __del__(self):
        self.exiting = True
        self.wait()

    def render(self, old_size, new_size):
        self.old_size = old_size
        self.new_size = new_size
        self.state = True
        self.exiting = False
        self.start()

    def run(self):
        while not self.exiting and self.state:
            self.new_size = get_dir_size()
            #print(self.new_size)
            if(self.old_size == -1):
                self.old_size = self.new_size
            elif(self.new_size > self.old_size):
                #print('triggered!')
                self.old_size = self.new_size
                list_of_files = glob.glob('C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Trigger_Folder\\*.jpg') # * means all if need specific format then *.jpg
                lastest_image = get_youngest_file(list_of_files) 
                head, tail = os.path.split(lastest_image)
                #print(tail)
                #print('youngest: C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Trigger_Folder\\' + tail)
                classification, img_filename = test_script('C:\\Users\\james\\Anaconda3\\envs\\classifier_env\\Classifier_Project\\RAPTR_Classification\\Trigger_Folder\\' + tail)
                #print("classified: " + img_filename)
                #time.sleep(3)
                self.output.emit(
                      img_filename, classification)

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.thread = WatchdogWorker()

        self.ok_button = QtGui.QPushButton("Run")
        self.ok_button.clicked.connect(self.makePicture)      
     

        self.cancel_button = QtGui.QPushButton("Pause")
        self.cancel_button.clicked.connect(self.cancel)      

        
        self.viewer = QtWidgets.QLabel()
        self.viewer.setFixedSize(300, 300)

        self.classificationBox = QtWidgets.QLabel()
        self.classificationLabel = QtWidgets.QLabel("Classification: ")

        self.thread.output.connect(self.addImage)
        self.thread.finished.connect(self.updateUi)
        self.thread.terminated.connect(self.updateUi)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.ok_button, 0, 0)
        layout.addWidget(self.cancel_button, 0, 1)
        layout.addWidget(self.viewer, 1, 0, 1, 3)
        layout.addWidget(self.classificationBox, 2, 1, 1, 3)
        layout.addWidget(self.classificationLabel, 2, 0, 1, 3)
        self.setLayout(layout)
        
        self.setWindowTitle(self.tr("RAPTR"))
        
    def makePicture(self):
        self.ok_button.setEnabled(False)
        pixmap = QtGui.QPixmap(self.viewer.size())
        pixmap.fill(QtCore.Qt.black)
        self.viewer.setPixmap(pixmap)
        self.thread.render(-1, 0)

    def addImage(self, img_filename, classification):
        pixmap = self.viewer.pixmap()
        pixmap = QtGui.QPixmap(img_filename)
        self.viewer.setPixmap(pixmap)
        self.classificationBox.setText(classification)

    def updateUi(self):
        print('updated!')
        
    
    def cancel(self):
        self.ok_button.setEnabled(True)
        self.thread.__del__()

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

#def watchdog_call():
