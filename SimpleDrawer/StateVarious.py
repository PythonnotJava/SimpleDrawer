import json
import sys
import random
from typing import *

import psutil
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtChart import *
from qt_material import apply_stylesheet, list_themes

from SideBar import SideBar
from OptimizeQt import *
from CanvasUI import *
from WalkerWebview import PygwalkerOpt
from MenuBar import MenuBar
from DefaultCanvas import *

class StateVarious(QStatusBar):
    def __init__(self):
        super().__init__()

        self.timer = QTimer(self)
        self.online_time = QTime(0, 0)
        self.timelabel = QLabel("在线时间: 00:00:00", self)
        self.cpulabel = QLabel("CPU 占用: 0%", self)
        self.memorylabel = QLabel("内存占用: 0", self)
        self.process = psutil.Process()
        self.__setUI()

    def __setUI(self) -> None:
        self.timer.start(1000)
        self.timer.timeout.connect(self.__update_time)

        self.addWidget(self.timelabel)
        self.addWidget(self.cpulabel)
        self.addWidget(self.memorylabel)

    def __update_time(self):
        self.online_time = self.online_time.addSecs(1)
        self.timelabel.setText(f"在线时间: {self.online_time.toString()}")
        # 获取当前进程的 CPU 和内存占用
        cpu_usage = self.process.cpu_percent(interval=0)
        memory_info = self.process.memory_info()
        memory_usage = memory_info.rss / (1024 * 1024)
        self.cpulabel.setText(f"CPU 占用: {cpu_usage}%")
        self.memorylabel.setText(f"内存占用: {memory_usage:.2f} MB")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = StateVarious()
    ui.show()
    sys.exit(app.exec())