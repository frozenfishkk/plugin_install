import os
from typing import Optional
from PySide6 import QtCore
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QPushButton,  QMessageBox, QCheckBox
from PySide6.QtCore import Signal, QThread
from .base import PageBase
from widgets.progress import CircularProgress
from pathlib import Path
from utils import run_as_admin
import subprocess

class FinishPage(PageBase):
    on_exit_button_clicked = Signal()
    install_dir: Path
    
    def __init__(self, parent: Optional[QWidget] = None, default_dir:str = "C:/Program Files/xghub") -> None:
        super().__init__(parent)
        self.font = QFont("SimSun", 16,QFont.Bold)
        self.label = QLabel("安装完成", self)
        self.label.setFont(self.font)
        self.label.setGeometry(300, 10, 100,50)
        self.exit_button = QPushButton(f'{"退出"}', self)
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.setGeometry(300, 324, 75, 25)


    def set_install_dir(self, install_dir:str):
        self.install_dir = Path(install_dir)

    def exit(self):
        self.on_exit_button_clicked.emit()
