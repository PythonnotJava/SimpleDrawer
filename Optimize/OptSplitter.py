from typing import Iterable, Optional

from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import QSplitter, QWidget, QSplitterHandle
from PyQt5.QtCore import Qt

from .ABSW import AbstractWidget

class OptSplitter(QSplitter, AbstractWidget):
    def __init__(self,
                 widgets : Iterable[QWidget],
                 sizes: Optional[Iterable] = None,
                 collapsible: bool = True,
                 handleWidth: int = 10,
                 handleIndex: Optional[int] = None,
                 handleTips: Optional[str] = None,
                 handleCursor: Optional[str] = None,
                 horizontal: bool = False,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.setChildrenCollapsible(collapsible)
        self.setHandleWidth(handleWidth)
        self.setOrientation(Qt.Horizontal if horizontal else Qt.Vertical)

        if handleIndex is not None:
            handle: QSplitterHandle = self.handle(handleIndex)
            if handleTips: handle.setToolTip(handleTips)
            if handleCursor: handle.setCursor(QCursor(QPixmap(handleCursor)))

        for widget in widgets:
            self.addWidget(widget)

        if sizes:
            self.setSizes(sizes)

__all__ = ['OptSplitter']

