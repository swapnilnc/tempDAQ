import multiprocessing
import threading
from threading import Thread
from multiprocessing import Process
from multiprocessing.sharedctypes import Value, Array
from mcculw import ul
from mcculw.enums import TempScale
from mcculw.enums import InterfaceType
from ctypes import c_ubyte
import numpy as np
import serial
import pydmm.pydmm as pd
import sys
import csv
import time
import json
# from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication, QLabel, QMdiArea, QGroupBox, QAction, \
#     QMainWindow
# from PyQt5.QtCore import QBasicTimer, Qt, QRect
# from PyQt5.QtGui import QIcon
import displayGUI

global numDevices
global valuesStr
global valueList
global testNum
global chNames
global chLimits
global timeInterval
global runDuration
global qNumDevices
global qchNames
global qValueList
global sharedList


def initialize():
    #  To be defined
    with open('test.json', 'r') as infile:
        data = json.load(infile)
    global numDevices
    global testNum
    global chNames
    global chLimits
    global timeInterval
    global runDuration
    global qchNames

    numDevices = data['numDevices']
    testNum = data['TestNum']
    chNames = data["chNames"]
    qchNames = chNames
    chLimits = data["chLimits"]
    timeInterval = data["timeInterval"]
    runDuration = data['runDuration']
    initTempDAQ()
    initCSV()


def initTempDAQ():
    global numDevices
    global sharedList
    ul.ignore_instacal()
    devices = ul.get_daq_device_inventory(InterfaceType.ANY)
    # Connected device List
    numDevices[0] = len(devices)
    # qValueList = Array(c_ubyte, (["0.0"]*(numDevices[0]*8+2)), lock=lock)
    sharedList = []
    for i in range(numDevices[0]*8+2):
        sharedList.append("0.0")
    print(sharedList)
    global qNumDevices
    qNumDevices = numDevices
    i = 1
    for device in devices:
        ul.create_daq_device(i, device)
        i += 1


class COMInit:
    def __init__(self, vCOM, cCOM):
        # Voltage COM Port
        self.vCOM = vCOM
        # Current COM Port
        self.cCOM = cCOM


def timeIntervalFunction(timeSec):
    time.sleep(timeSec)


class MultiMeterDAQ:

    def __init__(self, port, timeout):
        self.port = port
        self.timeout = timeout

    def multimeter(self):
        try:
            port1 = self.port
            timeout1 = self.timeout
            number = pd.read_dmm(port=port1, timeout=timeout1)  # port='COM3'
            return number
        except:
            print('Error Multimeter')
            return 00.0


def tempCh():
    valuesAr = np.array([], dtype=float)
    numChannels = 8
    for boardNum in range(numDevices[0]):
        for channel in range(numChannels):
            try:
                values = ul.t_in(boardNum + 1, channel, TempScale.CELSIUS)
                valuesAr = np.append(valuesAr, values)
                # Display the value
                # print('Channel', i, 'Value (deg C):', values, '/n', self.values)
            except:
                valuesAr = np.append(valuesAr, 9999.0)
    return valuesAr


def writeGlobal(v=False, c=False):
    # This will run every 5 seconds
    # ****** TO IMPLEMENT CHECK IF VOLTAGE OR CURRENT IS AVAILABLE*****
    start = time.time()
    timeSec = 5
    timer = Thread(target=timeIntervalFunction(timeSec), args=())
    timer.start()
    if c:
        currentDAQ = MultiMeterDAQ(COMInit.cCOM, 3)
        current = currentDAQ.multimeter()
    else:
        current = 0.0

    if v:
        voltageDAQ = MultiMeterDAQ(COMInit.vCOM, 3)
        voltage = voltageDAQ.multimeter()
    else:
        voltage = 0.0
    temperatureAr = tempCh()
    arrUpload = np.append(temperatureAr, current)
    arrUpload = np.append(arrUpload, voltage)
    #  Converting the array to string - up to 3 dec place
    temp = np.array2string(arrUpload, precision=3, separator=',', suppress_small=True)
    # Removing unnecessary spaces and '\n's from result
    temp = temp[1:(len(temp) - 1)]
    temp = temp.replace(' ', '')
    temp = temp.replace('\n', '')
    timer.join()
    global valuesStr
    global valueList
    global sharedList
    mutex.acquire()
    valuesStr = temp
    stringList = valuesStr.split(',')
    valueList = [float(x) for x in stringList]
    for i in range(len(stringList)):
        sharedList[i] = stringList[i]
    mutex.release()
    end = time.time()
    print(valuesStr, end - start, valueList)
    writeGlobal(v, c)


