import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize, Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("这是一个写满文字的主页！", self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 初始窗口大小
        self.resize(800, 600)

    def resizeEvent(self, event):
        # 获取窗口的宽度和高度
        width = self.width()
        height = self.height()

        # 计算字体大小
        font_size = min(width, height) // 20  # 你可以调整这个比例
        self.label.setStyleSheet(f"font-size: {font_size}px;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
