from collections import defaultdict
import numpy as np
import pyqtgraph as pg
from PIL import Image
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import (
    QColor,
    QPen,
    QLinearGradient,
    QBrush,
    QRadialGradient,
    QImage,
    QPixmap,
)
from PyQt6.QtWidgets import QApplication, QGraphicsItemGroup, QGraphicsRectItem

from tile import Tile


class MapView(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.painter = Painter(self)
        self.paint()
        # self.minimap = MiniMapView(self)  # 暂时不设minimap
        # self.bind_event()

    def init_ui(self):
        self.setMinimumSize(200, 200)
        self.setBackground(QColor(255, 255, 255))
        self.setAspectLocked(True)  # xy坐标轴始终1:1
        self.setXRange(0, 10)
        self.setYRange(0, 10)
        self.plotItem.vb.setLimits(xMin=0, xMax=16, yMin=0, yMax=16)

        self.addLegend()
        self.showGrid(True, True)
        self.getPlotItem().getViewBox().invertY(True)
        self.getPlotItem().showAxis("top")
        self.getPlotItem().showAxis("right")

    def paint(self):
        item = pg.ScatterPlotItem()  # 创建一个绘图项，用于绘制点
        self.addItem(item)

        # 创建圆形渐变
        gradient = QRadialGradient(0, 0, 0.7, -0.5, -0.5)
        gradient.setColorAt(0, QColor(255, 255, 63))  # 设置中心为淡黄色
        gradient.setColorAt(1, QColor(192, 192, 192))  # 设置边缘为灰色
        brush = QBrush(gradient)

        # 设置圆点的渐变填充
        item.setBrush(brush)

        # 创建数据点
        data = []
        for point in [(2, 3), (4, 6), (8, 4), (6, 2)]:
            data.append({"pos": point, "size": 10})

        # 设置数据点
        item.setData(data)

        # # test: show image
        # image_data = np.flipud(np.array(Image.open("static/icon/icon.png")))
        # image = pg.ImageItem(image_data.transpose([1, 0, 2]))
        # image.setRect(QRectF(-0.5, -0.5, 1, 1))  # (x, y, width, height)
        # self.addItem(image)
        
        # test
        for i in range(16):
            for j in range(16):
                self.painter.get_layer(0).add_tile("王城砖地", (i, j))

    def bind_event(self):
        self.plotItem.vb.sigStateChanged.connect(self.minimap.update_plot)
        self.sigRangeChanged.connect(self.minimap.update_overview_range)


class Painter:
    def __init__(self, map: MapView) -> None:
        self.map = map
        self.layers_name = [
            "sky",
            "land",
            "land_surface",
            "object",
            "weather",
            "cloud",
        ]  # 从底层到顶层

        self.init_painter()

    def init_painter(self):
        self.layers = {k: Layer(layer_num=i, map=self.map) for i, k in enumerate(self.layers_name)}
        
    def get_layer(self, num):
        return self.layers[self.layers_name[num]]


class Layer:
    tiles = {}  # Tile对象缓存

    def __init__(self, layer_num, map: MapView) -> None:
        self.layer_num = layer_num
        self.map = map
        self.blocks = {}

    def add_tile(self, tilename, position):
        """在当前图层添加一块地砖。

        Args:
            tilename (str): 地砖类别中文名
            position (tuple): 坐标
        """
        if tilename not in Layer.tiles.keys():
            Layer.tiles[tilename] = Tile(tilename)
        tile: Tile = Layer.tiles[tilename]
        image = self.blocks[position] = pg.ImageItem(image=np.array(tile.get_tile(15)).transpose([1, 0, 2]))
        image.setRect(QRectF(position[0], position[1], 1, 1))
        self.map.addItem(image)
        image.setZValue(self.layer_num)


class MiniMapView(pg.PlotWidget):
    def __init__(self, fathermap: MapView):
        super().__init__()
        self.father = fathermap
        self.init_ui()
        self.paint()

    def init_ui(self):
        self.setMinimumSize(100, 100)
        self.setBackground(QColor(255, 255, 255))
        self.setAspectLocked(True)  # xy坐标轴始终1:1

        x_limits, y_limits = [
            self.father.plotItem.vb.state["limits"][i] for i in ["xLimits", "yLimits"]
        ]
        self.setRange(xRange=x_limits, yRange=y_limits)
        self.plotItem.vb.setLimits(
            xMin=x_limits[0], xMax=x_limits[1], yMin=y_limits[0], yMax=y_limits[1]
        )

        self.addLegend()
        self.showGrid(True, True)
        self.getPlotItem().getViewBox().invertY(True)
        self.getPlotItem().hideAxis("bottom")
        self.getPlotItem().hideAxis("left")

    def paint(self):
        # 创建小地图中的范围框
        self.range_box = QGraphicsRectItem(0, 0, 1, 1)
        self.range_box.setPen(pg.mkPen("g"))  # 设置范围框的颜色为红色
        self.addItem(self.range_box)

    def update_plot(self):
        self.plotItem.clear()
        for item in self.father.plotItem.items:
            self.addItem(item)
        self.addItem(self.range_box)

    def update_overview_range(self):
        """更新小地图中的范围框位置和大小。"""
        current_range = self.father.viewRange()
        self.range_box.setRect(
            current_range[0][0],
            current_range[1][0],
            current_range[0][1] - current_range[0][0],
            current_range[1][1] - current_range[1][0],
        )
