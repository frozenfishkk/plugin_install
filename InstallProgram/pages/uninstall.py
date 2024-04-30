import json
import time
import winreg
import psutil
import requests
import zipfile
import os
import logging
from typing import Optional
from PySide6.QtGui import QPixmap
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


class InstallThread(QThread):
    install_finish = Signal()
    install_percent = Signal(float, float)
    file_not_found = Signal()

    install_dir: Path
    temp_file_path: Path = Path("temp.zip")

    def __init__(self, parent: Optional[QWidget] = None,
                 install_dir: Path = Path("C:\\Program Files (x86)\\Default Company Name\\svn_plugin\\")) -> None:
        super().__init__(parent)
        self.install_dir = install_dir

    def getDisk(self):
        partitions = psutil.disk_partitions(all=False)
        disk_list = []
        for partition in partitions:
            disk_list.append(partition.device)
        return disk_list

    def delete_registry_key(self,key, subkey):
        try:
            current_key = winreg.OpenKey(key, subkey, 0, winreg.KEY_ALL_ACCESS)
            subkey_count, _, _ = winreg.QueryInfoKey(current_key)
            for i in range(subkey_count):
                sub_name = winreg.EnumKey(current_key, 0)
                self.delete_registry_key(current_key, sub_name)
            winreg.CloseKey(current_key)
            winreg.DeleteKey(key, subkey)
            print(f"Deleted key: {subkey}")
        except FileNotFoundError:
            print(f"Key not found: {subkey}")
    def registry(self):
        key_path = r"CLSID\{D765C6EE-477A-4819-9809-BBF1C16F675D}"

        # 删除指定键及其所有子项
        root_key = winreg.HKEY_CLASSES_ROOT
        self.delete_registry_key(root_key, key_path)
        for num, disk in enumerate(self.getDisk()):
            key_path = f"SOFTWARE\\TortoiseSVN\\BugTraq Associations\\{num}"
            try:
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
            except FileNotFoundError:
                pass
        print(f"注册表删除")

    def set_install_dir(self, install_dir: str):
        print(f"set thread install_dir:{install_dir}")
        self.install_dir = Path(install_dir)


    def run(self) -> None:
        self.registry()
        time.sleep(3)
        self.install_finish.emit()



class unInstallPage(PageBase):
    """
    卸载
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
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(180, 50, 350, 25)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setVisible(False)
        self.label = QLabel("svn_plugin卸载中", self)
        self.label.setGeometry(180, 10, 200, 40)

        self.exit_button = QPushButton(f'{"退出"}', self)
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.setGeometry(410, 324, 75, 25)
        self.install_thread = InstallThread(self)
        self.install_thread.install_percent.connect(self.update_progress)
        self.install_thread.install_finish.connect(self.on_install_finish.emit)



    def update_progress(self, download_percent: float, unzip_percent: float):
        percent = 0.5 * download_percent + 0.5 * unzip_percent
        # print(download_percent, unzip_percent, percent)
        percent = max(0.0, min(1.0, percent))

    def un_install(self):
        self.install_thread.start()

        self.progress_bar.setMaximum(0)
        self.progress_bar.setVisible(True)


    def set_install_dir(self, install_dir: str):
        self.install_thread.set_install_dir(install_dir)


    def last_page(self):
        self.on_last_page_button_clicked.emit()

    def exit(self):
        self.on_exit_button_clicked.emit()
