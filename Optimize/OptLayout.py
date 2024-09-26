# 布局

from typing import Optional, Sequence, Union
from functools import singledispatchmethod

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QLayout, QHBoxLayout, QVBoxLayout, QGridLayout

from .ABSW import AbstractWidget

class Row(QHBoxLayout):
    def __init__(self,
                 widgets: Optional[Sequence[QWidget]] = None,
                 lays: Optional[Sequence[QLayout]] = None,
                 mixin: Optional[Sequence] = None,
                 aligns: Union[
                     Qt.Alignment,
                     Sequence[Qt.Alignment],
                     Qt.AlignmentFlag,
                     Sequence[Qt.AlignmentFlag]
                 ] = Qt.Alignment(),
                 stretch: int = 1
                 ):
        """
        三种模式只能用一种
        :param widgets: 控件模式
        :param lays: 布局模式
        :param mixin: 混合模式
        :param aligns: 控件模式下统一布局或者分开布局（序列类型且前提等长）；布局模式或者混合模式下统一布局
        :param stretch: 间距
        """
        super().__init__()
        if widgets:
            if isinstance(aligns, (Qt.Alignment, Qt.AlignmentFlag)):
                aligns = [aligns] * len(widgets)
            for wt, al in zip(widgets, aligns):
                self.addWidget(wt, stretch=stretch, alignment=al)

        if lays:
            for ly in lays:
                self.addLayout(ly, stretch=stretch)

        if mixin:
            for wl in mixin:
                if isinstance(wl, QLayout):
                    self.addLayout(wl, stretch=stretch)
                else:
                    self.addWidget(wl, stretch=stretch)

        if isinstance(aligns, (Qt.Alignment, Qt.AlignmentFlag)):
            self.setAlignment(aligns)

    @classmethod
    def widgetsBuild(cls,
                     widgets: Sequence[QWidget],
                     aligns: Union[
                         Qt.Alignment,
                         Sequence[Qt.Alignment],
                         Qt.AlignmentFlag,
                         Sequence[Qt.AlignmentFlag]
                     ] = Qt.Alignment(),
                     stretch: int = 1
                     ):
        return cls(
            widgets=widgets,
            lays=None,
            mixin=None,
            aligns=aligns,
            stretch=stretch
        )

    @classmethod
    def laysBuild(cls,
                  lays: Sequence[QLayout],
                  aligns: Union[
                      Qt.Alignment,
                      Sequence[Qt.Alignment],
                      Qt.AlignmentFlag,
                      Sequence[Qt.AlignmentFlag]
                  ] = Qt.Alignment(),
                  stretch: int = 1
                  ):
        return cls(
            lays=lays,
            stretch=stretch,
            aligns=aligns,
            mixin=None,
            widgets=None
        )

    @classmethod
    def singleWidgetBuild(cls, widget: QWidget, align: Qt.Alignment | Qt.AlignmentFlag = Qt.Alignment()):
        self = cls()
        self.addWidget(widget, alignment=align)
        return self

    def resetContentsMargins(self, left, top, right, bottom) -> 'Row':
        self.setContentsMargins(left, top, right, bottom)
        return self

