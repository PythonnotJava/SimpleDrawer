import sys
from typing import *
from abc import abstractmethod
from dataclasses import dataclass

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from qtawesome import icon as qt_icon

from OptimizeQt import *
from ChartWrapper import *

class OperatorBar(AbstractWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fileInput = OptLineEdit(
            placeholderText='模板路径',
            minw=400
        )
        self.openBtn = OptPushButton(
            text="打开",
            textModel=True,
            iconModel=True,
            icon=qt_icon('ei.folder-open'),
            iconFixed=False,
            maxw=150
        )

        self.__setUI()
    def __setUI(self) -> None:
        self.setLayout(
            Column.laysBuild(
                aligns=Qt.Alignment(),
                lays=[
                    Row.widgetsBuild(
                        widgets=[
                            self.fileInput,
                            self.openBtn
                        ]
                    )
                ]
            )
        )

@dataclass
class TabType:
    widget : QWidget
    title : str = 'Unkonw'
    icon : Optional[Union[QIcon, str]] = None

class TabView(QTabWidget, AbstractWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__setUI()
    def __setUI(self) -> None:
        self.setTabPosition(QTabWidget.North)

    def append(self, tab : TabType, which_return : Optional[int] = None) -> Any:
        widget = tab.widget
        label = tab.title
        icon = tab.icon
        if icon:
            icon = QIcon(icon)
            self.addTab(widget, icon, label)
        else:
            self.addTab(widget, label)
        match which_return:
            case 0:
                return widget
            case 1:
                return self
            case _:
                return

class CanvasMixin:
    @abstractmethod
    def append(self, **kwargs) -> Any: pass
    @abstractmethod
    def linkOpenFunction(self, func: Callable) -> None: pass
    @abstractmethod
    def setCurrentPath(self, path: str) -> None: pass

class TabCanvas(QSplitter, AbstractWidget, CanvasMixin):
    def __init__(
            self,
            defaultTabType : Optional[TabType] = None,
            **kwargs
    ):
        super().__init__(**kwargs)

        self.operatorBar = OperatorBar()
        self.tabview = TabView()

        self.counter = 0

        self.__setUI(defaultTabType)
    def __setUI(self, defaultTabType : Optional[TabType] = None) -> None:
        self.setOrientation(Qt.Vertical)
        self.addWidget(self.operatorBar)
        self.addWidget(self.tabview)
        if not defaultTabType:
            self.tabview.append(TabType(
                widget=OptLabel.textBuild(
                    minw=400,
                    minh=400,
                    qss='background-color:skyblue',
                    text="打开模板文件自动画图！"
                ),
                title="导航",
            ))
        else:
            self.tabview.append(defaultTabType)

    def append(self, tab : TabType, which_return : Optional[int] = None) -> Any:
        t = self.tabview.append(tab, which_return)
        self.counter += 1
        self.tabview.setCurrentIndex(self.counter)
        return t

    def linkOpenFunction(self, func : Callable) -> None:
        self.operatorBar.openBtn.clicked.connect(func)

    def setCurrentPath(self, path : str) -> None:
        self.operatorBar.fileInput.setText(path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = TabCanvas()
    ui.show()
    sys.exit(app.exec_())