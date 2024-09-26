from PyQt5.QtChart import *
from PyQt5.QtGui import QPainter

ShapeMap = {
    'c' : QScatterSeries.MarkerShape.MarkerShapeCircle,
    'r' : QScatterSeries.MarkerShape.MarkerShapeRectangle
}

ChartThemeMap = {
    0 : QChart.ChartTheme.ChartThemeLight,
    1 : QChart.ChartTheme.ChartThemeBlueCerulean,
    2 : QChart.ChartTheme.ChartThemeDark,
    3 : QChart.ChartTheme.ChartThemeBrownSand,
    4 : QChart.ChartTheme.ChartThemeBlueNcs,
    5 : QChart.ChartTheme.ChartThemeHighContrast,
    6 : QChart.ChartTheme.ChartThemeBlueIcy,
    7 : QChart.ChartTheme.ChartThemeQt
}

RubberBandMap = {
    0 : QChartView.RubberBand.NoRubberBand,
    1 : QChartView.RubberBand.HorizontalRubberBand,
    2 : QChartView.RubberBand.VerticalRubberBand,
    3 : QChartView.RubberBand.RectangleRubberBand
}

HintsMap = {
    0 : QPainter.RenderHint.Antialiasing,
    1 : QPainter.RenderHint.HighQualityAntialiasing,
    2 : QPainter.RenderHint.LosslessImageRendering,
    3 : QPainter.RenderHint.NonCosmeticDefaultPen,
    4 : QPainter.RenderHint.TextAntialiasing,
    5 : QPainter.RenderHint.SmoothPixmapTransform,
    6 : QPainter.RenderHint.Qt4CompatiblePainting
}

AnimationOptionsMap = {
    0 : QChart.AnimationOption.NoAnimation,
    1 : QChart.AnimationOption.AllAnimations,
    2 : QChart.AnimationOption.GridAxisAnimations,
    3 : QChart.AnimationOption.SeriesAnimations
}

BarSeriesMap = {
    0 : QBarSeries,
    1 : QStackedBarSeries,
    2 : QPercentBarSeries,
    3 : QHorizontalBarSeries,
    4 : QHorizontalStackedBarSeries,
    5 : QHorizontalPercentBarSeries
}