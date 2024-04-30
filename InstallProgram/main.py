
from PySide6.QtWidgets import QMainWindow, QApplication, QStackedWidget,QVBoxLayout,QProgressBar,QHBoxLayout
from pages import  InstallPage, FinishPage,alreadyInstallPage
import logging
import os
import utils
from pages.start import startPage
from pages.uninstall import unInstallPage
from utils import run_as_admin,check_registry_key

class Window(QMainWindow):
    install_dir: str
    def __init__(self):
        super().__init__()
        self.resize(500, 360)
        self.move(700, 210)
        self.setWindowTitle("svn_plugin安装程序")
        # 检查指定的注册表键是否存在
        key_path = r"CLSID\{D765C6EE-477A-4819-9809-BBF1C16F675D}"


        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        if check_registry_key(key_path):
            self.alreadyInstall = alreadyInstallPage()
            self.alreadyInstall.on_exit_button_clicked.connect(self.exit)
            self.alreadyInstall.on_next_button_clicked.connect(self.goto_next_page)
            self.stacked_widget.addWidget(self.alreadyInstall)
            self.alreadyInstall.on_uninstall_start.connect(self.goto_uninstall)
        self.startpage = startPage()
        self.startpage.on_exit_button_clicked.connect(self.exit)
        self.startpage.on_next_button_clicked.connect(self.goto_next_page)

        self.stacked_widget.addWidget(self.startpage)

        self.install_page = InstallPage(self)
        self.install_page.on_last_page_button_clicked.connect(self.goto_last_page)


        self.install_page.on_exit_button_clicked.connect(self.exit)
        self.install_page.on_install_finish.connect(self.goto_next_page)
        self.stacked_widget.addWidget(self.install_page)

        self.finish_page = FinishPage()
        self.finish_page.on_exit_button_clicked.connect(self.exit)
        self.stacked_widget.addWidget(self.finish_page)
        self.unInstallPage = unInstallPage()
        self.unInstallPage.on_exit_button_clicked.connect(self.exit)
        self.unInstallPage.on_install_finish.connect(self.goto_finish)
        self.stacked_widget.addWidget(self.unInstallPage)

    def set_install_dir(self, install_dir:str):
        self.install_dir = install_dir
        self.install_page.set_install_dir(install_dir)
        self.finish_page.set_install_dir(install_dir)

    def exit(self):
        self.close()
    def goto_finish(self):
        self.finish_page.label.setText("卸载完成")
        self.stacked_widget.setCurrentIndex(3)
    def goto_uninstall(self):
        self.stacked_widget.setCurrentIndex(4)
        self.unInstallPage.un_install()
    def goto_page(self, index:int):
        self.stacked_widget.setCurrentIndex(index)

    def goto_next_page(self):
        index = self.stacked_widget.currentIndex()
        self.goto_page(index+1)

    def goto_last_page(self):
        index = self.stacked_widget.currentIndex()
        self.goto_page(index-1)

    def after_install_work(self):
        desktop_ink_path = os.path.join(os.path.expanduser("~"), "Desktop", "xghub.lnk")
        utils.create_shortcut(desktop_ink_path, 
                              f"{self.install_dir}/xghub.exe",
                              "",
                              f"{self.install_dir}",
        )

        if self.install_page.is_append_env_var():
            utils.append_path_env(f"{self.install_dir}/svn")
        if self.install_page.is_run_xghub():
            cmd = f"{self.install_dir}/xghub.exe"
            os.chdir(self.install_dir)
            os.execl(cmd, cmd)
        

if __name__ == '__main__':
    logging.basicConfig(filename="test.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%M-%d %H:%M:%S", level=logging.DEBUG)
    #run_as_admin()
    app = QApplication([])
    w = Window()
    w.show()
    app.exec()  
