import sys
import importlib
import importlib.util
from PyQt5.QtWidgets import *


# 非控件
class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, p : QWidget):
        super().__init__(icon, p)

        show_action = QAction("Show", p)
        quit_action = QAction("Exit", p)
        show_action.triggered.connect(p.show)
        quit_action.triggered.connect(QApplication.instance().quit)

        tray_menu = QMenu()

        tray_menu.addActions([show_action, quit_action])
        self.setContextMenu(tray_menu)
        self.activated.connect(p.show)

# 动态插入插件
class DWidgetLoader:
    def __call__(self, p):
        fileName, _ = QFileDialog.getOpenFileName(
            p,
            '选择插件',
            'C:/',
            "Python File(*.py)"
        )
        if fileName:
            try:
                spec = importlib.util.spec_from_file_location("DynamicModule", fileName)
                module = importlib.util.module_from_spec(spec)
                sys.modules["DynamicModule"] = module
                spec.loader.exec_module(module)
                DWidget = getattr(module, "DWidget")
                instance = DWidget()
                p.register(
                    instance,
                    instance.name,
                    instance.icon
                )
            except Exception as e:
                QMessageBox.information(
                    p,
                    '载入失败',
                    e.__str__(),
                )


