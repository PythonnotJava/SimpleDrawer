from typing import Optional, Iterable

from PyQt5.QtWidgets import QGroupBox, QWidget
from PyQt5.QtCore import Qt

from .ABSW import AbstractWidget

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

__all__ = ['Group']