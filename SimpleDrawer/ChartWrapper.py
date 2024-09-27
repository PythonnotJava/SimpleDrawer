import sys
import json
from collections import UserDict
from os import PathLike
from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtChart import *

from SideBar import SideBar
from OptimizeQt import *
from WarpperBase import *
from Series import *

def translatePoints(src : dict) -> Union[List[QPointF], List[List[QPointF]]]:
    xs = src['xs']
    ys = src['ys']
    get = []
    if isinstance(xs[0], list):
        for i, xi in enumerate(xs):
            tp = []
            yi = ys[i]
            for index, value in enumerate(xi):
                tp.append(QPointF(value, yi[index]))
            get.append(tp)
    else:
        for index, value in enumerate(xs):
            get.append(QPointF(value, ys[index]))
    return get

class ScatterWrapper:
    def __init__(self, path : Union[PathLike, str]):
        settings = json.load(open(path, 'r', encoding='utf-8'))
        shape = settings['shape']
        if isinstance(shape, str):
            self.__data = dict(
                title=settings.get('title', 'Unknow'),
                series=ScatterSeries(
                    markerShape=ShapeMap[shape],
                    markerSize=settings.get('size', 10.),
                    points=translatePoints(settings),
                    color=settings['color'],
                    name=settings['categories'],
                ),
                mult=False,
                theme=ChartThemeMap[settings.get('theme', 0)],
                xrange=settings.get('xrange', None),
                yrange = settings.get('yrange', None),
                polar=settings.get('polar', False),
                xlabel=settings.get('xlabel', None),
                ylabel=settings.get('ylabel', None)
            )
        else:
            scaseries = []
            ps : List[List[QPointF]] = translatePoints(settings)
            for i, s in enumerate(shape):
                scaseries.append(ScatterSeries(
                    markerShape=ShapeMap[s],
                    markerSize=settings['size'][i],
                    points=ps[i],
                    color=settings['color'][i],
                    name=settings['categories'][i]
                ))
            self.__data = dict(
                title=settings.get('title', 'Unknow'),
                series=scaseries,
                mult=True,
                theme=ChartThemeMap[settings.get('theme', 0)],
                xrange=settings.get('xrange', None),
                yrange=settings.get('yrange', None),
                polar=settings.get('polar', False),
                xlabel=settings.get('xlabel', None),
                ylabel=settings.get('ylabel', None)
            )
    @property
    def data(self) -> dict: return self.__data

class LineCurveWrapper:
    def __init__(self, path: Union[PathLike, str]):
        settings = json.load(open(path, 'r', encoding='utf-8'))
        color = settings['color']
        if isinstance(color, str):
            self.__data = dict(
                title=settings.get('title', 'Unknow'),
                series=LineSeries(
                    points=translatePoints(settings),
                    color=settings['color'],
                    name=settings['categories'],
                    lw=settings['lw']
                ) if settings.get('type', 0) == 0
                else LineSeries(
                    points=translatePoints(settings),
                    color=settings['color'],
                    name=settings['categories'],
                    lw=settings['lw']
                ),
                mult=False,
                theme=ChartThemeMap[settings.get('theme', 0)],
                xrange=settings.get('xrange', None),
                yrange=settings.get('yrange', None),
                polar=settings.get('polar', False),
                xlabel=settings.get('xlabel', None),
                ylabel=settings.get('ylabel', None)
            )
        else:
            scaseries = []
            ps: List[List[QPointF]] = translatePoints(settings)
            types = {
                0 : LineSeries,
                1 : CurveSeries
            }
            for i, s in enumerate(color):
                scaseries.append(types.get(settings['type'][i], 0)(
                    points=ps[i],
                    color=settings['color'][i],
                    name=settings['categories'][i],
                    lw=settings['lw'][i]
                ))
            self.__data = dict(
                title=settings.get('title', 'Unknow'),
                series=scaseries,
                mult=True,
                theme=ChartThemeMap[settings.get('theme', 0)],
                xrange=settings.get('xrange', None),
                yrange=settings.get('yrange', None),
                polar=settings.get('polar', False),
                xlabel=settings.get('xlabel', None),
                ylabel=settings.get('ylabel', None)
            )

    @property
    def data(self) -> dict:
        return self.__data

