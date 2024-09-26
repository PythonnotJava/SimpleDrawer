import sys
from typing import *

import pandas
import pygwalker
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from pygwalker import *

from Optimize.OptLabel import OptLabel
from Optimize.OptLayout import Column
from OptimizeQt import AbstractWidget
from CanvasUI import OperatorBar

class PygwalkerOpt(AbstractWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.operatorbar = OperatorBar()
        self.msgwidget = AbstractWidget()
        self.__setUI()

    def __setUI(self) -> None:
        self.operatorbar.openBtn.clicked.connect(self.linkOpenFunction)
        self.operatorbar.fileInput.setPlaceholderText('等待打开中')
        self.setLayout(
            Column.widgetsBuild(
                widgets=[
                    self.operatorbar,
                    self.msgwidget
                ]
            )
        )

    def linkOpenFunction(self) -> None:
        fileName, fileType = QFileDialog.getOpenFileName(
            self,
            "选择数据类表格文件",
            "C:/",
            "Excel(*.xlsx, *xls);Csv(*.csv)"
        )
        if fileName:
            fileType : str
            try:
                data : pandas.DataFrame
                if fileName.endswith('csv'):
                    data = pandas.read_csv(fileName)
                else:
                    data = pandas.read_excel(fileName)
                pygdata = pygwalker.walk(data)
                html = pygdata.to_html_without_iframe()
                with open('temp.html', 'w') as f:
                    f.write(html)
                    f.close()
                QDesktopServices.openUrl(QUrl('temp.html'))
                self.msgwidget.setUniqueWidget(
                    OptLabel.textBuild("成功打开站点")
                )
            except Exception as e:
                self.msgwidget.setUniqueWidget(
                    OptLabel.textBuild(str(e))
                )
            self.operatorbar.fileInput.setText(fileName)
        else:
            self.operatorbar.fileInput.setText('Lost FileName!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = PygwalkerOpt()
    ui.show()
    sys.exit(app.exec())