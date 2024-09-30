import sys
from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from qtawesome import icon as qt_icon

from OptimizeQt import *

class SideBar(AbstractWidget):
    def __init__(
            self,
            leader_func: Callable = lambda: ...,
            scatter_func: Callable = lambda: ...,
            line_func: Callable = lambda: ...,
            bar_func: Callable = lambda: ...,
            pie_func: Callable = lambda: ...,
            **kwargs
    ):
        super().__init__(**kwargs)

        self.setStyleSheet(
            """
            QPushButton {
                font-size: 20px;
            }
            """
        )

        self.__setUI(leader_func, scatter_func, line_func, bar_func, pie_func)
    def __setUI(
            self,
            leader_func : Callable = lambda : ...,
            scatter_func: Callable = lambda: ...,
            line_func: Callable = lambda: ...,
            bar_func: Callable = lambda: ...,
            pie_func: Callable = lambda: ...
    ) -> None:
        self.setLayout(
            Column.widgetsBuild(
                widgets=[
                    OptPushButton(
                        text='主页导航',
                        textModel=True,
                        iconModel=True,
                        icon=qt_icon('fa.home'),
                        cFunction=leader_func,
                        iconFixed=False,
                        objectName='主页导航'
                    ),
                    OptPushButton(
                        text='散点图',
                        iconModel=True,
                        textModel=True,
                        icon=qt_icon('fa.line-chart'),
                        cFunction=scatter_func,
                        iconFixed=False,
                        objectName='散点图'
                    ),
                    OptPushButton(
                        text='线性图',
                        iconModel=True,
                        textModel=True,
                        icon=qt_icon('fa.bar-chart'),
                        cFunction=line_func,
                        iconFixed=False,
                        objectName='线性图',
                    ),
                    OptPushButton(
                        text='柱状图',
                        iconModel=True,
                        textModel=True,
                        icon=qt_icon('fa.pie-chart'),
                        cFunction=bar_func,
                        iconFixed=False,
                        objectName='柱状图',
                    ),
                ],
                stretch=5
            ).resetContentsMargins(10, 0, 10, 0)
        )

        self.append(OptPushButton(
            text='饼状图',
            textModel=True,
            iconModel=True,
            icon=qt_icon('mdi.chart-scatter-plot'),
            cFunction=pie_func,
            iconFixed=False,
            objectName='饼状图',
        ))

    # 设置某个索引按钮被按下
    def pressStateByIndex(self, index) -> None:
        self.findChildren(QPushButton)[index].click()
    # 命名模式
    def pressStateByObejctName(self, obj : str) -> None:
        self.findChild(QPushButton, obj).click()

    @overload
    def append(self, text, func, icon) -> None:
        ...
    @overload
    def append(self, btn : Union[QPushButton, OptPushButton, QToolButton]):
        ...
    @overload
    def append(self, lay : QLayout, padding=QMargins(0, 0, 0, 0)):
        ...
    """
    * append(self, btn : Union[QPushButton, OptPushButton, QToolButton])
    * append(self, text, func, icon)
    * append(self, lay, padding)
    """
    def append(self, *args):
        if args.__len__() == 3:
            self.layout().addWidget(OptPushButton(
                text=args[0],
                textModel=True,
                iconModel=True,
                icon=args[2],
                cFunction=args[1],
                iconFixed=False
            ))
        elif args.__len__() == 2:
            slay : Column = self.layout()
            ilay : QLayout = args[0]
            slay.addLayout(ilay)
            ilay.setContentsMargins(args[1])
        else:
            self.layout().addWidget(args[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = SideBar(maxh=600, maxw=200)
    ui.show()
    sys.exit(app.exec_())