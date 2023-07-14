import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QLabel,
    QToolBar,
    QWidgetAction,
    QSlider,
)

# 创建应用程序
app = QApplication([])
win = QMainWindow()

# 创建GraphicsLayoutWidget，用于管理多个图层
layout = pg.GraphicsLayoutWidget()
win.setCentralWidget(layout)

# 创建示例图像数据
image_data1 = np.random.rand(100, 100)
image_data2 = np.random.rand(100, 100)
image_data3 = np.random.rand(100, 100)

# 创建第一个图层
layer1 = layout.addPlot()
layer1.setTitle("Layer 1")

# 添加图像项1到第一个图层
image_item1 = pg.ImageItem(image=image_data1)
layer1.addItem(image_item1)

# 创建第二个图层
layer2 = layout.addPlot()
layer2.setTitle("Layer 2")

# 添加图像项2到第二个图层
image_item2 = pg.ImageItem(image=image_data2)
layer2.addItem(image_item2)

# 创建第三个图层
layer3 = layout.addPlot()
layer3.setTitle("Layer 3")

# 添加图像项3到第三个图层
image_item3 = pg.ImageItem(image=image_data3)
layer3.addItem(image_item3)

# 设置图层之间的间距
# layout.setSpacing(30)

# 启动应用程序的事件循环
win.show()
app.exec()