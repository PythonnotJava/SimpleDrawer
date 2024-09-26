from typing import Optional, Union

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QPaintEvent, QResizeEvent

from .ABSW import AbstractWidget

class OptLabel(QLabel, AbstractWidget):

    imgPath : Optional[str] = None

    def __init__(self,
                 textModel : bool = False,
                 text : Optional[str] = None,
                 textWrap : bool = False,
                 textFormat : Optional[Qt.TextFormat] = None,
                 imgModel : bool = False,
                 imgPath : Optional[str] = None,
                 imgFixed : bool = False,
                 linkable : bool = True,
                 textAlign : Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment(),
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.setAlignment(textAlign)

        if textModel:
            self.setText(text)
            self.setWordWrap(textWrap)
            self.setOpenExternalLinks(linkable)
            if textFormat:
                self.setTextFormat(textFormat)

        if imgModel:
            self.setPixmap(QPixmap(imgPath).scaled(self.size()) if imgFixed else QPixmap(imgPath))
            self.imgPath = imgPath

        self.imgFixed = imgFixed

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)
        if self.imgFixed and self.imgPath:
            self.setPixmap(QPixmap(self.imgPath).scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    # 构建图版本的label
    @classmethod
    def imgBuild(
            cls,
            imgPath : str,
            imgFixed : bool = False,
            textAlign : Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment(),
            **kwargs
    ):
        return cls(imgModel=True, imgPath=imgPath, imgFixed=imgFixed, textAlign=textAlign, **kwargs)

    # 构建文字版本的label
    @classmethod
    def textBuild(cls,
                  text: str,
                  textWrap: bool = False,
                  textFormat: Optional[Qt.TextFormat] = None,
                  linkable: bool = True,
                  textAlign: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment(),
                  **kwargs
                  ):
        return cls(
            textModel=True,
            text=text,
            textWrap=textWrap,
            textFormat=textFormat,
            linkable=linkable,
            textAlign=textAlign,
            **kwargs
        )

class CircleAvatar(AbstractWidget):
    def __init__(self,
                 imgPath: str,
                 diameter: int,  # 直径
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._diameter = diameter
        self.img = QPixmap(imgPath).scaled(diameter, diameter)
        self.setFixedSize(diameter, diameter)

    def paintEvent(self, e: QPaintEvent) -> None:
        super().paintEvent(e)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, self._diameter, self._diameter)

        painter.setBrush(Qt.transparent)
        painter.drawPath(path)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self.img)

    def setAvatar(self, imgPath : Union[QPixmap, str]):
        self.img = imgPath if isinstance(imgPath, QPixmap) else QPixmap(imgPath)
        self.update()

__all__ = ['OptLabel', 'CircleAvatar']

