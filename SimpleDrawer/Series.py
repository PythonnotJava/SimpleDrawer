from typing import *

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtChart import *
from PyQt5.QtCore import *

from OptimizeQt import AbstractWidget

# 散点图
class ScatterSeries(QScatterSeries):
    def __init__(
            self,
            points : Iterable[Union[QPointF, QPoint]],
            name : str = 'Name',
            color : str = 'blue',
            markerShape : QScatterSeries.MarkerShape = QScatterSeries.MarkerShapeCircle,
            markerSize : float = 10.,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.setMarkerSize(markerSize)
        self.setMarkerShape(markerShape)
        self.setColor(QColor(color))
        self.setName(name)
        self.append(points)

# 折线图
class LineSeries(QLineSeries):
    def __init__(
            self,
            points: Iterable[Union[QPointF, QPoint]],
            name: str = 'Name',
            color: str = 'blue',
            lw : float = 5.,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.append(points)
        self.setName(name)
        self.setPen(QPen(QColor(color), lw))

# 曲线图
class CurveSeries(QSplineSeries):
    def __init__(
            self,
            points: Iterable[Union[QPointF, QPoint]],
            name: str = 'Name',
            color: str = 'blue',
            lw : float = 5.,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.append(points)
        self.setName(name)
        self.setPen(QPen(QColor(color), lw))

# 饼状图
class PieSeries(QPieSeries):
    def __init__(
            self,
            names : List,
            datas : List,
            hole : float = 0.0,
            labelsVisible : bool = True,
            isDefaultColor : bool = False,
            colors : Optional[List] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if isDefaultColor:
            for index, value in enumerate(names):
                self.append(value, datas[index])
        else:
            for index, value in enumerate(names):
                sl = QPieSlice(value, datas[index])
                self.append(sl)
                sl.setColor(QColor(colors[index]))

        self.setHoleSize(hole)
        self.setLabelsVisible(labelsVisible)
        self.hovered.connect(self.__hovered)

    @staticmethod
    def __hovered(s : QPieSlice, state : bool):
        if state:
            s.setPen(QPen(Qt.red, 3))
            s.setExploded(True)
        else:
            s.setPen(QPen(s.color(), 0))
            s.setExploded(False)
