import sys
import random
from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtChart import *
from numpy.testing.print_coercion_tables import print_cancast_table
from qt_material import apply_stylesheet, list_themes

class MenuBar(QMenuBar):
    def __init__(self, p=None, **kwargs):
        super().__init__(**kwargs)

        self.settingmenu = QMenu('设置', self)
        self.pluginmenu = QMenu('插件', self)

        self.defaultMainTheme = None
        self.__setUI(p)
    def __setUI(self, p) -> None:
        toggleMainThemeAct = QAction("切换主题", self.settingmenu)
        toggleDrawThemeAct = QAction("切换图例主题", self.settingmenu)
        toggleMainThemeMenu = QMenu()
        toggleMainThemeAct.setMenu(toggleMainThemeMenu)
        self.settingmenu.addActions([toggleMainThemeAct, toggleDrawThemeAct])
        self.addMenu(self.pluginmenu)
        self.addMenu(self.settingmenu)
        for _, theme in enumerate(list_themes()):
            act = QAction(theme, toggleMainThemeMenu)
            print(theme)
            act.triggered.connect(lambda _, t=theme: self.__toggleMainTheme(p, t))
            toggleMainThemeMenu.addAction(act)

    def __toggleMainTheme(self, parent, theme) -> None:
        apply_stylesheet(parent, theme=theme)
        self.defaultMainTheme = theme

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MenuBar()
    ui.show()
    sys.exit(app.exec_())