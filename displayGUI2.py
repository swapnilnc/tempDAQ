import sys
import time
from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication, QLabel, QMdiArea, QGroupBox, QAction, \
    QMainWindow, QGridLayout, QVBoxLayout
from PyQt5.QtCore import QBasicTimer, Qt, QRect, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QIcon
from multiprocessing.sharedctypes import Value, Array
from threading import Thread, Lock
import tempfile
# from threading import Thread
from multiprocessing import Process
import os
import time
import json


class ResultObj(QObject):
    def __init__(self, val):
        self.val = val


# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal(object)
    progress = pyqtSignal()

    def __init__(self, dir, callback):
        super().__init__()
        self.dir = dir
        self.finished.connect(callback)

    def run(self):
        """Long-running task."""
        print('reached here')
        print('in read', self.dir)
        with open(self.dir, 'r') as readTemp:
            valueList = readTemp.read()
            readTemp.close()
        valueList = valueList.replace(' ', '')
        valueList = valueList.split(',')
        print('blah', valueList, type(valueList[0]))
        self.finished.emit(ResultObj(valueList))


class AppDemo(QWidget):
    def __init__(self, dir):
        super().__init__()
        self.dir = dir
        self.resize(1920, 1080)
        workspace = QVBoxLayout()
        # workspace.resize(self.rect().width(), self.rect().height())
        # Creating object for Temp Display
        self.tempWidget = ProgressBarWidget()
        workspace.addWidget(self.tempWidget)
        # Creating object for Voltage Current Display
        self.displayVIWidget = displayVIWidget()
        workspace.addWidget(self.displayVIWidget)
        # Button to start process
        buttonStart = QPushButton("Start")
        workspace.addWidget(buttonStart)
        buttonStart.clicked.connect(self.iterateProcess)
        # Step 2: Creating a thread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker(self.dir, self.reportProgress)
        self.setLayout(workspace)
        print(self.children())

    def iterateProcess(self):
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        print("entered here")
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run())
        # self.worker.finished.connect(self.thread.quit)
        # self.worker.finished.connect(callback, self.worker.quit)
        # self.worker.progress.connect(self.reportProgress)
        buttonStart.clicked.connect(self.thread.start())
        self.thread.finished.connect(self.thread.deleteLater)
        # fileMenu.addAction(startDisplay)

    # The QThread connects here and reportProgress updates the display
    def reportProgress(self, result):
        val = result.val
        print('reported!!', val)
        print(val[-2:])
        print(val[:-2])
        self.displayVIWidget.setValue(val[-2:])
        self.tempWidget.setValue(val[:-2])
        print('reported values!')


class ProgressBarWidget(QWidget):

    def __init__(self):
        super().__init__()
        with open('test.json', 'r') as inFile:
            data = json.load(inFile)
            numDevices = data['numDevices']
            chNames = data["chNames"]
            inFile.close()
        print('in progressbar widget read data')
        self.leads = numDevices[0] * 8
        self.resize(1920, 500)
        # self.resize((60 + self.leads * 60), 500)
        self.resize(self.rect().width(), self.rect().height())
        # self.setWindowTitle('Temperature Data')
        # self.setWindowIcon(QIcon('daqicon.png'))
        self.progressBar = [QProgressBar(self) for i in range(self.leads)]
        self.valLabels = [QLabel(self) for i in range(self.leads)]
        self.leadNames = [QLabel(self) for i in range(self.leads)]
        for i in range(numDevices[0] * 8):
            self.leadNames[i].setGeometry((20 + i * 60), 5, 50, 25)
            self.leadNames[i].setAlignment(Qt.AlignCenter)
            self.leadNames[i].setText(chNames[i])
        for i in range(numDevices[0] * 8):
            self.progressBar[i].setGeometry((30 + i * 60), 30, 30, 200)
            self.valLabels[i].setGeometry((25 + i * 60), 233, 40, 25)
            self.valLabels[i].setAlignment(Qt.AlignCenter)
            self.valLabels[i].setText('0.0')
            self.progressBar[i].setOrientation(Qt.Vertical)
            self.progressBar[i].setMaximum(150)
            self.progressBar[i].setValue(25)

        print('progressbar widget complete')

    def setValue(self, valueList):
        print('qwerty!!!!!', valueList)
        for i in range(numDevices[0]):
            print(i)
            self.valLabels[0 * (i * 8)].setText(valueList[0 * (i * 8)])
            self.valLabels[1 * (i * 8)].setText(valueList[0 * (i * 8)])
            self.valLabels[2 * (i * 8)].setText(valueList[0 * (i * 8)])
            self.valLabels[3 * (i * 8)].setText(valueList[0 * (i * 8)])
            self.valLabels[4 * (i * 8)].setText(valueList[0 * (i * 8)])
            self.valLabels[5 * (i * 8)].setText(valueList[0 * (i * 8)])
            self.valLabels[6 * (i * 8)].setText(valueList[0 * (i * 8)])
            self.valLabels[7 * (i * 8)].setText(valueList[0 * (i * 8)])
            # value = int(valueList[i])
            # self.progressBar[i].setValue(value)
            # if value <= 150:
            #     self.progressBar[i].setValue(value)
            # else:
            #     value = 0
            #     self.progressBar[i].setValue(value)


class displayVIWidget(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle('Current and Voltage')
        # self.setWindowIcon(QIcon('daqicon.png'))
        self.resize(1920, 500)
        self.resize(self.rect().width(), self.rect().height())
        # GroupBox for current data
        self.groupBoxCur = QGroupBox(self)
        self.groupBoxCur.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.groupBoxCur.setTitle("Current")
        self.groupBoxCur.setGeometry(QRect(10, 10, 200, 200))
        self.labelCur = QLabel(self.groupBoxCur)
        self.labelCur.setGeometry(QRect(10, 10, 180, 180))
        self.labelCur.setAlignment(Qt.AlignCenter)
        # GroupBox for voltage data
        self.groupBoxVol = QGroupBox(self)
        self.groupBoxVol.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.groupBoxVol.setTitle('Voltage')
        self.groupBoxVol.setGeometry(QRect(220, 10, 200, 200))
        self.labelVol = QLabel(self.groupBoxVol)
        self.labelVol.setGeometry(QRect(10, 10, 180, 180))
        self.labelVol.setAlignment(Qt.AlignCenter)
        # Set init values
        self.labelCur.setText('9.9')
        self.labelVol.setText('9.9')

    def setValue(self, val):
        print('set value in VI', val[0], val[1])
        self.labelCur.setText(str(value[0]))
        self.labelVol.setText(str(value[1]))
        # Not even this works
        # self.labelCur.setText('1.0')
        # self.labelVol.setText('2.0')


def runGUI(dir):
    app = QApplication(sys.argv)
    window = AppDemo(dir)
    window.setWindowIcon(QIcon('daqicon2.png'))
    window.setWindowTitle('Data Acquisition')
    window.show()
    sys.exit(app.exec_())
