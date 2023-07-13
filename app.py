import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
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
from mapview import MapView


class MainWindow(QMainWindow):
    icon_path = "static/icon/"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FO/FFO Map Editor Alpha By: 猫崎板子")
        self.setGeometry(0, 0, 1280, 800)
        self.setWindowIcon(QIcon(self._to_icon_path("icon.png")))
        self.center_window()

        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()
        self.create_central_widget()

    def _to_icon_path(self, filename):
        """转换路径为图标路径。

        Args:
            filename (str): 图标名

        Returns:
            str: 图标路径
        """
        return MainWindow.icon_path + filename

    def center_window(self):
        """创建主界面。"""
        frame_geometry = self.frameGeometry()
        center_point = QApplication.primaryScreen().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def create_menu(self):
        """创建菜单栏。"""
        menu_bar = self.menuBar()

        # region File menu
        file_menu = menu_bar.addMenu("File")

        # file - new/open
        self.action_new = QAction(
            QIcon(self._to_icon_path("new.png")), "New Model", self
        )
        self.action_new.setShortcut("Ctrl+N")
        self.action_open = QAction(
            QIcon(self._to_icon_path("open.png")), "Open Model", self
        )
        action_recent = QAction("Recent Model 1", self)
        action_recent = QAction("Recent Model 2", self)

        # file - save/save as
        self.action_save = QAction(QIcon(self._to_icon_path("save.png")), "Save", self)
        self.action_save.setShortcut("Ctrl+S")
        action_save_as = QAction(
            QIcon(self._to_icon_path("save_as.png")), "Save As", self
        )
        action_save_as.setShortcut("Ctrl+Shift+S")

        # file - options
        action_options = QAction(
            QIcon(self._to_icon_path("options.png")), "Options", self
        )

        # file - exit
        action_exit = QAction("Exit", self)
        action_exit.setShortcut("Ctrl+Q")
        action_exit.triggered.connect(app.quit)

        # file - end
        file_menu.addAction(self.action_new)
        file_menu.addAction(self.action_open)
        recent_menu = file_menu.addMenu("Recent Model")
        recent_menu.addAction(action_recent)
        recent_menu.addAction(action_recent)
        file_menu.addSeparator()
        file_menu.addAction(self.action_save)
        file_menu.addAction(action_save_as)
        file_menu.addSeparator()
        file_menu.addAction(action_options)
        file_menu.addSeparator()
        file_menu.addAction(action_exit)
        
        # endregion File menu

        # region Edit menu
        edit_menu = menu_bar.addMenu("Edit")

        action_undo = QAction(QIcon(self._to_icon_path("undo.png")), "Undo", self)
        action_undo.setShortcut("Ctrl+Z")
        action_redo = QAction(QIcon(self._to_icon_path("redo.png")), "Redo", self)
        action_redo.setShortcut("Ctrl+Y")
        edit_menu.addAction(action_undo)
        edit_menu.addAction(action_redo)
        # endregion Edit menu

        # region View menu
        view_menu = menu_bar.addMenu("View")

        action_default_layout = QAction("Use Default Layout", self)
        view_menu.addAction(action_default_layout)
        # endregion

        # region Run menu
        run_menu = menu_bar.addMenu("Run")

        # run - stop/run/pause/fast_forward
        self.action_reset = QAction(
            QIcon(self._to_icon_path("reset.png")), "Reset", self
        )
        self.action_run = QAction(QIcon(self._to_icon_path("run.png")), "Run", self)
        self.action_run.setShortcut("F5")
        self.action_pause = QAction(
            QIcon(self._to_icon_path("pause.png")), "Pause", self
        )
        self.action_fast_forward = QAction(
            QIcon(self._to_icon_path("fast-forward.png")), "Fast Forward", self
        )
        run_menu.addAction(self.action_reset)
        run_menu.addAction(self.action_run)
        run_menu.addAction(self.action_pause)
        run_menu.addAction(self.action_fast_forward)
        # endregion

        # region Help menu
        help_menu = menu_bar.addMenu("Help")

        copyright_action = QAction("Copyright Info", self)
        about_action = QAction("About", self)

        help_menu.addAction(copyright_action)
        help_menu.addAction(about_action)
        # endregion

    def create_toolbar(self):
        """创建界面顶部工具栏。"""
        toolbar = QToolBar("Top Toolbar")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)

        toolbar.addAction(self.action_new)
        toolbar.addAction(self.action_open)
        toolbar.addAction(self.action_save)

        toolbar.addSeparator()

        toolbar.addAction(self.action_reset)
        toolbar.addAction(self.action_run)
        toolbar.addAction(self.action_pause)
        toolbar.addAction(self.action_fast_forward)

        toolbar.addSeparator()

        speed_slider = QSlider(Qt.Orientation.Horizontal)
        speed_slider.setFixedWidth(200)
        speed_slider.setRange(1, 20)
        speed_slider.setValue(4)
        speed_slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        speed_slider.setTickInterval(1)
        speed_label = QLabel("  4x")
        speed_slider.valueChanged.connect(
            lambda value: speed_label.setText(f"  {value}x")
        )

        toolbar.addWidget(QLabel("  Run Speed:  "))
        toolbar.addWidget(speed_slider)
        toolbar.addWidget(speed_label)

    def create_statusbar(self):
        status_bar = self.statusBar()
        status_bar.showMessage("Ready")

    def create_central_widget(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        vbox = QVBoxLayout(central_widget)
        vbox.setContentsMargins(10, 10, 10, 10)

        splitter = QSplitter()
        mapview = MapView()

        # 左侧部件
        left_widget = QWidget(splitter)
        left_widget.setStyleSheet("background-color: #f0f0f0;")
        left_vbox = QHBoxLayout(left_widget)
        left_vbox.setContentsMargins(5, 5, 5, 5)
        # left_vbox.addWidget(mapview.minimap)
        left_vbox.addWidget(None)

        # 中心部件
        splitter.addWidget(mapview)

        # 右侧部件
        right_widget = QWidget(splitter)
        right_widget.setStyleSheet("background-color: #f0f0f0;")

        splitter.setSizes([160, 480, 160])

        vbox.addWidget(splitter)

        self.setLayout(vbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
