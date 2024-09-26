from typing import Optional, Iterable, Any, Callable, Union

from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import QMenu, QAction, QWidget, QMenuBar

from .ABSW import AbstractWidget

# 菜单分割栏
class OptSeparator : pass

class OptMenuBar(QMenuBar, AbstractWidget):
    def __init__(self,
                 actions : Optional[Iterable[QAction]] = None,
                 menus : Optional[Iterable[QMenu]] = None,
                 actMnuSpt : Optional[Iterable[Any]] = None,  # QAction、OptSeparator、QMenu的混合
                 **kwargs
                 ):
        super().__init__(**kwargs)

        if actMnuSpt:
            for ams in actMnuSpt:
                if isinstance(ams, QMenu):
                    ams.setParent(self)
                    self.addMenu(ams)
                elif isinstance(ams, QAction):
                    ams.setParent(self)
                    self.addAction(ams)
                elif isinstance(ams, OptSeparator):
                    self.addSeparator()
                else:
                    pass

        if menus:
            for menu in menus:
                menu.setParent(self)
                self.addMenu(menu)

        if actions:
            for action in actions:
                action.setParent(self)
                self.addAction(action)

    # 仅仅actions
    @classmethod
    def actionsBuild(cls, actions : Iterable[QAction], **kwargs):
        return cls(actions=actions, actMnuSpt=None, menus=None, **kwargs)

    # 仅仅menus
    @classmethod
    def menusBuild(cls, menus : Iterable[QMenu], **kwargs):
        return cls(actions=None, actMnuSpt=None, menus=menus, **kwargs)

class OptMenu(QMenu, AbstractWidget):
    def __init__(self,
                 title : Optional[str] = None,
                 actions : Optional[Iterable[QAction]] = None,
                 menus : Optional[Iterable[QMenu]] = None,
                 actMnuSpt: Optional[Iterable[Any]] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.rebuild(title, actions, menus, actMnuSpt)

    def rebuild(self,
                title: Optional[str] = None,
                actions: Optional[Iterable[QAction]] = None,
                menus: Optional[Iterable[QMenu]] = None,
                actMnuSpt: Optional[Iterable[Any]] = None
                ) -> 'OptMenu':
        if title:
            self.setTitle(title)

        if actions:
            for action in actions:
                action.setParent(self)
                self.addAction(action)

        if menus:
            for menu in menus:
                menu.setParent(self)
                self.addMenu(menu)

        if actMnuSpt:
            for ams in actMnuSpt:
                if isinstance(ams, QMenu):
                    ams.setParent(self)
                    self.addMenu(ams)
                elif isinstance(ams, QAction):
                    ams.setParent(self)
                    self.addAction(ams)
                elif isinstance(ams, OptSeparator):
                    self.addSeparator()
                else:
                    pass
        return self

    # 仅仅actions
    @classmethod
    def actionsBuild(cls, actions: Iterable[QAction], **kwargs):
        return cls(actions=actions, actMnuSpt=None, menus=None, **kwargs)

    # 仅仅menus
    @classmethod
    def menusBuild(cls, menus: Iterable[QMenu], **kwargs):
        return cls(actions=None, actMnuSpt=None, menus=menus, **kwargs)


class OptAction(QAction):
    def __init__(self,
                 parent: Optional[QWidget] = None,
                 icon: QIcon | str = None,
                 text: Optional[str] = None,
                 cFunction: Callable = lambda: ...,
                 objectName: Optional[str] = None,
                 tips: Optional[str] = None,
                 shortcuts: Union[str, QKeySequence, None] = None,
                 enable: bool = True
                 ):
        super().__init__()
        self.triggered.connect(cFunction)
        self.setEnabled(enable)

        if parent:
            self.setParent(parent)

        if icon:
            self.setIcon(icon if isinstance(icon, QIcon) else QIcon(icon))

        if text:
            self.setText(text)

        if objectName:
            self.setObjectName(objectName)

        if tips:
            self.setToolTip(tips)

        if shortcuts:
            self.setShortcut(shortcuts)

__all__ = ['OptAction', 'OptMenu', "OptSeparator", "OptMenuBar"]