class BarWrapper:
    def __init__(self, path: Union[PathLike, str]):
        settings = json.load(open(path, 'r', encoding='utf-8'))
        color = settings['color']
        k = settings.get('type', 0)
        series = BarSeriesMap.get(k, QBarSeries)()
        series.setBarWidth(settings.get('bw', 0.5))
        isDefaultColor = settings.get('default-color', False)
        series.setLabelsVisible(settings.get('value-visible', True))
        if isinstance(color, str):
            barSets = QBarSet(settings.get('categories', 'Unknow'))
            barSets.append(settings['datas'])
            if not isDefaultColor:
                barSets.setColor(QColor(settings.get('color', 'black')))
            series.append(barSets)
            self.__data = dict(
                title=settings.get('title', 'Unknow'),
                theme=ChartThemeMap[settings.get('theme', 0)],
                mult=False,
                rorate=int(settings.get('rorate', 0)),
                labels=settings['labels'],
                series=series,
                ishor=k >= 3,
                xlabel=settings.get('xlabel', None),
                ylabel=settings.get('ylabel', None)
            )
        else:
            for index, c in enumerate(color):
                barSet = QBarSet(settings.get('categories')[index])
                barSet.append(settings['datas'][index])
                if not isDefaultColor:
                    barSet.setColor(QColor(settings.get('color')[index]))
                series.append(barSet)
            self.__data = dict(
                title=settings.get('title', 'Unknow'),
                theme=ChartThemeMap[settings.get('theme', 0)],
                mult=False,  # Bar只能有一个
                series=series,
                rorate=int(settings.get('rorate', 0)),
                labels=settings['labels'],
                ishor=k >= 3,
                xlabel=settings.get('xlabel', None),
                ylabel=settings.get('ylabel', None)
            )

    @property
    def data(self) -> dict: return self.__data

class PieWrapper:
    def __init__(self, path : Union[PathLike, str]):
        settings = json.load(open(path, 'r', encoding='utf-8'))
        isDatasVisible = settings.get('datas-visible', True)
        isUsePercentage = settings.get('use-percentage', True)
        ft = settings.get('format', 0)
        names = settings['categories']
        series = PieSeries(
            labelsVisible=settings.get('label-visible', True),
            hole=settings.get('hole', 0),
            names=names,
            datas=settings['datas'],
            isDefaultColor=settings.get('default-color', False),
            colors=settings['color']
        )

        if isDatasVisible and isUsePercentage:  # 数据可见并且采用百分比模式
            for sl in series.slices():
                sl.setLabel(f"{sl.percentage() * 100:.{ft}f}%")
        elif isDatasVisible and not isUsePercentage:  # 数据可见并且正常显示原数据
            for sl in series.slices():
                sl.setLabel(f"{sl.percentage()}")
        else:  # 不显示数据
            pass

        self.__data = dict(
            title=settings.get('title', 'Unknow'),
            theme=ChartThemeMap[settings.get('theme', 0)],
            mult=False,
            series=series,
            isLegendVisible=True,
            names=names
        )

    @property
    def data(self) -> dict: return self.__data

