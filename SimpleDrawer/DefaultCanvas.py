import json
import sys
import random
from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtChart import *
from qt_material import apply_stylesheet, list_themes

from SideBar import SideBar
from OptimizeQt import *
from CanvasUI import *
from WalkerWebview import PygwalkerOpt
from MenuBar import MenuBar

# 主界面发布页
class HomePageView(QLabel):
    def __init__(self):
        super().__init__()

        self.setText("""
            <!DOCTYPE html> 
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Title</title>
            </head>
            <body>
                <div style="margin: 0 auto;font-weight: bold;padding-left: 20%;text-align: left;">
                    <h1>SimpleDrawer</h1>
                    <p>SimpleDrawer是一款简易画图为目标开发的软件，支持插件轻松拓展。</p>
                    <p>代码地址：<a href="https://github.com/PythonnotJava/SimpleDrawer">https://github.com/PythonnotJava/SimpleDrawer</a></p>
                </div>
            </body>
            </html>
        """)
        self.setOpenExternalLinks(True)
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignCenter)