
from typing import Optional

from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QRadioButton, QButtonGroup, QGridLayout, QVBoxLayout, \
    QHBoxLayout
from PySide6.QtCore import Signal
from .base import PageBase
proxies = {
    "http://": None,
    "https://": None,
}





class alreadyInstallPage(PageBase):
    """
    已安装的界面
    """
    on_last_page_button_clicked = Signal()
    on_next_button_clicked = Signal()
    on_exit_button_clicked = Signal()
    on_uninstall_start = Signal()
    on_install_finish = Signal()

    def __init__(self, parent: Optional[QWidget] = None, default_dir: str = "C:/Program Files/xghub") -> None:
        super().__init__(parent)

        # self.progress.setGeometry(240, 100, 120, 120)
        # pixmap = QPixmap("resource/left_bg.jpg")
        # self.setAutoFillBackground(True)
        # palette = self.palette()
        # palette.setBrush(self.backgroundRole(), pixmap)
        # self.setPalette(palette)
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        self.button_group = QButtonGroup()
        # 设置背景图片在左侧
        self.setStyleSheet("background-image: url(background.jpg); background-position: left;")
        self.label = QLabel("您的设备上已经安装了 svn提交信息插件 程序\n", self)
        self.label.setGeometry(170, 150, 350, 40)
        self.radio_button1 = QRadioButton('卸载')
        self.radio_button1.setChecked(True)  # 默认选中第一个选项
        self.radio_button2 = QRadioButton('修复')
        self.radio_button2.setGeometry(170, 105, 350, 40)
        layout.addStretch(1)
        layout.addWidget(self.radio_button1)
        layout.addWidget(self.radio_button2)
        layout.addStretch(3)
        layout1.addStretch(3)
        layout1.addLayout(layout)
        layout1.addStretch(4)

        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)

        # grid_layout.addWidget(self.radio_button1, 0, 0)  # 放置在第 1 行，第 1 列
        # grid_layout.addWidget(self.radio_button2, 1, 0)
        # self.setLayout(grid_layout)
        self.setLayout(layout1)
        self.label.setGeometry(170, 0, 350, 40)
        # self.label.setStyleSheet("background-color: white;")
        self.next_button = QPushButton(f'{"下一步"}', self)
        self.next_button.setGeometry(330, 324, 75, 25)
        self.next_button.clicked.connect(self.next)
        self.button_group.addButton(self.radio_button1)
        self.button_group.addButton(self.radio_button2)
        self.exit_button = QPushButton(f'{"退出"}', self)
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.setGeometry(410, 324, 75, 25)



    def next(self):
        if self.radio_button1.isChecked():
            self.on_uninstall_start.emit()
        else:
            self.on_next_button_clicked.emit()
    def last_page(self):
        self.on_last_page_button_clicked.emit()

    def exit(self):
        self.on_exit_button_clicked.emit()
