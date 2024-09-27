import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QPainter

class PieChartExample(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建主窗口
        self.setWindowTitle("饼状图示例")
        self.setGeometry(100, 100, 600, 400)

        # 创建饼状图系列
        series = QPieSeries()
        series.append("类别A", 40)
        series.append("类别B", 30)
        series.append("类别C", 30)

        # 设置切片标签显示为占比
        for slice in series.slices():
            slice.setLabelVisible(True)
            slice.setLabel(f"{slice.percentage() * 100:.1f}%")  # 显示占比

        # 创建图表并添加系列
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("饼状图示例")

        # 设置图例位置
        chart.legend().setAlignment(Qt.AlignRight)

        # 创建图表视图
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(chart_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PieChartExample()
    window.show()
    sys.exit(app.exec_())
