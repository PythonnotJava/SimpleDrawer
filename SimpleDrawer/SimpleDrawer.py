import sys
import random
from typing import *

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


WHATTHIS = "Find Simple tools in Drawer."

class SimpleDrawer(QMainWindow, AbstractWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.homePage = OptLabel.textBuild(text="自带插件系统，可以轻松拓展功能界面！")
        self.scaGallery = TabCanvas(defaultTabType=TabType(
            widget=OptLabel.textBuild(
                minw=400,
                minh=400,
                qss='background-color:skyblue',
                text="散点图！"
            ),
            title="导航",
        ))
        self.lineGallery = TabCanvas(defaultTabType=TabType(
                widget=OptLabel.textBuild(
                    minw=400,
                    minh=400,
                    qss='background-color:skyblue',
                    text="线型图！"
                ),
                title="导航",
        ))
        self.pieGallery = TabCanvas(defaultTabType=TabType(
                widget=OptLabel.textBuild(
                    minw=400,
                    minh=400,
                    qss='background-color:skyblue',
                    text="饼状图！"
                ),
                title="导航",
        ))
        self.barGallery = TabCanvas(defaultTabType=TabType(
                widget=OptLabel.textBuild(
                    minw=400,
                    minh=400,
                    qss='background-color:skyblue',
                    text="柱状图！"
                ),
                title="导航",
        ))
        self.mixinGallery = TabCanvas(defaultTabType=TabType(
                widget=OptLabel.textBuild(
                    minw=400,
                    minh=400,
                    qss='background-color:skyblue',
                    text="混合图！"
                ),
                title="导航",
        ))
        self.sidebar = SideBar(
            leader_func=lambda: self.setStackIndex(0),
            scatter_func=lambda: self.setStackIndex(1),
            line_func=lambda: self.setStackIndex(2),
            bar_func=lambda: self.setStackIndex(3),
            pie_func=lambda: self.setStackIndex(4)
        )

        self.__setUI()

    def __setUI(self) -> None:
        self.setCentralWidget(
            OptSplitter(
                horizontal=True,
                widgets=[
                    self.sidebar,
                    Stack(
                        minw=400,
                        widgets=[
                            self.homePage,
                            self.scaGallery,
                            self.lineGallery,
                            self.barGallery,
                            self.pieGallery,
                        ],
                        currentIndex=0,
                        objectName='stack'
                    )
                ]
            )
        )

        self.scaGallery.linkOpenFunction(self.drawScatter)
        self.lineGallery.linkOpenFunction(self.drawLineOrCurve)
        self.barGallery.linkOpenFunction(self.drawBar)
        self.pieGallery.linkOpenFunction(self.drawPie)
        self.register(self.mixinGallery, '混合图', qt_icon('mdi6.chart-multiple'))

        apply_stylesheet(self, theme='light_blue.xml')

        menubar = QMenuBar(self)
        toggleThemeBtn = QAction("随即切换主题", menubar)
        toggleThemeBtn.triggered.connect(lambda : apply_stylesheet(self, theme=list_themes()[random.randint(0, 19)]))
        menubar.addAction(toggleThemeBtn)
        self.setMenuBar(menubar)
       
    def setStackIndex(self, index: int) -> None:
        stack: Stack = self.findChild(Stack, 'stack')
        if index != stack.currentIndex:
            stack.setCurrentIndex(index)

    def setStackWidget(self, widget : QWidget) -> None:
        stack: Stack = self.findChild(Stack, 'stack')
        if widget != stack.currentWidget():
            stack.setCurrentWidget(widget)

    def absract_draw(self, what_to_do : str, PlotWrapper, Widget, Gallery : TabCanvas):
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            what_to_do,
            "C:/",
            "模板(*.json)"
        )
        if fileName:
            try:
                wrapper = PlotWrapper(fileName).data
                Gallery.append(TabType(
                    widget=Widget(wrapper=wrapper),
                    title=wrapper.get('title')
                ))
            except Exception as e:
                w = AbstractWidget()
                w.setUniqueWidget(
                    widget=OptLabel.textBuild(text=e.__str__(), textWrap=True),
                    contentMargins=[0, 0, 0, 0]
                )
                Gallery.append(TabType(
                    widget=w,
                    title=str(type(e))
                ))
            Gallery.setCurrentPath(fileName)
        else:
            Gallery.setCurrentPath("Lost FilePath!")

    def drawScatter(self): self.absract_draw("打开散点图模板", ScatterWrapper, ValueAxisSeriesView, self.scaGallery)
    def drawLineOrCurve(self): self.absract_draw("打开线型图模板", LineCurveWrapper, ValueAxisSeriesView, self.lineGallery)
    def drawBar(self): self.absract_draw("打开柱状图模板", BarWrapper, BarSeriesView, self.barGallery)
    def drawPie(self): self.absract_draw("打开饼状图模板", PieWrapper, PieSeriesView, self.pieGallery)

    def register(self, widget : QWidget, name : str, icon) -> None:
        self.findChild(Stack, 'stack').addWidget(widget)
        self.sidebar.append(name, lambda : self.setStackWidget(widget), icon)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("SimpleDrawer")
    app.setWindowIcon(QIcon('logo.svg'))
    ui = SimpleDrawer()

    # 拓展案例
    ui.register(PygwalkerOpt(), "pygwalker可视化", qt_icon('mdi.lightning-bolt'))

    ui.show()
    sys.exit(app.exec_())