class ChartContainerMixin(QChartView):
    def __init__(self, wrapper : dict):
        super().__init__()
        self.wrapper = wrapper
        self.isPolar = wrapper.get('polar', False)  # 不管有没有这个属性
        self.chart = QChart() if not self.isPolar else QPolarChart()

        self.__setBaseUI()
    def __setBaseUI(self) -> None:
        if self.wrapper.get('mult'):
            series: List[QAbstractSeries] = self.wrapper.get('series')
            for s in series:
                self.chart.addSeries(s)
        else:
            self.chart.addSeries(self.wrapper.get('series'))

        self.setChart(self.chart)
        self.chart.setTheme(self.wrapper.get('theme'))
        self.chart.setTitle(self.wrapper.get('title'))

        self.chart.createDefaultAxes()

        # global
        globalSetting = json.load(open('config.json', 'r', encoding='U8'))
        self.setRenderHint(HintsMap[globalSetting['hints']])
        self.setRubberBand(RubberBandMap[globalSetting['rubberBand']])
        self.chart.setAnimationDuration(globalSetting['animationDuration'])
        self.chart.setAnimationOptions(AnimationOptionsMap[globalSetting['animationOptions']])

    def contextMenuEvent(self, e) -> None:
        menu = QMenu(self)
        saveToAct = QAction("保存图片", menu)
        saveToAct.triggered.connect(self.__saveToAct)
        resetThemeAct = QAction('重置主题', menu)
        resetThemeMenu = QMenu()
        for index in range(8):
            resetThemeMenu.addAction(self.__create_action(index, resetThemeMenu))
        resetThemeAct.setMenu(resetThemeMenu)
        ifHideGridAct = QAction("显示/隐藏网格线", menu)
        ifHideGridAct.triggered.connect(self.__ifHideGridAct)
        menu.addActions([saveToAct, resetThemeAct, ifHideGridAct])
        menu.exec_(e.globalPos())

    def __ifHideGridAct(self) -> None:
        if self.isPolar:
            self.chart : QPolarChart
            xaxis : QAbstractAxis = self.chart.axes(QPolarChart.PolarOrientation.PolarOrientationRadial)[0]
            yaxis : QAbstractAxis = self.chart.axes(QPolarChart.PolarOrientation.PolarOrientationAngular)[0]
        else:
            xaxis = self.chart.axes()[0]
            yaxis = self.chart.axes()[1]
        xaxis.setGridLineVisible(not xaxis.isGridLineVisible())
        xaxis.setMinorGridLineVisible(not xaxis.isMinorGridLineVisible())
        yaxis.setGridLineVisible(not yaxis.isGridLineVisible())
        yaxis.setMinorGridLineVisible(not yaxis.isMinorGridLineVisible())

    def __create_action(self, theme, resetThemeMenu):
        action = QAction(str(theme), resetThemeMenu)
        action.triggered.connect(lambda: self.chart.setTheme(theme))
        return action

    def __saveToAct(self) -> None:
        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "选择保存路径",
            "C://",
            "png(*.png);;jpg(*.jpg);;jpeg(*.jpeg)"
        )
        if fileName:
            self.grab().save(fileName)

# 数值轴类图，散点图、线性图都可以是
class ValueAxisSeriesView(ChartContainerMixin):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__setUI()

    def __setUI(self) -> None:
        if not self.isPolar:
            xaxis = self.chart.axes(Qt.Orientation.Horizontal)[0]
            yaxis = self.chart.axes(Qt.Orientation.Vertical)[0]
        else:
            xaxis = self.chart.axes()[0]
            yaxis = self.chart.axes()[1]

        if self.wrapper['xrange']:
            xaxis.setRange(*self.wrapper['xrange'])
        if self.wrapper['yrange']:
            yaxis.setRange(*self.wrapper['yrange'])

        if self.wrapper['xlabel']:
            xaxis.setTitleText(self.wrapper['xlabel'])
        if self.wrapper['ylabel']:
            yaxis.setTitleText(self.wrapper['ylabel'])

# 柱状图
class BarSeriesView(ChartContainerMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.isPolar = False

        self.__setUI()
    def __setUI(self) -> None:
        axis = QBarCategoryAxis()
        axis.append(self.wrapper['labels'])
        axis.setLabelsAngle(self.wrapper['rorate'])
        series = self.wrapper['series']
        series.attachAxis(axis)
        self.chart.setAxisY(axis, series) if self.wrapper['ishor'] else self.chart.setAxisX(axis, series)

        xaxis = self.chart.axisX(series)
        yaxis = self.chart.axisY(series)
        if self.wrapper['xlabel']:
            xaxis.setTitleText(self.wrapper['xlabel'])
        if self.wrapper['ylabel']:
            yaxis.setTitleText(self.wrapper['ylabel'])

# 饼状图
class PieSeriesView(ChartContainerMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.isPolar = False
        lg : QLegend = self.chart.legend()
        mks : List[QLegendMarker] = lg.markers(self.wrapper['series'])
        for index, mk in enumerate(mks):
            mk.setLabel(self.wrapper['names'][index])

if __name__ == '__main__':
    # print(PieWrapper("../template/pie.template.json").data)
    app = QApplication([])
    ui = QMainWindow()
    ui.setCentralWidget(PieSeriesView(wrapper=PieWrapper("../template/pie.template.json").data))
    ui.show()
    app.exec()