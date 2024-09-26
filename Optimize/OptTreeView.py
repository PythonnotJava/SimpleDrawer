# 复杂的树控件——实现多级目录关系

from typing import Optional, Callable

from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtCore import Qt

from .ABSW import AbstractWidget

# 带有额外内容存储功能的项
class StandardItemWithContent(QStandardItem):
    def __init__(self, *args):
        super().__init__(*args)

        self.memoryContent = None

# 专门生成目录的TreeView
class ContentTreeView(QTreeView, AbstractWidget):
    def __init__(self,
                 defaultItems : Optional[dict] = None,
                 headerTitle: str = 'Content',
                 hideHeader: bool = False,  # 隐藏表头标题的条件下，HeaderTitle不生效
                 editableItems: bool = True,  # 是否可以编辑项
                 onClickedLowItems : Callable = lambda standardItemWithContent : ...,
                 onClickedOtherItems: Callable = lambda standardItemWithContent : ...,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.__editableItems = editableItems
        self.__onClickedOtherItems = onClickedOtherItems
        self.__onClickedLowItems = onClickedLowItems

        self.uniqueModel = QStandardItemModel()
        self.setModel(self.uniqueModel)
        self.clicked.connect(self.on_item_clicked)  # 连接点击信号到槽函数

        if hideHeader:
            self.setHeaderHidden(True)
        else:
            _item = QStandardItem(headerTitle)
            self.uniqueModel.setHorizontalHeaderItem(0, _item)
            _item.setTextAlignment(Qt.AlignCenter)

        if defaultItems:
            self.addItems(defaultItems)

    def _addItems(self, parent_item: QStandardItem, items: dict) -> None:
        for key, value in items.items():
            item = StandardItemWithContent(key)
            item.setEditable(self.__editableItems)
            if isinstance(value, dict):
                self._addItems(item, value)
            else:
                item.memoryContent = value
            parent_item.appendRow(item)

    def addItems(self, items: dict) -> None:
        self._addItems(self.uniqueModel.invisibleRootItem(), items)

    def on_item_clicked(self, index):
        item : StandardItemWithContent = index.model().itemFromIndex(index)
        self.__onClickedLowItems(item) if not item.hasChildren() else self.__onClickedOtherItems(item)

__all__ = ['ContentTreeView', 'StandardItemWithContent']

