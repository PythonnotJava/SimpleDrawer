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

from SideBar import SideBar
from OptimizeQt import *
from CanvasUI import *
from WalkerWebview import PygwalkerOpt
from MenuBar import MenuBar
from DefaultCanvas import *
from StateVarious import StateVarious
from AskDlg import *
from ToolKit import *

WHATTHIS = "Find Simple tools in Drawer."

class SimpleDrawer(QMainWindow, AbstractWidget):
    GlobalSettings = json.load(open('config.json', 'r', encoding='u8'))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.homePage = HomePageView()
        self.scaGallery = TabCanvas(defaultTabType=TabType(
            widget=DefaultDrawPageView('doc/scatter.template.md'),
            title="导航",
        ))
        self.lineGallery = TabCanvas(defaultTabType=TabType(
                widget=DefaultDrawPageView('doc/line.template.md'),
                title="导航",
        ))
        self.pieGallery = TabCanvas(defaultTabType=TabType(
                widget=DefaultDrawPageView('doc/pie.template.md'),
                title="导航",
        ))
        self.barGallery = TabCanvas(defaultTabType=TabType(
                widget=DefaultDrawPageView('doc/bar.template.md'),
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

        self.menubar = MenuBar(p=self, s=self.GlobalSettings, dy=lambda : DWidgetLoader()(self))
        self.statebar = StateVarious()

        self.trayicon = SystemTrayIcon(QIcon("logo.svg"), self)

        self.hidesc = QShortcut(QKeySequence(self.GlobalSettings['shortcuts']['mini']), self)

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
        apply_stylesheet(self, theme=self.GlobalSettings['defaultMainTheme'])
        self.setMenuBar(self.menubar)
        self.setStatusBar(self.statebar)
        self.trayicon.show()
        self.setAcceptDrops(True)

        # 快捷键设置
        self.hidesc.activated.connect(lambda : self.showMinimized())
       
    def setStackIndex(self, index: int) -> None:
        stack: Stack = self.findChild(Stack, 'stack')
        if index != stack.currentIndex:
            stack.setCurrentIndex(index)

    def setStackWidget(self, widget : QWidget) -> None:
        stack: Stack = self.findChild(Stack, 'stack')
        if widget != stack.currentWidget():
            stack.setCurrentWidget(widget)

    def __loadFile(
            self,
            Gallery : TabCanvas,
            PlotWrapper,
            Widget, fileName) -> None:
        try:
            wrapper = PlotWrapper(path=fileName).data
            Gallery.append(TabType(
                widget=Widget(wrapper=wrapper),
                title=wrapper.get('title')
            ))
            self.statebar.showMessage("绘图成功！", 2500)
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
            self.statebar.showMessage("绘图失败！", 2500)
        Gallery.setCurrentPath(fileName)

    def absract_draw(self, what_to_do : str, PlotWrapper, Widget, Gallery : TabCanvas):
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            what_to_do,
            "C:/",
            "模板(*.json)"
        )
        if fileName:
            self.__loadFile(Gallery, PlotWrapper, Widget, fileName)
        else:
            Gallery.setCurrentPath("Lost FilePath!")
            self.statebar.showMessage("取消选择！", 2500)

    def drawScatter(self): self.absract_draw("打开散点图模板", ScatterWrapper, ValueAxisSeriesView, self.scaGallery)
    def drawLineOrCurve(self): self.absract_draw("打开线型图模板", LineCurveWrapper, ValueAxisSeriesView, self.lineGallery)
    def drawBar(self): self.absract_draw("打开柱状图模板", BarWrapper, BarSeriesView, self.barGallery)
    def drawPie(self): self.absract_draw("打开饼状图模板", PieWrapper, PieSeriesView, self.pieGallery)

    def closeEvent(self, e: QCloseEvent) -> None:
        if self.menubar.defaultMainTheme:
            self.GlobalSettings['defaultMainTheme'] = self.menubar.defaultMainTheme

        if self.GlobalSettings['exit-ask']:
            exitDlg = ExitDlg(self.GlobalSettings)
            exitDlg.whatToDo.connect(lambda x: self.__isExitAsk(exitDlg, x))
            result = exitDlg.exec_()

            if result == QDialog.Rejected:  # 点击×号
                e.ignore()
                return

        json.dump(self.GlobalSettings, open('config.json', 'w'), indent=4)
        super().closeEvent(e)

    def __isExitAsk(self, dlg: ExitDlg, signal: int) -> None:
        if signal == 0:  # 最小化到托盘
            dlg.close()
            self.hide()
        elif signal == 1:  # 退出
            QApplication.instance().quit()
        elif signal == 2:  # 取消
            dlg.close()

    # 支持拖入画图
    def dragEnterEvent(self, e: QDragEnterEvent, *args):
        if e.mimeData() is not None and e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent, *args):
        if e.mimeData().hasUrls():
            url = e.mimeData().urls()[0]
            filePath = url.toLocalFile()
            try:
                wrapper = json.load(open(filePath, 'r', encoding='u8'))
                drawType = wrapper['class'].lower()
                match drawType:
                    case 'scatter':
                        self.__loadFile(self.scaGallery, ScatterWrapper, ValueAxisSeriesView, filePath)
                        self.setStackWidget(self.scaGallery)
                    case 'line':
                        self.__loadFile(self.lineGallery, LineCurveWrapper, ValueAxisSeriesView, filePath)
                        self.setStackWidget(self.lineGallery)
                    case 'bar':
                        self.__loadFile(self.barGallery, BarWrapper, BarSeriesView, filePath)
                        self.setStackWidget(self.barGallery)
                    case 'pie':
                        self.__loadFile(self.pieGallery, PieWrapper, PieSeriesView, filePath)
                        self.setStackWidget(self.pieGallery)
                    case _:
                        self.statebar.showMessage('不支持类型的图列', 2500)
            except:
                self.statebar.showMessage('未知类型的图列', 2500)

    # 核心外置接口函数
    #############################################################################################
    # 注册控件
    def register(self, widget : QWidget, name : str, icon) -> None:
        self.findChild(Stack, 'stack').addWidget(widget)
        self.sidebar.append(name, lambda : self.setStackWidget(widget), icon)
    #############################################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("SimpleDrawer")
    app.setWindowIcon(QIcon('logo.svg'))
    ui = SimpleDrawer()
    # 拓展案例
    ui.register(PygwalkerOpt(), "pygwalker可视化", qt_icon('mdi.lightning-bolt'))
    ui.show()
    sys.exit(app.exec_())