import json
import sys
import random
from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtChart import *
from qt_material import apply_stylesheet, list_themes

from OptimizeQt import *


class ExitDlg(QDialog, AbstractWidget):

    whatToDo = pyqtSignal(int)

    def __init__(self, s=None):
        super().__init__()

        self.checkbox = QCheckBox()
        self.checkbox.clicked.connect(lambda: self.__my_lambda(s, not self.checkbox.checkState() == Qt.CheckState.Checked))
        self.__setUI()

    @staticmethod
    def __my_lambda(s, v): s['exit-ask'] = v

    def __setUI(self) -> None:
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(300, 100)
        self.selfLayoutConstructor(
            hbox=False,
            widgets_lays=[
                WidgetOrLayoutType(
                    obj=QLabel("您 确 定 要 关 闭 此 软 件 吗  ？"),
                    dtype=1
                ),
                WidgetOrLayoutType(
                    obj=Row.widgetsBuild(
                        widgets=[
                            self.checkbox,
                            QLabel('以后都不用提醒我！')
                        ],
                    ).resetContentsMargins(80, 0, 0, 0),
                    dtype=0
                ),
                WidgetOrLayoutType(
                    obj=Row.widgetsBuild(
                        widgets=[
                            OptPushButton.textBuild(
                                text="最小化到托盘",
                                cFunction=lambda: self.whatToDo.emit(0),
                                maxw=150
                            ),
                            OptPushButton.textBuild(
                                text="退出",
                                cFunction=lambda: self.whatToDo.emit(1),
                                maxw=80
                            ),
                            OptPushButton.textBuild(
                                text="取消",
                                cFunction=lambda: self.whatToDo.emit(2),
                                maxw=80
                            ),
                        ]
                    ),
                    dtype=0
                )
            ]
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = ExitDlg()
    ui.show()
    sys.exit(app.exec())