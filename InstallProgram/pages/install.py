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
from PySide6.QtWidgets import QWidget, QLabel, QPushButton,  QMessageBox,QProgressBar
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

    def __init__(self, parent: Optional[QWidget] = None, install_dir:Path = Path("C:\\Program Files (x86)\\Default Company Name\\svn_plugin\\")) -> None:
        super().__init__(parent)
        self.install_dir = install_dir

    def getDisk(self):
        partitions = psutil.disk_partitions(all=False)
        disk_list = []
        for partition in partitions:
            disk_list.append(partition.device)
        return disk_list

    def registry(self):
        for key_path, values in config.REG_DATA.items():
            key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
            for value_name, value_data in values.items():
                winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
            key.Close()

        for num, disk in enumerate(self.getDisk()):
            key_path = f"SOFTWARE\\TortoiseSVN\\BugTraq Associations\\{num}"
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.SetValueEx(key, "Provider", 0, winreg.REG_SZ, "{D765C6EE-477A-4819-9809-BBF1C16F675D}")
            winreg.SetValueEx(key, "WorkingCopy", 0, winreg.REG_SZ, disk)
            winreg.CloseKey(key)
        print(f"注册表写入")

    def writeConfig(self):
        user_home = os.path.expanduser("~")
        documents_dir = os.path.join(user_home, "Documents")
        with open(f"{documents_dir}\\SvnPluginConfig.json", "w") as f:
            f.write(json.dumps(config.CONFIG_DATA, indent=4))
            print("配置文件")
    def set_install_dir(self, install_dir:str):
        print(f"set thread install_dir:{install_dir}")
        self.install_dir = Path(install_dir)

    def get_file_url(self,filename) -> Optional[str]:
            return f"http://effectplatform.xgjoy.org/aquaman/file/download?filename={filename}"
        

    def downlaod(self, url:str):
        r = requests.get(url)
        local_filename = f'{self.temp_file_path}'
        with open(local_filename, 'wb') as f:
            self.install_percent.emit(0.5, 0.0)
            f.write(r.content)
        self.install_percent.emit(1.0, 0.0)

    def unzip(self):
        run_as_admin()
        with zipfile.ZipFile(self.temp_file_path, "r") as zip_ref:
            zip_ref.extractall(self.install_dir)
        self.install_percent.emit(1.0, 1.0)
        

    def run(self) -> None:

        url = self.get_file_url("svn_plugin.zip")
        logging.info(f"安装路径:{url}")
        if url is None:
            self.file_not_found.emit()
            return
        self.downlaod(url)

        self.unzip()
        os.remove(self.temp_file_path)
        self.registry()
        self.writeConfig()
        time.sleep(3)
        self.install_finish.emit()

class InstallPage(PageBase):
    """
    选择安装路径的页面
    """
    on_last_page_button_clicked = Signal()
    on_next_button_clicked = Signal()
    on_exit_button_clicked = Signal()

    on_install_finish = Signal()
    
    def __init__(self, parent: Optional[QWidget] = None, default_dir:str = "C:/Program Files/xghub") -> None:
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
        self.progress_bar.setGeometry(180,50,350,25)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setVisible(False)
        self.label = QLabel("svn_plugin安装", self)
        self.label.setGeometry(180, 10, 200, 40)
        self.previous_button = QPushButton(f'{"上一步"}', self)
        self.previous_button.clicked.connect(self.last_page)
        self.previous_button.setGeometry(250, 324, 75, 25)
        self.install_button = QPushButton(f'{"安装"}', self)
        self.install_button.clicked.connect(self.install)
        self.install_button.setGeometry(330, 324, 75, 25)

        self.exit_button = QPushButton(f'{"退出"}', self)
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.setGeometry(410, 324, 75, 25)

        self.install_thread = InstallThread(self)
        self.install_thread.install_percent.connect(self.update_progress)
        self.install_thread.install_finish.connect(self.on_install_finish.emit)

    
    def update_progress(self, download_percent:float, unzip_percent:float):
        percent = 0.5*download_percent + 0.5*unzip_percent
        #print(download_percent, unzip_percent, percent)
        percent = max(0.0, min(1.0, percent))

    
    def install(self):
        running = False
        self.install_thread.start()
        for process in psutil.process_iter():
            # 如果进程名为 python，则打印进程的详细信息
            if process.name() == "TortoiseProc.exe":
                # 打印进程的详细信息
                QMessageBox.critical(self, "错误", "SVN正在运行,请先关闭SVN进程再点击安装")
                self.install_thread.quit()
                self.progress_bar.setVisible(False)
                running = True
        if not running:
            self.progress_bar.setMaximum(0)
            self.progress_bar.setVisible(True)

    def set_install_dir(self, install_dir:str):
        self.install_thread.set_install_dir(install_dir)

    def on_file_not_found(self):
        QMessageBox.critical(self, "错误", "未找到xghub安装包 请检查效能平台上安装包是否存在")

    def last_page(self):
        self.on_last_page_button_clicked.emit()

    def exit(self):
        self.on_exit_button_clicked.emit()
