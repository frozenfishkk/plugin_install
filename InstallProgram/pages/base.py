from typing import Optional
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtGui import QPaintEvent, QPainter
from utils.path import RESOURCE_PATH
import resource_rc
class PageBase(QWidget):
    left_background_image_label: QLabel

    def __init__(self, parent: Optional[QWidget]=None) -> None:
        QWidget.__init__(self, parent)
        self.init_gui()

    def init_gui(self):
        self.setFixedSize(500, 360)
        self.init_icon()
        self.init_left_background_image()

    def init_icon(self):
        self.setWindowIcon(QIcon((RESOURCE_PATH/"ico.png").as_posix()))

    def init_left_background_image(self):
        pix = QPixmap(":/left_bg.jpg")
        self.left_background_image_label = QLabel(self)
        self.left_background_image_label.setGeometry(-1, -1, 300, 318)
        self.left_background_image_label.setPixmap(pix)

    def paintEvent(self, event: QPaintEvent) -> None:
        qp = QPainter()
        qp.begin(self)
        qp.drawLine(0, 315, 1000, 315)
        qp.end()
        return super().paintEvent(event)
    


