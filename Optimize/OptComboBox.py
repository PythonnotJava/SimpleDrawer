# 下拉框

from typing import Callable, Optional, Sequence, Iterable, Union

from PyQt5.QtGui import QIcon, QFontDatabase
from PyQt5.QtCore import QAbstractItemModel, Qt
from PyQt5.QtWidgets import QCompleter, QComboBox, QToolButton, QMenu

from .ABSW import AbstractWidget
from .QTyping import IconWithStringType


class OptComboBox(QComboBox, AbstractWidget):
    def __init__(self,
                 icon_strings: Optional[Sequence[IconWithStringType]] = None,
                 strItems: Optional[Iterable[str]] = None,  # icon_strings与strItems模式二选一
                 currentIndex: int = 0,
                 model: Optional[QAbstractItemModel] = None,
                 editable: bool = True,
                 enabled: bool = True,
                 completer: Optional[QCompleter] = None,
                 currentIndexChangedFunction: Callable = lambda _: ...,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setEnabled(enabled)
        self.setEditable(editable)
        self.setCurrentIndex(currentIndex)
        self.currentIndexChanged.connect(currentIndexChangedFunction)

        if icon_strings:
            for iws in icon_strings:
                if isinstance(iws.icon, QIcon):
                    self.addItem(iws.icon, iws.name)
                else:
                    self.addItem(QIcon(iws.icon), iws.name)

        if strItems:
            self.addItems(strItems)

        if model:
            self.setModel(model)

        if completer:
            self.setCompleter(completer)


# @ bug
class DropButtonComboBox(QToolButton, AbstractWidget):
    def __init__(self,
                 menu: QMenu,
                 icon: Union[str, QIcon, None] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.__menu = menu

        self.setIcon(QIcon(icon) if isinstance(icon, str) else icon)
        self.__isUp = True

        self.__config()

    def __config(self):
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setMenu(self.__menu)

        font_id = QFontDatabase.addApplicationFont('Optimize/source/font/fontawesome-webfont.ttf')
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.setStyleSheet(f"font-family: {font_family}; font-size: 16px;")
        self.setText("\uf078")

        self.clicked.connect(self.__whenClicked)

    def __whenClicked(self):
        if self.__isUp:
            self.setText("\uf077")
            self.__menu.exec(self.mapToGlobal(self.rect().bottomLeft()))
        else:
            self.setText("\uf078")
        self.__isUp = not self.__isUp


__all__ = ['OptComboBox', 'DropButtonComboBox']
