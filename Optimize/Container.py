from typing import Callable, Optional, Sequence, Union, Iterable

from PyQt5.QtWidgets import QStackedWidget, QWidget, QGroupBox, QScrollArea
from PyQt5.QtCore import Qt

from .ABSW import AbstractWidget

class Stack(QStackedWidget, AbstractWidget):
    def __init__(self,
                 widgets : Sequence[QWidget],
                 currentIndex : int = 0,
                 currentIndexChangedFunction: Callable = lambda _: ...,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setCurrentIndex(currentIndex)
        for widget in widgets:
            self.addWidget(widget)
        self.currentChanged.connect(currentIndexChangedFunction)

class Group(QGroupBox, AbstractWidget):
    def __init__(self,
                 title : str = '',
                 useFlat : bool = True,
                 uniqueWidget: Optional[QWidget] = None,
                 uniqueWidgetMargins : Optional[Iterable] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.setTitle(title)
        self.setFlat(useFlat)

        if uniqueWidget:
            self.setUniqueWidget(uniqueWidget, align=Qt.AlignCenter, margins=uniqueWidgetMargins)

class ScrollArea(QScrollArea, AbstractWidget):
    def __init__(self,
                 coreWidget : Optional[QWidget] = None,
                 align : Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment(),
                 resizabled : bool = True,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setAlignment(align)
        self.setWidgetResizable(resizabled)

        if coreWidget:
            self.setWidget(coreWidget)


__all__ = ['Stack', 'Group', 'ScrollArea']