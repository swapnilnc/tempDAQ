import os
import sys
import time
from typing import Union

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout

import value_check as check
from UI import ui_home, custom_widgets

currentDir = os.path.dirname(__file__)
inPath = os.path.join(currentDir, './tempFiles/tmporhmpebg')


class HomeWindow(QMainWindow):
    def __init__(self,inPath):
        super(HomeWindow, self).__init__()
        self.progressbar_widget = None
        self.inPath = inPath
        self.is_timer_running = False
        self.start_time = None
        self.timer_count = 0
        self.check_timer: Union[None, 'QTimer'] = None

        self.progressbar_list = []
        self.ui = ui_home.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setBaseSize(1050, 853)
        self.resize(1050, 853)
        self.setWindowTitle('Data Acquisition')

        self.ui.label_current.setText('9.9')
        self.ui.label_voltage.setText('9.9')

        self.config_data = check.load_configuration_file('test.json')
        self.add_progressBars()

        # add graph widget
        self.graph_widget = custom_widgets.CustomGraphWidget("Time vs Data plot", "Time (s)", self.config_data['chNames'])
        self.grid_layout_graph_widget = QGridLayout()
        self.ui.widget.setLayout(self.grid_layout_graph_widget)
        self.grid_layout_graph_widget.addWidget(self.graph_widget)
        self.grid_layout_graph_widget.setContentsMargins(0, 0, 0, 0)

        self.ui.pushButton_start.clicked.connect(self.startCheck_timer)

    def create_timer(self, interval):
        if not self.check_timer:
            self.check_timer = QTimer()
            self.check_timer.setInterval(interval * 1000)
            self.check_timer.timeout.connect(self.update_progressBars)

    def startCheck_timer(self):
        if not self.check_timer:
            self.create_timer(self.config_data['timeInterval'])
        if not self.is_timer_running:
            self.start_time = time.time_ns()  # note starting time
            self.graph_widget.reset_graphs()  # this will clear existing graphs from canvas

            self.update_progressBars()

            self.check_timer.start()

            self.is_timer_running = True
            self.ui.pushButton_start.setText("Running...")
            self.ui.pushButton_start.setDisabled(True)

    def update_progressBars(self):
        """
        update existing progress-bars with new obtained values
        """
        self.timer_count = time.time_ns() - self.start_time
        if (self.timer_count / 10 ** 9) > self.config_data['runDuration']:
            self.check_timer.stop()
            self.is_timer_running = False
            self.start_time = None
            self.timer_count = 0
            self.ui.pushButton_start.setText("Start")
            self.ui.pushButton_start.setEnabled(True)
            self.check_timer = None
            return

        self.ui.statusbar.showMessage("updating...")
        new_values = check.reload_file_data(self.inPath)
        for progress_bar, value in zip(self.progressbar_list, new_values):
            progress_bar.update_progressbar(round(value, 3))
        self.ui.label_current.setText(str(new_values[-1]))
        self.ui.label_voltage.setText(str(new_values[-2]))
        time_s = self.timer_count // 10 ** 9
        self.graph_widget.plot(time_s, *new_values)

        self.ui.statusbar.showMessage("updated", 2000)

    def add_progressBars(self):
        """
        call only once to initialize all progress bars and set their labels and initial values
        :return:
        """
        self.progressbar_list = []
        for label, max_limit in zip(self.config_data['chNames'], self.config_data['chLimits']):
            value = 0.0
            self.progressbar_widget = custom_widgets.CustomProgressbarWidget(label, max_limit=max_limit)
            self.ui.horizontalLayout_scrollarea.addWidget(self.progressbar_widget)
            self.progressbar_widget.update_progressbar(value)
            self.progressbar_list.append(self.progressbar_widget)


def runGUI(dir):
    app = QApplication(sys.argv)
    w = HomeWindow(dir)
    w.show()
    sys.exit(app.exec())
