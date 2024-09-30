# 按钮类
from typing import Optional, Callable, Iterable, Union

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QAbstractButton, QPushButton, QToolButton
from PyQt5.QtGui import QColor, QIcon, QKeySequence, QPen, QPainter, QMouseEvent, QPaintEvent, QResizeEvent, QBrush

from .ABSW import AbstractWidget

class FlashButton(QAbstractButton, AbstractWidget):

    def __init__(self,
                 flashColor=QColor(120, 120, 120),
                 bgColor=QColor(200, 200, 200),
                 textModel : bool = True,
                 text : Optional[str] = None,
                 iconModel : bool = False,   # 有bug，图片不铺满问题
                 icon : Union[str, QIcon, None] = None,  # 为了支持qtawesome
                 iconFixed : bool = True,
                 cFunction : Callable = lambda : ...,   # click function,
                 shortcuts : Union[str, QKeySequence, None] = None,
                 **kwargs
                 ):

        super().__init__(**kwargs)

        self._textModel = textModel
        self._text = text
        self._iconModel = iconModel
        self._icon = icon
        self._iconFixed = iconFixed
        self._flashColor = flashColor
        self._bgColor = bgColor
        self._isPressed = False

        if shortcuts:
            self.setShortcut(shortcuts)

        self.clicked.connect(cFunction)

    def paintEvent(self, e : QPaintEvent):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), self._flashColor) if self._isPressed\
            else painter.fillRect(self.rect(), self._bgColor)

        if self._textModel:
            textRect = self.rect()
            painter.drawText(textRect, Qt.AlignCenter, self._text)

        if self._iconModel:
            iconRect = self.rect() if self._iconFixed else self.rect()
            icon = self._icon if isinstance(self._icon, QIcon) else QIcon(self._icon)
            icon.paint(painter, iconRect, Qt.AlignCenter)

    def mousePressEvent(self, e : QMouseEvent):
        self._isPressed = True
        self.clicked.emit()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent):
        self._isPressed = False
        super().mouseReleaseEvent(e)

    @classmethod
    def textBuild(cls,
                  text : str,
                  flashColor=QColor(120, 120, 120),
                  bgColor=QColor(200, 200, 200),
                  cFunction: Callable = lambda: ...,
                  shortcuts: Union[str, QKeySequence, None] = None,
                  **kwargs
                  ):
        return cls(
            flashColor=flashColor,
            textModel=True,
            bgColor=bgColor,
            cFunction=cFunction,
            text=text,
            shortcuts=shortcuts,
            **kwargs
        )

