import json
import time
import winreg
import psutil
import requests
import zipfile
import os
import logging
from typing import Optional
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox, QProgressBar
from PySide6.QtCore import Signal, QThread

import config
from .base import PageBase
from widgets.progress import CircularProgress
from pathlib import Path
from utils import run_as_admin
from config import *

proxies = {
    "http://": None,
    "https://": None,
}





class startPage(PageBase):
    """
    选择安装路径的页面
    """
    on_last_page_button_clicked = Signal()
    on_next_button_clicked = Signal()
    on_exit_button_clicked = Signal()

    on_install_finish = Signal()

    def __init__(self, parent: Optional[QWidget] = None, default_dir: str = "C:/Program Files/xghub") -> None:
        super().__init__(parent)

        # self.progress.setGeometry(240, 100, 120, 120)
        # pixmap = QPixmap("resource/left_bg.jpg")
        # self.setAutoFillBackground(True)
        # palette = self.palette()
        # palette.setBrush(self.backgroundRole(), pixmap)
        # self.setPalette(palette)

        # 设置背景图片在左侧
        self.setStyleSheet("background-image: url(background.jpg); background-position: left;")
        self.label = QLabel("欢迎使用 svn提交信息插件 安装程序", self)
        self.font = QFont("SimSun", 12, QFont.Bold)
        self.label.setFont(self.font)
        self.label.setGeometry(170, 0, 350, 40)
        # self.label.setStyleSheet("background-color: white;")
        self.label1 = QLabel("此程序将引导你完成 svn提交信息插件 的安装。\n点击 [下一步] 继续", self)
        self.label1.setGeometry(170, 50, 350, 40)
        self.next_button = QPushButton(f'{"下一步"}', self)
        self.next_button.setGeometry(330, 324, 75, 25)
        self.next_button.clicked.connect(self.next)

        self.exit_button = QPushButton(f'{"退出"}', self)
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.setGeometry(410, 324, 75, 25)


    def next(self):
        self.on_next_button_clicked.emit()
    def last_page(self):
        self.on_last_page_button_clicked.emit()

    def exit(self):
        self.on_exit_button_clicked.emit()