def initCSV():
    with open('Trial.csv', 'w', newline='') as file:
        global chNames
        global qchNames
        writer = csv.writer(file)
        dateNow = time.strftime('%Y-%m-%d', time.localtime())  # '2021-05-14'
        timeNow = time.strftime('%H:%M:%S', time.localtime())  # '12:06:16'
        # *******To be implemented*******
        row_list = [["Python csv Generation Trial"],
                    [f"Worksheet name: {numDevices[0]} DAQ CPU 15min x {numDevices[1]} V x {numDevices[2]} C"],
                    [f"Recording date: {dateNow}, {timeNow}"],
                    ["Block length: 1"],
                    [f"Delta: {timeInterval / 60}min"],
                    [f"Number of channel:8x{numDevices[0]} Temp, Current, Voltage"],
                    [f"> {testNum}"],
                    [f"> {testNum}"]
                    ]
        writer.writerows(row_list)
        # *******To be implemented*******
        # strList = ['Date', 'Time']
        strList = []
        for numDevice in range(numDevices[0]):
            for channel in range(8):
                strList.append(f'DAQ{numDevice + 1}CH{channel}')
        if len(strList) == len(chNames):
            writer.writerow(["Date", "Time"] + chNames + ["Voltage", "Current"])
        else:
            writer.writerow(["Date", "Time"] + strList + ["Voltage", "Current"])
            chNames = strList
        qchNames = chNames
        file.close()


