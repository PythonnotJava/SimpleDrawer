# 对话框

from typing import Callable

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QWhatsThis, QDialog, QPushButton, QLineEdit, QLabel

from .OptLayout import Row, Column
from .ABSW import AbstractWidget
from .QTyping import WidgetOrLayoutType
from .OptLabel import OptLabel
from .OptButton import OptPushButton

class OptDlg(QDialog, AbstractWidget):

    def __init__(self,
                 hideWhatThisButton: bool = True,
                 whatThisButtonFunction : Callable = lambda : ...,
                 **kwargs):
        super().__init__(**kwargs)

        self.setModal(True)

        if hideWhatThisButton:
            self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

        self.whatThisButtonFunction = whatThisButtonFunction

    def event(self, e: QEvent):
        if e.type() == QEvent.Type.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            self.whatThisButtonFunction()
        return super().event(e)

class InputDialog(OptDlg):
    """
    InputDialog(
        hideWhatThisButton: bool = True,
        whatThisButtonFunction : Callable = lambda : ...,
        infoText : str = 'Content',
        confirmText : str = 'Yes',
        cancelText : str = 'No',
        confirmFunction : Callable = lambda : ...,
        cancelFunction : Callable = lambda : ...,
        **kwargs
    )
    """
    def __init__(self,
                 infoText : str = 'Content',
                 confirmText : str = 'Yes',
                 cancelText : str = 'No',
                 confirmFunction : Callable = lambda : ...,
                 cancelFunction : Callable = lambda : ...,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.lineEdit = QLineEdit()
        self.label = QLabel(infoText)
        self.confirmBtn = QPushButton(confirmText)
        self.cancelBtn = QPushButton(cancelText)
        self.confirmBtn.clicked.connect(confirmFunction)
        self.cancelBtn.clicked.connect(cancelFunction)

        self.setLayout(
            Column.laysBuild(
                lays=[
                    Row.widgetsBuild(widgets=[self.label, self.lineEdit], aligns=Qt.AlignCenter),
                    Row.widgetsBuild(widgets=[self.confirmBtn, self.cancelBtn], aligns=Qt.AlignCenter)
                ]
            )
        )

    def text(self) -> str: return self.lineEdit.text()

class SingleButttonBox(OptDlg):
    def __init__(self,
                 message : str,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.selfLayoutConstructor(
            hbox=False,
            widgets_lays=[
                WidgetOrLayoutType(
                    dtype=0,
                    obj=Column.widgetsBuild(
                        widgets=[
                            OptLabel.textBuild(text=message, textWrap=True),
                            OptPushButton.textBuild(text='Ok', cFunction=self.close, maxw=150)
                        ],
                        aligns=Qt.AlignCenter
                    )
                )
            ]
        )

__all__ = ['InputDialog', 'OptDlg', 'SingleButttonBox']