class OptPushButton(QPushButton, AbstractWidget):
    def __init__(self,
                 textModel : bool = True,
                 text : Optional[str] = None,
                 iconModel : bool = False,
                 iconFixed : bool = True,
                 icon : Union[str, QIcon, None] = None,
                 cFunction : Callable = lambda : ...,
                 shortcuts : Union[str, QKeySequence, None] = None,
                 enabled : bool = True,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setEnabled(enabled)
        self.clicked.connect(cFunction)
        if shortcuts:
            self.setShortcut(shortcuts)

        if textModel:
            self.setText(text)

        if iconModel:
            self.setIcon(icon if isinstance(icon, QIcon) else QIcon(icon))

            if iconFixed:
                self.setIconSize(self.size())

    @classmethod
    def iconBuild(cls,
                  icon: Union[str, QIcon],
                  iconFixed : bool = True,
                  cFunction : Callable = lambda : ...,
                  shortcuts: Union[str, QKeySequence, None] = None,
                  **kwargs
                  ):
        return cls(
            textModel=False,
            iconModel=True,
            icon=icon,
            cFunction=cFunction,
            iconFixed=iconFixed,
            shortcuts=shortcuts,
            **kwargs
        )

    @classmethod
    def textBuild(cls,
                  text : str,
                  cFunction : Callable = lambda : ...,
                  shortcuts: Union[str, QKeySequence, None] = None,
                  **kwargs
                  ):
        return cls(
            textModel=True,
            iconModel=False,
            text=text,
            cFunction=cFunction,
            shortcuts=shortcuts,
            **kwargs
        )

class OptToolButton(QToolButton, AbstractWidget):
    def __init__(self,
                 text : Optional[str] = None,
                 icon : QIcon | str = None,
                 buttonStyle : Qt.ToolButtonStyle = Qt.ToolButtonStyle.ToolButtonTextBesideIcon,
                 iconFixed : bool = False,
                 cFunction: Callable = lambda: ...,
                 shortcuts: Union[str, QKeySequence, None] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.clicked.connect(cFunction)
        self.setToolButtonStyle(buttonStyle)

        if text:
            self.setText(text)

        if icon:
            self.setIcon(icon)
            if iconFixed:
                self.setIconSize(self.size())

        if shortcuts:
            self.setShortcut(shortcuts)

class Switch(AbstractWidget):  # 支持右键开关

    clicked = pyqtSignal(bool)

    def __init__(self,
                 isOpen : bool = True,
                 height : int = 50,
                 openColor : Union[QColor, Qt.GlobalColor] = Qt.blue,
                 closeColor : Union[QColor, Qt.GlobalColor] = Qt.yellow,
                 circleColor : Union[QColor, Qt.GlobalColor] = Qt.cyan,
                 buttonBorderColor : Union[QColor, Qt.GlobalColor] = Qt.white,
                 circleBorderColor : Union[QColor, Qt.GlobalColor] = QColor('darkblue'),
                 onPress : Callable = lambda _: ...,
                 **kwargs  # 不接受关于高宽指定的参数
                 ):
        super().__init__(**kwargs)

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._openColor = openColor
        self._closeColor = closeColor
        self._circleColor = circleColor
        self._buttonBorderColor = buttonBorderColor
        self._circleBorderColor = circleBorderColor

        self.clicked.connect(onPress)
        self._proportion = 2.0

        self.H, self.W = height, int(height * self._proportion)
        self.setFixedSize(self.W, self.H)

        self.__isOpen = isOpen  # 右开左关

        self.clicked.emit(self.__isOpen)  # 重要！创建就需要根据当前状态触发一次

    def resizeEvent(self, e : QResizeEvent):
        new_height = self.height()
        self.setFixedSize(int(new_height * self._proportion), new_height)

    def mousePressEvent(self, e : QMouseEvent):
        super().mousePressEvent(e)
        self.__isOpen = not self.__isOpen
        self.clicked.emit(self.__isOpen)
        self.update()

    def paintEvent(self, e : QPaintEvent):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        radius = self.H // 2

        if self.__isOpen:
            painter.setPen(Qt.NoPen)
            brush = QBrush(self._openColor)
            painter.setBrush(brush)
            painter.drawRoundedRect(0, 0, self.W, self.H, radius, radius)

            painter.setPen(Qt.NoPen)
            brush.setColor(self._circleColor)
            painter.setBrush(brush)
            painter.drawRoundedRect(self.W - self.H, 0, self.H, self.H, radius, radius)
        else:
            painter.setPen(Qt.NoPen)
            brush = QBrush(self._closeColor)
            painter.setBrush(brush)
            painter.drawRoundedRect(0, 0, self.W, self.H, radius, radius)

            painter.setPen(Qt.NoPen)
            brush.setColor(self._circleColor)
            painter.setBrush(brush)
            painter.drawRoundedRect(0, 0, self.H, self.H, radius, radius)

        penWidth = 2

        pen = QPen(self._buttonBorderColor)
        pen.setWidth(penWidth)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(0, 0, self.W, self.H, radius, radius)

        pen.setColor(self._circleBorderColor)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        if self.__isOpen:
            circle_radius = self.H // 2 - penWidth
            circle_x = self.W - self.H + penWidth
            circle_y = penWidth

            painter.drawRoundedRect(
                circle_x, circle_y,
                self.H - penWidth * 2,
                self.H - penWidth * 2,
                circle_radius,
                circle_radius
            )
        else:
            circle_radius = self.H // 2 - penWidth
            circle_x = penWidth
            circle_y = penWidth
            painter.drawRoundedRect(
                circle_x, circle_y,
                self.H - penWidth * 2,
                self.H - penWidth * 2,
                circle_radius,
                circle_radius
            )

class TextButton(QPushButton, AbstractWidget):
    def __init__(self,
                 text : str,
                 paddings : Union[int, Iterable[int]] = 1,
                 cFunction: Callable = lambda: ...,
                 shortcuts: Union[str, QKeySequence, None] = None,
                 enabled : bool = True,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.setText(text)
        self.clicked.connect(cFunction)
        self.setEnabled(enabled)

        self.setStyleSheet(
            "padding :" + 'px '.join([str(x) for x in paddings]) + 'px' if isinstance(paddings, Iterable) else f'padding : {paddings}px'
        )

        if shortcuts:
            self.setShortcut(shortcuts)

__all__ = ['FlashButton', 'Switch', 'OptPushButton', 'OptToolButton', 'TextButton']