def appendCSV():
    start = time.time()
    timeSec = timeInterval
    timer = Thread(target=timeIntervalFunction(timeSec), args=())
    timer.start()
    global valuesStr
    listUp = valuesStr.split(",")
    print(valuesStr)
    dateNow = time.strftime('%Y-%m-%d', time.localtime())  # '2021-05-14'
    timeNow = time.strftime('%H:%M:%S', time.localtime())  # '12:06:16'
    with open('Trial.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([dateNow, timeNow] + listUp)
        # file.close()
    timer.join()
    end = time.time()
    print('appended', end - start)
    appendCSV()


def serialUpload(a='COM6'):
    global valuesStr
    ser = serial.Serial(
        port=a,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    ser.write((valuesStr + '~').encode())


def checkLimit():
    readValue = valuesStr[0:(len(valuesStr) - 3)]
    count = 0
    for i in range(len(readValue)):
        if readValue[i] > chLimits[i]:
            count += 1
    if count == 0:
        throttleCurrent(True)
    else:
        throttleCurrent(False)


def throttleCurrent(option):
    # to be defined
    a = 1


def getScreenSize():
    import ctypes
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize


# class AppDemo(QMainWindow, qValueList, qchNames, qNumDevices):
#     def __init__(self):
#         super().__init__()
#         global numDevices
#         global valueList
#         self.resize(1920, 1080)
#         workspace = QMdiArea(self)
#         workspace.resize(self.rect().width(), self.rect().height())
#
#         self.tempWidget = ProgressBarWidget()
#         workspace.addSubWindow(self.tempWidget)
#         self.tempWidget.adjustSize()
#         self.displayVIWidget = displayVIWidget()
#         workspace.addSubWindow(self.displayVIWidget)
#         self.tempWidget.setWindowState(Qt.WindowActive)
#         self.tempWidget.setGeometry(20, 20, (60 + numDevices[0] * 8 * 60), 500)
#         self.menuBar = self.menuBar()
#         fileMenu = self.menuBar.addMenu('File')
#         startDisplay = QAction('Start', self)
#         startDisplay.setShortcut('Ctrl+Q')
#         startDisplay.triggered.connect(lambda: self.setValue())
#         fileMenu.addAction(startDisplay)
#
#     def setValue(self):
#         while True:
#             global valueList
#             timer = Thread(target=timeIntervalFunction(3), args=())
#             timer.start()
#             self.displayVIWidget.setValue(valueList[-2:])
#             self.tempWidget.setValue(valueList[:-2])
#             print(self.tempWidget.sizeHint())
#             timer.join()
#         # self.setGeometry(500, 500, (60 + self.leads * 60), 500)
#         # self.tempWidget.showMaximized()
#         # self.tempWidget.setGeometry(500, 500, (60 + numDevices[0] * 8 * 60), 500)
#         # self.button = QPushButton('My Button')
#         # self.button.clicked.connect(lambda: print('button is clicked'))
#         # workspace.addSubWindow(self.button)
#
#         # textEditor = QTextEdit()
#         # workspace.addSubWindow(textEditor)
#
#
# class ProgressBarWidget(QWidget):
#     global numDevices
#     global valueList
#     global chNames
#
#     def __init__(self):
#         super().__init__()
#         self.leads = numDevices[0] * 8
#         # self.isMaximized()
#         # self.resize((60 + self.leads * 60), 500)
#         # self.resize(self.rect().width(), self.rect().height())
#         self.setWindowTitle('Temperature Data')
#         self.setWindowIcon(QIcon('daqicon.png'))
#         self.setEnabled(True)
#         self.setWindowState(Qt.WindowNoState)
#         self.progressBar = [QProgressBar(self) for i in range(self.leads)]
#         self.valLabels = [QLabel(self) for i in range(self.leads)]
#         self.leadNames = [QLabel(self) for i in range(self.leads)]
#         for i in range(numDevices[0] * 8):
#             self.leadNames[i].setGeometry((20 + i * 60), 5, 50, 25)
#             self.leadNames[i].setAlignment(Qt.AlignCenter)
#             self.leadNames[i].setText(chNames[i])
#         for i in range(numDevices[0] * 8):
#             self.progressBar[i].setGeometry((30 + i * 60), 30, 30, 200)
#             self.valLabels[i].setGeometry((25 + i * 60), 233, 40, 25)
#             self.valLabels[i].setAlignment(Qt.AlignCenter)
#             self.progressBar[i].setOrientation(Qt.Vertical)
#             self.progressBar[i].setMaximum(150)
#         # timeSec = 5
#         #     self.btnStart = QPushButton('Start', self)
#         #     self.btnStart.move(30, 280)
#         #     self.btnStart.clicked.connect(super)
#         # self.timer = QBasicTimer()
#         # self.step = 1
#
#     def setValue(self, valueFloatList):
#
#         for i in range(len(valueFloatList)):
#             value = valueFloatList[i]
#             self.valLabels[i].setText(str(value))
#             if value <= 150:
#                 self.progressBar[i].setValue(int(value))
#             else:
#                 value = 0
#                 self.progressBar[i].setValue(value)
#
#     # def timerEvent(self, event):
#     #     print('started')
#     #     global valuesStr
#     #     valuesList = valuesStr.split(',')
#     #     print(valuesList)
#     #     self.progressBar[0].setValue(valuesList[0])
#     #     # for i in range(numDevices[0] * 8):
#     #     #     # self.progressBar[i].setValue(valuesList[i])
#     #     #     self.progressBar[i].setValue(self.step)
#     #     if self.step <= 2147483639:
#     #         self.step += 1
#     #     else:
#     #         self.step = 1
#     #         self.step += 1
#
#
# class displayVIWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Current and Voltage')
#         self.setWindowIcon(QIcon('daqicon.png'))
#         self.groupBoxCur = QGroupBox(self)
#         self.groupBoxCur.setContextMenuPolicy(Qt.DefaultContextMenu)
#         self.groupBoxCur.setTitle("Current")
#         self.groupBoxCur.setGeometry(QRect(10, 10, 200, 200))
#         self.groupBoxVol = QGroupBox(self)
#         self.groupBoxVol.setContextMenuPolicy(Qt.DefaultContextMenu)
#         self.groupBoxVol.setTitle('Voltage')
#         self.groupBoxVol.setGeometry(QRect(220, 10, 200, 200))
#         # print(value)
#         self.labelCur = QLabel(self.groupBoxCur)
#         self.labelCur.setGeometry(QRect(10, 10, 180, 180))
#         # self.labelCur.setText(str(value[0]))
#         self.labelCur.setAlignment(Qt.AlignCenter)
#         self.labelVol = QLabel(self.groupBoxVol)
#         self.labelVol.setGeometry(QRect(10, 10, 180, 180))
#         # self.labelVol.setText(str(value[1]))
#         self.labelVol.setAlignment(Qt.AlignCenter)
#
#     def setValue(self, value):
#         print(value)
#         self.labelCur.setText(str(value[0]))
#         self.labelVol.setText(str(value[1]))
#
#
# def runGUI(qValueList, qchNames, qNumDevices):
#     app = QApplication(sys.argv)
#     window = AppDemo(qValueList, qchNames, qNumDevices)
#     window.setWindowIcon(QIcon('daqicon2.png'))
#     window.setWindowTitle('Data Acquisition')
#     window.show()
#     sys.exit(app.exec_())

# def process1():
#     t1 = Thread(target=writeGlobal, args=(v, c), daemon=True)
#     t1.start()
#     t2 = Thread(target=appendCSV, args=(), daemon=True)
#     t2.start()
#
#
# def process2():
#     t3 = Thread(target=runGUI, args=(), daemon=True)
#     t3.start()




if __name__ == '__main__':
    lock = multiprocessing.Lock()
    mutex = threading.Lock()
    manager = multiprocessing.Manager()
    sharedList = manager.list()
    initialize()
    v = False
    c = False
    t1 = Thread(target=writeGlobal, args=(v, c), daemon=True)
    t1.start()
    t2 = Thread(target=appendCSV, args=(), daemon=True)
    t2.start()
    time.sleep(10)
    t3 = Process(target=displayGUI.runGUI, args=(sharedList, qchNames, qNumDevices), daemon=True)
    t3.start()
    # t3 = Thread(target=checkLimit, args=(), daemon=True)
    # t3.start()
    print(numDevices[0])
    print('main sleeping')
    time.sleep(runDuration)
    print('main awake')
