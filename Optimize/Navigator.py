from typing import Sequence, Optional, Union, Callable

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtWidgets import QTabWidget, QWidget, QAbstractButton, QButtonGroup, QHBoxLayout, QVBoxLayout

from .ABSW import AbstractWidget
from .OptLabel import OptLabel
from .OptLayout import Row
from .QTyping import TabCfgType, WidgetOrLayoutType

class OptTabWidget(QTabWidget, AbstractWidget):
    def __init__(self,
                 tabs : Sequence[TabCfgType],
                 currentIndex : int = 0,
                 tabsShape: QTabWidget.TabShape = QTabWidget.TabShape.Rounded,
                 tabsPosition: QTabWidget.TabPosition = QTabWidget.TabPosition.North,
                 movable: bool = False,
                 currentIndexChangedFunction: Callable = lambda _: ...,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.setTabPosition(tabsPosition)
        self.setTabShape(tabsShape)
        self.setMovable(movable)
        self.setCurrentIndex(currentIndex)
        self.currentChanged.connect(currentIndexChangedFunction)

        # tab : TabCfgType
        for index, tab in enumerate(tabs):
            self.addTab(
                tab.widget,
                tab.icon if isinstance(tab.icon, QIcon) else QIcon(tab.icon),
                tab.label
            )
            if tab.toolTip:
                self.setTabToolTip(index, tab.toolTip)
class AppBar(AbstractWidget):
    def __init__(self,
                 leading : QWidget,
                 title : Optional[str] = None,
                 actions : Optional[Sequence[QWidget]] = None,
                 actionsAlign : Qt.Alignment = Qt.AlignRight,  # actions在appBar的布局
                 actionsWithinAlign : Qt.Alignment = Qt.AlignRight,  # actions之间的布局
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.leading = leading
        self.titleLabel = OptLabel(text=title, textModel=True)
        self.actions = actions

        self.selfLayoutConstructor(
            hbox=True,
            widgets_lays=[
                WidgetOrLayoutType(
                    dtype=1,
                    obj=leading,
                    align=Qt.AlignLeft
                ),
                WidgetOrLayoutType(
                    dtype=1,
                    obj=self.titleLabel,
                    align=Qt.AlignLeft
                ),
                WidgetOrLayoutType(
                    dtype=0,
                    obj=Row.widgetsBuild(
                        widgets=actions,
                        aligns=actionsWithinAlign,
                    ),
                    align=actionsAlign
                )
            ]
        )

    def setTitle(
            self,
            title : Optional[str] = None,
            **kwargs
    ):
        if title:
            self.titleLabel.setText(title)
        self.titleLabel.updateSelf(**kwargs)

# @bug 横/竖方向的按钮组
class ButtonGroupWidget(AbstractWidget):

    def __init__(self,
                 buttons : Sequence[QAbstractButton],
                 hbox : bool = True,
                 align: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment(),
                 stretch : int = 1,
                 useSpacing : bool = False,
                 spacing : int = 10,
                 margins : Union[QMargins, Sequence] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.ButtonManager = QButtonGroup(self)

        __box = QHBoxLayout(self) if hbox else QVBoxLayout(self)

        if useSpacing:
            for btn in buttons:
                __box.addWidget(btn, stretch=stretch, alignment=align)
                __box.addSpacing(spacing)
                self.ButtonManager.addButton(btn)
        else:
            for btn in buttons:
                __box.addWidget(btn, stretch=stretch, alignment=align)
                self.ButtonManager.addButton(btn)

        if margins:
            __box.setContentsMargins(margins if isinstance(margins, QMargins) else QMargins(*margins))
        self.setLayout(__box)

    # 均分布局模式
    @classmethod
    def uniformBuild(
            cls,
            buttons: Sequence[QAbstractButton],
            hbox: bool = True,
            stretch: int = 1,
            margins: Union[QMargins, Sequence] = None,
            **kwargs
    ):
        return cls(
            buttons=buttons,
            useSpacing=False,
            hbox=hbox,
            align=Qt.AlignmentFlag.AlignCenter,
            stretch=stretch,
            margins=margins,
            **kwargs
        )

    # 紧凑模式
    @classmethod
    def compactBuild(
            cls,
            buttons: Sequence[QAbstractButton],
            hbox: bool = True,
            stretch: int = 1,
            align: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.AlignCenter,
            margins: Union[QMargins, Sequence] = None,
            **kwargs
    ):
        return cls(
            buttons=buttons,
            hbox=hbox,
            stretch=stretch,
            useSpacing=True,
            spacing=0,
            align=align,
            margins=margins,
            **kwargs
        )

    # 自定义间距模式
    @classmethod
    def spacingBuild(
            cls,
            buttons: Sequence[QAbstractButton],
            hbox: bool = True,
            stretch: int = 1,
            align: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.AlignCenter,
            spacing : int = 10,
            margins: Union[QMargins, Sequence] = None,
            **kwargs
    ):
        return cls(
            buttons=buttons,
            hbox=hbox,
            stretch=stretch,
            align=align,
            useSpacing=True,
            spacing=spacing,
            margins=margins,
            **kwargs
        )

__all__ = ['AppBar', 'OptTabWidget', 'ButtonGroupWidget']