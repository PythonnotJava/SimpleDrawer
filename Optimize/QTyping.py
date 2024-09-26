from typing import Optional, Union, Literal, Dict
from dataclasses import dataclass

from PyQt5.QtChart import QAbstractSeries, QAbstractAxis
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLayout, QWidget
from PyQt5.QtGui import QIcon, QColor, QPen, QBrush, QGradient

ColorType = Union[QColor, Qt.GlobalColor, QGradient, None]
ColorTypeWithPen = Union[QPen, QColor, Qt.GlobalColor, QGradient, None]
ColorTypeWithBrush = Union[QBrush, QColor, Qt.GlobalColor, QGradient, None]

# 用于抽象基类的声明布局
@dataclass
class WidgetOrLayoutType:
    dtype: Literal[0, 1]
    obj: Union[QLayout, QWidget]
    align: Qt.Alignment | Qt.AlignmentFlag = Qt.Alignment()

@dataclass
class IconWithStringType:
    icon : Union[str, QIcon]
    name : str

@dataclass
class TabCfgType:
    widget : QWidget
    icon : Union[str, QIcon]
    label : str
    toolTip : Optional[str] = None

# 简易的按钮各种状态的qss生成器，只需导入各种状态的前景颜色、背景颜色即可，其他属性可以通过setattr动态设置
class ButtonStateQssSimpleGenerator(str):
    def __new__(cls,
                normalForegroundColor : Union[QColor, Qt.GlobalColor] = Qt.black,
                hoverForegroundColor : Union[QColor, Qt.GlobalColor] = Qt.black,
                pressedForegroundColor : Union[QColor, Qt.GlobalColor] = Qt.black,
                disabledForegroundColor : Union[QColor, Qt.GlobalColor] = Qt.black,
                normalBackgroundColor : Union[QColor, Qt.GlobalColor] = Qt.white,
                hoverBackgroundColor : Union[QColor, Qt.GlobalColor] = QColor('lightskyblue'),
                pressedBackgroundColor : Union[QColor, Qt.GlobalColor] = QColor('#d98a92'),
                disabledBackgroundColor : Union[QColor, Qt.GlobalColor] = Qt.lightGray,
                ):
        qss_template = """
        /* Normal state */
        QPushButton {{
            color: {};
            background-color: {};
        }}

        /* Hover state */
        QPushButton:hover {{
            color: {};
            background-color: {};
        }}

        /* Pressed state */
        QPushButton:pressed {{
            color: {};
            background-color: {};
        }}

        /* Disabled state */
        QPushButton:disabled {{
            color: {};
            background-color: {};
        }}
        """.format(QColor(normalForegroundColor).name(),
                   QColor(normalBackgroundColor).name(),
                   QColor(hoverForegroundColor).name(),
                   QColor(hoverBackgroundColor).name(),
                   QColor(pressedForegroundColor).name(),
                   QColor(pressedBackgroundColor).name(),
                   QColor(disabledForegroundColor).name(),
                   QColor(disabledBackgroundColor).name())

        return super(ButtonStateQssSimpleGenerator, cls).__new__(cls, qss_template)

__all__ = [
    'WidgetOrLayoutType',
    'IconWithStringType',
    'TabCfgType',
    'ButtonStateQssSimpleGenerator',
    'ColorType',
    'ColorTypeWithPen',
    'ColorTypeWithBrush'
]
