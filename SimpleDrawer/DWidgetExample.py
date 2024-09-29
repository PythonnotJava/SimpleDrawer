import sys
from PyQt5.QtWidgets import *
from qtawesome import icon as qt_icon

class DWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.name = "笔记本"
        self.icon = qt_icon('mdi.microsoft-dynamics-365')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = DWidget()
    ui.show()
    sys.exit(app.exec_())