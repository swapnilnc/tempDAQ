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
import multiprocessing
import threading
import sys
import csv
import time
import json
import os
import tempfile
# from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication, QLabel, QMdiArea, QGroupBox, QAction, \
#     QMainWindow
# from PyQt5.QtCore import QBasicTimer, Qt, QRect
# from PyQt5.QtGui import QIcon
import runGUI

global numDevices


def initialize():
    initTempDAQ()


def initTempDAQ():
    global numDevices
    ul.ignore_instacal()
    devices = ul.get_daq_device_inventory(InterfaceType.ANY)
    # If number of devices is different replace new number
    with open('test.json', 'r') as infile:
        data = json.load(infile)
        print(data)
        numDevices = data['numDevices']
        chLimits = data['chLimits']
        infile.seek(0)
        infile.close()
    # Connected device List
    if numDevices[0] != len(devices):
        extra = len(devices) - numDevices[0]
        print('dasdasda', extra)
        extraLimits = 150
        for i in range(extra*8):
            chLimits.append(extraLimits)
        numDevices[0] = len(devices)
        data['numDevices'] = numDevices
        data['chLimits'] = chLimits
        print(data)
        with open('test.json', 'w') as outfile:
            json.dump(data, outfile)
            outfile.close()
    i = 1
    for device in devices:
        ul.create_daq_device(i, device)
        i += 1
    initCSV()


def initCSV():
    with open('test.json', 'r') as inFile:
        data = json.load(inFile)
        numDevices = data['numDevices']
        testNum = data['TestNum']
        chNames = data["chNames"]
        timeInterval = data["timeInterval"]
        inFile.close()

    with open('Trial.csv', 'w', newline='') as file:
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
            data["chNames"] = chNames
            with open('test.json', 'w') as outfile:
                json.dump(data, outfile)
                outfile.close()
        file.close()


def initTempData():
    currentDir = os.getcwd()
    inPath = '{}/tempFiles'.format(currentDir)
    outDic = tempfile.TemporaryFile(mode='w+b', dir=inPath, delete=False)
    # opList = b'21.265, 21.592, 24.693, 20.673, 25.573, 23.851, 21.262, 25.552, 0., 0.'
    # outDic.write(opList)
    # outDic.seek(0)
    print(outDic.name)
    return str(outDic.name)


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


def writeGlobal(v=False, c=False, dirTemp=[]):
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

    # global valuesStr
    # global valueList
    # global sharedList

    mutex.acquire()
    with open(dirTemp[0], 'w+b') as writeTemp:
        arr = bytes(temp, 'utf-8')
        writeTemp.write(arr)
        writeTemp.close()
    valuesStr = temp
    stringList = valuesStr.split(',')
    valueList = [float(x) for x in stringList]
    # for i in range(len(stringList)):
    #     sharedList[i] = stringList[i]
    mutex.release()
    end = time.time()
    print(valuesStr, end - start, valueList)
    writeGlobal(v, c, dirTemp)


def timeIntervalFunction(timeSec):
    time.sleep(timeSec)


def appendCSV(dirTemp):
    start = time.time()
    with open('test.json', 'r') as infile:
        data = json.load(infile)
        timeSec = data["timeInterval"]
        infile.close()
    timer = Thread(target=timeIntervalFunction(timeSec), args=())
    timer.start()
    mutex.acquire()
    print(dirTemp)
    with open(dirTemp, 'r') as readTemp:
        valuesStr = readTemp.read()
        readTemp.close()
    mutex.release()
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
    appendCSV(dirTemp)


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    mutex = threading.Lock()
    manager = multiprocessing.Manager()
    sharedList = manager.list()
    with open('test.json', 'r') as infile:
        data = json.load(infile)
        runDuration = data["runDuration"]
        infile.close()
    initialize()
    dir = initTempData()
    v = False
    c = False
    t1 = Thread(target=writeGlobal, args=(v, c, [dir]), daemon=True)
    t1.start()
    t2 = Thread(target=appendCSV, args=[dir], daemon=True)
    t2.start()
    time.sleep(10)
    t3 = Process(target=runGUI.runGUI, args=([dir]), daemon=True)
    t3.start()
    print(numDevices[0])
    print('main sleeping')
    time.sleep(runDuration)
    print('main awake')
