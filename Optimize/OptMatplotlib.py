from matplotlib import use as matplotlib_use
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtCore import Qt

from .ABSW import AbstractWidget
from .OptLayout import Row

matplotlib_use('Qt5Agg')

class MatplotlibQtFigure(AbstractWidget):
    def __init__(self,
                 figure : Figure,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.figure = figure
        self.canvas = FigureCanvasQTAgg(self.figure)  # 这是一个Widget

        self.setLayout(
            Row.singleWidgetBuild(
                widget=self.canvas,
                align=Qt.AlignCenter
            )
        )

    # 需要即时绘制的时候要连接这个方法
    def draw(self):
        self.canvas.draw()

__all__ = ["MatplotlibQtFigure"]

