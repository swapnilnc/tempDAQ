# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 853)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 320))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_4.setContentsMargins(0, 0, -1, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame_down_mid = QtWidgets.QFrame(self.frame_2)
        self.frame_down_mid.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_down_mid.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_down_mid.setObjectName("frame_down_mid")
        self.gridLayout_4.addWidget(self.frame_down_mid, 0, 1, 2, 1)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setMaximumSize(QtCore.QSize(110, 16777215))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_8.setObjectName("gridLayout_8")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem, 1, 0, 1, 1)
        self.pushButton_start = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_start.setObjectName("pushButton_start")
        self.gridLayout_8.addWidget(self.pushButton_start, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_8.addItem(spacerItem1, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.frame_3, 0, 2, 2, 1)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.widget = QtWidgets.QWidget(self.frame_4)
        self.widget.setObjectName("widget")
        self.gridLayout_7.addWidget(self.widget, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 2, 1)
        self.gridLayout_2.addWidget(self.frame_2, 2, 0, 1, 1)
        self.frame_outer_top = QtWidgets.QFrame(self.centralwidget)
        self.frame_outer_top.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_outer_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_outer_top.setObjectName("frame_outer_top")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_outer_top)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(self.frame_outer_top)
        self.scrollArea.setMinimumSize(QtCore.QSize(721, 361))
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 361))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 780, 359))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_scrollarea = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_scrollarea.setObjectName("horizontalLayout_scrollarea")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_outer_top, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(0, 80))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(-1, 3, -1, 3)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_current = QtWidgets.QGroupBox(self.frame)
        self.groupBox_current.setStyleSheet("QGroupBox:title {\n"
"subcontrol-origin: margin;\n"
"subcontrol-position: top center;\n"
"padding-left: 10px;\n"
"padding-right: 10px;\n"
"}")
        self.groupBox_current.setObjectName("groupBox_current")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_current)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_current = QtWidgets.QLabel(self.groupBox_current)
        self.label_current.setAlignment(QtCore.Qt.AlignCenter)
        self.label_current.setObjectName("label_current")
        self.gridLayout_5.addWidget(self.label_current, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_current, 0, 0, 1, 1)
        self.groupBox_voltage = QtWidgets.QGroupBox(self.frame)
        self.groupBox_voltage.setStyleSheet("QGroupBox:title {\n"
"subcontrol-origin: margin;\n"
"subcontrol-position: top center;\n"
"padding-left: 10px;\n"
"padding-right: 10px;\n"
"}")
        self.groupBox_voltage.setObjectName("groupBox_voltage")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_voltage)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_voltage = QtWidgets.QLabel(self.groupBox_voltage)
        self.label_voltage.setAlignment(QtCore.Qt.AlignCenter)
        self.label_voltage.setObjectName("label_voltage")
        self.gridLayout_6.addWidget(self.label_voltage, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_voltage, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_start.setText(_translate("MainWindow", "Start"))
        self.groupBox_current.setTitle(_translate("MainWindow", "Current"))
        self.label_current.setText(_translate("MainWindow", "0.00"))
        self.groupBox_voltage.setTitle(_translate("MainWindow", "Voltage"))
        self.label_voltage.setText(_translate("MainWindow", "0.00"))