class Column(QVBoxLayout):
    def resetContentsMargins(self, left, top, right, bottom) -> 'Column':
        self.setContentsMargins(left, top, right, bottom)
        return self

    def __init__(self,
                 widgets: Optional[Sequence[QWidget]] = None,
                 lays: Optional[Sequence[QLayout]] = None,
                 mixin: Optional[Sequence] = None,
                 aligns: Union[
                     Qt.Alignment,
                     Sequence[Qt.Alignment],
                     Qt.AlignmentFlag,
                     Sequence[Qt.AlignmentFlag]
                 ] = Qt.Alignment(),
                 stretch: int = 1
                 ):
        """
        三种模式只能用一种
        :param widgets: 控件模式
        :param lays: 布局模式
        :param mixin: 混合模式
        :param aligns: 控件模式下统一布局或者分开布局（序列类型且前提等长）；布局模式或者混合模式下统一布局
        :param stretch: 间距
        """
        super().__init__()
        if widgets:
            if isinstance(aligns, (Qt.Alignment, Qt.AlignmentFlag)):
                aligns = [aligns] * len(widgets)
            for wt, al in zip(widgets, aligns):
                self.addWidget(wt, stretch=stretch, alignment=al)

        if lays:
            for ly in lays:
                self.addLayout(ly, stretch=stretch)

        if mixin:
            for wl in mixin:
                if isinstance(wl, QLayout):
                    self.addLayout(wl, stretch=stretch)
                else:
                    self.addWidget(wl, stretch=stretch)

        if isinstance(aligns, (Qt.Alignment, Qt.AlignmentFlag)):
            self.setAlignment(aligns)

    @classmethod
    def widgetsBuild(cls,
                     widgets: Sequence[QWidget],
                     aligns: Union[
                         Qt.Alignment,
                         Sequence[Qt.Alignment],
                         Qt.AlignmentFlag,
                         Sequence[Qt.AlignmentFlag]
                     ] = Qt.Alignment(),
                     stretch: int = 1
                     ):
        return cls(
            widgets=widgets,
            lays=None,
            mixin=None,
            aligns=aligns,
            stretch=stretch
        )

    @classmethod
    def laysBuild(cls,
                  lays: Sequence[QLayout],
                  aligns: Union[
                      Qt.Alignment,
                      Sequence[Qt.Alignment],
                      Qt.AlignmentFlag,
                      Sequence[Qt.AlignmentFlag]
                  ] = Qt.Alignment(),
                  stretch: int = 1
                  ):
        return cls(
            lays=lays,
            stretch=stretch,
            aligns=aligns,
            mixin=None,
            widgets=None
        )

    @classmethod
    def singleWidgetBuild(cls, widget: QWidget, align: Qt.Alignment | Qt.AlignmentFlag = Qt.Alignment()):
        self = cls()
        self.addWidget(widget, alignment=align)
        return self


# 一是可用来设置两个widget之间的间距，二是可以用来限制子组件的大小。
class SizedBox(AbstractWidget):
    """
    * SizedBox(fixSize : QSize, widget : QWidget, **kwargs)
    * SizedBox(fixWidth : int, fixHeight : int, widget : QWidget, **kwargs)
    * SizedBox(fixSize : QSize, layout : QLayout, **kwargs)
    * SizedBox(fixWidth : int, fixHeight : int, layout : QLayout, **kwargs)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._initialize(*args)

    @singledispatchmethod
    def _initialize(self, *args): ...

    @_initialize.register
    def _(self, fixSize: QSize, widget: QWidget):
        self.setFixedSize(fixSize)
        self.setLayout(Row.singleWidgetBuild(widget))

    @_initialize.register
    def _(self, fixSize: QSize, layout: QLayout):
        self.setFixedSize(fixSize)
        self.setLayout(layout)

    @_initialize.register
    def _(self, fixWidth: int, fixHeight: int, widget: QWidget):
        self.setFixedSize(fixWidth, fixHeight)
        self.setLayout(Row.singleWidgetBuild(widget))

    @_initialize.register
    def _(self, fixWidth: int, fixHeight: int, layout: QLayout):
        self.setFixedSize(fixWidth, fixHeight)
        self.setLayout(layout)

class SimpleGrid(QGridLayout):
    def __init__(self,
                 row : int,
                 col : int,
                 widgets : Sequence[QWidget],
                 align: Qt.Alignment | Qt.AlignmentFlag = Qt.Alignment()
                 ):
        super().__init__()
        index : int
        for r in range(row):
            for c in range(col):
                index = r * col + c
                self.addWidget(widgets[index], r, c, align)
                index += 1

__all__ = ['Row', 'Column', 'SizedBox', 'SimpleGrid']

