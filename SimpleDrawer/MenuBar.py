import sys
import random
from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtChart import *
from numpy.testing.print_coercion_tables import print_cancast_table
from qtawesome import icon as qt_icon
from qt_material import apply_stylesheet, list_themes

class MenuBar(QMenuBar):
    def __init__(self, p=None, s=None, dy : Callable = lambda : ..., **kwargs):
        super().__init__(**kwargs)

        self.settingmenu = QMenu('设置', self)
        self.pluginmenu = QMenu('插件', self)

        self.defaultMainTheme = None
        self.__setUI(p, s, dy)
    def __setUI(self, p, s, dy) -> None:
        toggleMainThemeAct = QAction("切换全局主题", self.settingmenu)
        toggleMainThemeMenu = QMenu()
        toggleMainThemeAct.setMenu(toggleMainThemeMenu)
        exitAskAct = QAction("退出提醒", self.settingmenu)
        if s['exit-ask']:
            exitAskAct.setIcon(qt_icon('fa.check'))
        exitAskAct.triggered.connect(lambda: self.__exitAskAct(s, exitAskAct))
        self.settingmenu.addActions([toggleMainThemeAct, exitAskAct])
        self.addMenu(self.pluginmenu)
        self.addMenu(self.settingmenu)
        for _, theme in enumerate(list_themes()):
            act = QAction(theme, toggleMainThemeMenu)
            act.triggered.connect(lambda _, t=theme: self.__toggleMainTheme(p, t))
            toggleMainThemeMenu.addAction(act)

        dynamicLoaderAct = QAction('动态载入', self.pluginmenu)
        dynamicLoaderAct.triggered.connect(dy)
        self.pluginmenu.addAction(dynamicLoaderAct)

    @staticmethod
    def __exitAskAct(s, exitAskAct : QAction):
        if not s['exit-ask']:
            exitAskAct.setIcon(qt_icon('fa.check'))
            s['exit-ask'] = True
        else:
            exitAskAct.setIcon(QIcon())
            s['exit-ask'] = False

    def __toggleMainTheme(self, parent, theme) -> None:
        apply_stylesheet(parent, theme=theme)
        self.defaultMainTheme = theme


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MenuBar()
    ui.show()
    sys.exit(app.exec_())