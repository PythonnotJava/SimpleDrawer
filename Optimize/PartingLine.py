# 分割线
from typing import Union

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt

from .ABSW import AbstractWidget

class PartingLine(QFrame, AbstractWidget):
    def __init__(self,
                 shadow: Union[QFrame.Shadow, int] = QFrame.Shadow.Plain,
                 horizontal: bool = True,
                 width: int = 10,
                 color: Union[QColor, Qt.GlobalColor, str] = '#000000',
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setFrameShadow(shadow)
        self.setLineWidth(width)
        if horizontal:
            self.setFrameShape(QFrame.Shape.HLine)
        else:
            self.setFrameShape(QFrame.Shape.VLine)
        if isinstance(color, QColor):
            self.setStyleSheet(f'color : {color.name()};')
        elif isinstance(color, str):
            self.setStyleSheet(f'color : {color};')
        else:
            self.setStyleSheet(f'color : {QColor(color).name()};')

    @classmethod
    def hLine(cls,
              shadow: Union[QFrame.Shadow, int] = QFrame.Shadow.Plain,
              width: int = 10,
              color: Union[QColor, Qt.GlobalColor, str] = '#000000',
              **kwargs
              ):
        return cls(
            width=width,
            shadow=shadow,
            horizontal=True,
            color=color,
            **kwargs
        )

    @classmethod
    def vLine(cls,
              shadow: Union[QFrame.Shadow, int] = QFrame.Shadow.Plain,
              width: int = 10,
              color: Union[QColor, Qt.GlobalColor, str] = '#000000',
              **kwargs
              ):
        return cls(
            width=width,
            shadow=shadow,
            horizontal=False,
            color=color,
            **kwargs
        )
