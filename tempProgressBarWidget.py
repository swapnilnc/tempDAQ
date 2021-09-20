import sys
from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication
from PyQt5.QtCore import QBasicTimer


class ProgressBarDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.progressBar = [QProgressBar(self) for i in range(2)]
        self.progressBar[0].setGeometry(30, 70, 200, 25)
        self.progressBar[1].setGeometry(30, 40, 200, 25)
        self.progressBar[0].setValue(20)
        self.progressBar[1].setValue(45)

        # len()
        # self.progressbar[0] = QProgressBar(self)
        # self.progressbar[0].setGeometry(30, 40, 200, 25)
        # self.progressbar[0].setValue(20)
        # self.progressbar = QProgressBar(self)
        # self.progressbar.setGeometry(30, 40, 200, 25)
        # self.progressbar.setValue(20)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = ProgressBarDemo()
    demo.show()

    sys.exit(app.exec_())
