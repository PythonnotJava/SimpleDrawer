# 滑动条

from typing import Callable, Optional

from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

from .ABSW import AbstractWidget

class OptSlider(QSlider, AbstractWidget):
    def __init__(self,
                 minNumber: int,
                 maxNumber: int,
                 step: int,
                 defaultValue: Optional[int] = None,
                 horizontal: bool = True,
                 valueChangedFunction: Callable = lambda _: ...,  # 值变化就显示效果，函数回调必须传入值，这个值即滑条value
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setMinimum(minNumber)
        self.setMaximum(maxNumber)
        self.setSingleStep(step)
        self.setValue(defaultValue if defaultValue else 0)
        self.setOrientation(Qt.Horizontal if horizontal else Qt.Vertical)
        self.valueChanged.connect(valueChangedFunction)

__all__ = ['OptSlider']
