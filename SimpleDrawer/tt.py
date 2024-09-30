import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Button Check Example')

        layout = QVBoxLayout()

        self.label = QLabel('按钮未被按下', self)
        layout.addWidget(self.label)

        self.button = QPushButton('按下我', self)
        self.button.setCheckable(True)  # 设置为可切换状态
        layout.addWidget(self.button)

        # 连接按钮的点击信号到槽函数
        self.button.clicked.connect(self.on_button_click)

        self.setLayout(layout)

    def on_button_click(self):
        # 使用 setChecked 方法
        if self.button.isChecked():
            self.label.setText('按钮已被按下')
        else:
            self.label.setText('按钮未被按下')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
