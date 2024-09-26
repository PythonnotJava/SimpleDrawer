# 交互输入

from typing import Optional, Union, Iterable

from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtGui import QPaintEvent, QPainter, QPen, QColor
from PyQt5.QtWidgets import QLineEdit, QCompleter, QPushButton, QTextEdit
from qtawesome import icon as qtIcon

from .ABSW import AbstractWidget
from .OptLayout import Row

class OptLineEdit(QLineEdit, AbstractWidget):
    def __init__(self,
                 enable: bool = True,
                 text: Optional[str] = None,
                 maxLen: Optional[int] = None,
                 placeholderText: Optional[str] = None,
                 completer : Optional[QCompleter] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.setEnabled(enable)

        if placeholderText is not None:
            self.setPlaceholderText(placeholderText)

        if text is not None:
            self.setText(text)

        if maxLen is not None:
            self.setMaxLength(maxLen)

        if completer:
            self.setCompleter(completer)

    @classmethod
    def autoComplete(cls,
                     models : Iterable[str],
                     enable: bool = True,
                     text: Optional[str] = None,
                     maxLen: Optional[int] = None,
                     placeholderText: Optional[str] = None,
                     visibleItems : int = 5,
                     caseSensitivity : Qt.CaseSensitivity = Qt.CaseInsensitive,
                     filterMode : Union[Qt.MatchFlags, Qt.MatchFlag] = Qt.MatchContains,
                     completionMode : int = QCompleter.PopupCompletion,
                     **kwargs
                     ):
        model = QStringListModel()
        model.setStringList(models)
        completer = QCompleter()
        completer.setModel(model)
        # completer = QCompleter(QStringListModel(models))不知道为什么不能这样
        completer.setMaxVisibleItems(visibleItems)
        completer.setCaseSensitivity(caseSensitivity)
        completer.setFilterMode(filterMode)
        completer.setCompletionMode(completionMode)
        return cls(
            enable=enable,
            text=text,
            maxLen=maxLen,
            placeholderText=placeholderText,
            completer=completer,
            **kwargs
        )

class PwdEdit(AbstractWidget):
    def __init__(self,
                 maxLen : int = 20,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.lineEdit = QLineEdit()
        self.viewBtn = QPushButton()

        self.maxLen = maxLen
        self.__isHide = True

        self.__config()

    def __config(self):
        self.lineEdit.setMaxLength(self.maxLen)
        self.viewBtn.setIcon(qtIcon('ei.eye-close', color='darkblue'))
        self.lineEdit.setEchoMode(QLineEdit.Password)

        def __func():
            if self.__isHide:
                self.lineEdit.setEchoMode(QLineEdit.Normal)
                self.viewBtn.setIcon(qtIcon('ei.eye-open', color='darkblue'))
            else:
                self.lineEdit.setEchoMode(QLineEdit.Password)
                self.viewBtn.setIcon(qtIcon('ei.eye-close', color='darkblue'))
            self.__isHide = not self.__isHide

        self.viewBtn.clicked.connect(__func)
        self.setLayout(
            Row.widgetsBuild(
                widgets=[self.lineEdit, self.viewBtn],
                aligns=Qt.Alignment(),
                stretch=0
            )
        )

        self.lineEdit.setStyleSheet("border: 0; border-bottom: 1px solid black;")
        self.viewBtn.setStyleSheet('border: 0;')

    def paintEvent(self, e : QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.NoBrush)

        rect = self.rect().adjusted(1, 1, -1, -1)
        rect.setHeight(rect.height() - 3)
        painter.drawRoundedRect(rect, 5, 5)

class OptTextEdit(QTextEdit, AbstractWidget):
    def __init__(self,
                 text : Optional[str] = None,
                 textColor : Union[QColor, Qt.GlobalColor] = Qt.black,
                 enabled : bool = True,
                 align : Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment(),
                 placeholderText: Optional[str] = None,
                 acceptRichText : Optional[bool] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.setTextColor(textColor)
        self.setEnabled(enabled)
        self.setAlignment(align)

        if acceptRichText:
            self.setAcceptRichText(acceptRichText)

        if placeholderText:
            self.setPlaceholderText(placeholderText)

        if text:
            self.setText(text)

class UnderlineEdit(OptLineEdit):
    """
    UnderlineEdit(self, underlineColor : QColor = QColor('#ffffff'), underlineHeight : int = 1, enable: bool = True, text: Optional[str] = None, maxLen: Optional[int] = None, placeholderText: Optional[str] = None, completer : Optional[QCompleter] = None, **kwargs)
    """
    def __init__(self, underlineColor : QColor = QColor('#ffffff'), underlineHeight : int = 1, **kwargs):
        super().__init__(**kwargs)
        self.underlineColor = underlineColor
        self.underlineHeight = underlineHeight
        self.setStyleSheet(f"border: 0; border-bottom: {underlineHeight}px solid {underlineColor.name()};")

    @classmethod
    def autoComplete(cls,
                     models : Iterable[str],
                     underlineColor : Union[QColor, Qt.GlobalColor] = Qt.black,
                     underlineHeight : int = 1,
                     enable: bool = True,
                     text: Optional[str] = None,
                     maxLen: Optional[int] = None,
                     placeholderText: Optional[str] = None,
                     visibleItems : int = 5,
                     caseSensitivity : Qt.CaseSensitivity = Qt.CaseInsensitive,
                     filterMode : Union[Qt.MatchFlags, Qt.MatchFlag] = Qt.MatchContains,
                     completionMode : int = QCompleter.PopupCompletion,
                     **kwargs
                     ):
        instance = super(UnderlineEdit, cls).autoComplete(
            models=models,
            enable=enable,
            text=text,
            maxLen=maxLen,
            placeholderText=placeholderText,
            visibleItems=visibleItems,
            caseSensitivity=caseSensitivity,
            filterMode=filterMode,
            completionMode=completionMode,
            **kwargs
        )
        instance.underlineColor = underlineColor
        instance.underlineHeight = underlineHeight
        instance.setStyleSheet(f"border: 0; border-bottom: {underlineHeight}px solid {underlineColor.name()};")
        return instance

__all__ = ['OptLineEdit', 'OptTextEdit', 'PwdEdit', 'UnderlineEdit']

