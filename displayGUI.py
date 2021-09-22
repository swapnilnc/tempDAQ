import sys
import time
from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication, QLabel, QMdiArea, QGroupBox, QAction, \
    QMainWindow
from PyQt5.QtCore import QBasicTimer, Qt, QRect
from PyQt5.QtGui import QIcon
from multiprocessing.sharedctypes import Value, Array
from threading import Thread, Lock


class AppDemo(QMainWindow):
    def __init__(self, valueList, chNames, numDevices):
        super().__init__()
        self.resize(1920, 1080)
        workspace = QMdiArea(self)
        workspace.resize(self.rect().width(), self.rect().height())
        self.tempWidget = ProgressBarWidget(chNames, numDevices)
        workspace.addSubWindow(self.tempWidget)
        self.tempWidget.adjustSize()
        self.displayVIWidget = displayVIWidget()
        workspace.addSubWindow(self.displayVIWidget)
        self.tempWidget.setWindowState(Qt.WindowActive)
        self.tempWidget.setGeometry(20, 20, (60 + numDevices[0] * 8 * 60), 500)
        self.menuBar = self.menuBar()
        fileMenu = self.menuBar.addMenu('File')
        startDisplay = QAction('Start', self)
        startDisplay.setShortcut('Ctrl+Q')
        startDisplay.triggered.connect(lambda: self.test(valueList))
        fileMenu.addAction(startDisplay)

    def test(self,valueList):
        while True:
            timer = Thread(target=timeIntervalFunction(3), args=())
            timer.start()
            print(valueList[:])
            timer.join()

    def setValue(self, valueList):
        while True:
            timer = Thread(target=timeIntervalFunction(3), args=())
            timer.start()
            self.displayVIWidget.setValue(valueList[-2:])
            self.tempWidget.setValue(valueList[:-2])
            timer = Thread(target=timeIntervalFunction(3), args=())
            timer.start()
            timer.join()


def timeIntervalFunction(timeSec):
    time.sleep(timeSec)


class ProgressBarWidget(QWidget):

    def __init__(self, chNames, numDevices):
        super().__init__()
        self.leads = numDevices[0] * 8
        # self.isMaximized()
        # self.resize((60 + self.leads * 60), 500)
        # self.resize(self.rect().width(), self.rect().height())
        self.setWindowTitle('Temperature Data')
        self.setWindowIcon(QIcon('daqicon.png'))
        self.setEnabled(True)
        self.setWindowState(Qt.WindowNoState)
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
            self.progressBar[i].setOrientation(Qt.Vertical)
            self.progressBar[i].setMaximum(150)

    def setValue(self, valueList):

        for i in range(len(valueList)):
            self.valLabels[i].setText(valueList[i])
            value = int(valueList[i])
            # if value <= 150:
            #     self.progressBar[i].setValue(value)
            # else:
            #     value = 0
            #     self.progressBar[i].setValue(value)


class displayVIWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Current and Voltage')
        self.setWindowIcon(QIcon('daqicon.png'))
        self.groupBoxCur = QGroupBox(self)
        self.groupBoxCur.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.groupBoxCur.setTitle("Current")
        self.groupBoxCur.setGeometry(QRect(10, 10, 200, 200))
        self.groupBoxVol = QGroupBox(self)
        self.groupBoxVol.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.groupBoxVol.setTitle('Voltage')
        self.groupBoxVol.setGeometry(QRect(220, 10, 200, 200))
        # print(value)
        self.labelCur = QLabel(self.groupBoxCur)
        self.labelCur.setGeometry(QRect(10, 10, 180, 180))
        # self.labelCur.setText(str(value[0]))
        self.labelCur.setAlignment(Qt.AlignCenter)
        self.labelVol = QLabel(self.groupBoxVol)
        self.labelVol.setGeometry(QRect(10, 10, 180, 180))
        # self.labelVol.setText(str(value[1]))
        self.labelVol.setAlignment(Qt.AlignCenter)

    def setValue(self, value):
        print(value)
        # self.labelCur.setText(str(value[0]))
        # self.labelVol.setText(str(value[1]))
        self.labelCur.setText(value[0])
        self.labelVol.setText(value[1])


def runGUI(qValueList, qchNames, qNumDevices):
    app = QApplication(sys.argv)
    window = AppDemo(qValueList, qchNames, qNumDevices)
    window.setWindowIcon(QIcon('daqicon2.png'))
    window.setWindowTitle('Data Acquisition')
    window.show()
    sys.exit(app.exec_())
