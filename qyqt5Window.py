import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QMdiArea, QCalendarWidget, QTextEdit, QPushButton)
# 21.265,21.592,24.693,20.673,25.573,23.851,21.262,25.552,0.,0.
class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 800)

        workspace = QMdiArea(self)
        workspace.resize(self.rect().width(), self.rect().height())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())
