# Python's edition must be no less than 3.12!

# Basic Types & some constants
from Optimize.QTyping import (
    WidgetOrLayoutType,
    IconWithStringType,
    TabCfgType,
    ButtonStateQssSimpleGenerator,
    ColorTypeWithPen,
    ColorType,
    ColorTypeWithBrush
)
from Optimize.QConst import QColorSkyblue, QColorLightskyblue, QColorTan

# Optimized Widgets
from Optimize.ABSW import AbstractWidget, OptApplication
from Optimize.OptLabel import OptLabel, CircleAvatar
from Optimize.OptLayout import SimpleGrid, SizedBox, Row, Column
from Optimize.OptButton import Switch, OptToolButton, OptPushButton, FlashButton, TextButton
from Optimize.OptDlg import OptDlg, InputDialog
from Optimize.OptSlider import OptSlider
from Optimize.OptInput import OptTextEdit, OptLineEdit, PwdEdit, UnderlineEdit
from Optimize.OptComboBox import OptComboBox, DropButtonComboBox
from Optimize.OptSplitter import OptSplitter
from Optimize.PartingLine import PartingLine
from Optimize.Navigator import OptTabWidget, AppBar, ButtonGroupWidget
from Optimize.Container import Stack, Group, ScrollArea
from Optimize.OptMenuSeries import OptSeparator, OptMenuBar, OptMenu, OptAction

# ThirdParties
from Optimize.OptMatplotlib import MatplotlibQtFigure