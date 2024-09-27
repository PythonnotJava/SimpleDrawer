from PyQt5.QtWidgets import QSystemTrayIcon, QWidget, QApplication, QAction ,QMenu

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
