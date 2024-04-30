from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QPaintEvent
from PySide6.QtCore import QRectF
from typing import Optional, Union

number = Union[int, float]

class CircularProgress(QWidget):
    value: number
    max_value: number

    def __init__(self, parent: Optional[QWidget], max_value:number=100, value:number=0) -> None:
        super().__init__(parent)
        self.max_value = max_value
        self.value = value

    def get_value(self)->number:
        return self.value
    
    def set_value(self, value:number):
        self.value = value
        self.update()

    def inc_value(self, inc_value:number):
        self.value += inc_value
        self.update()

    def get_max_value(self)->number:
        return self.max_value
    
    def set_max_value(self, max_value:number):
        self.max_value = max_value
        self.update()

    def inc_max_value(self, inc_value:number):
        self.max_value+=inc_value
        self.update()
    
    def get_percent(self)->float:
        return self.value/self.max_value
    
    def set_percent(self, percent:float):
        self.value = percent*self.max_value
        self.update()
    
    def get_color(self)->QColor:
        red = int(255.0 * (1.0 - self.get_percent()))
        green = int(255.0 * self.get_percent())
        blue = 0
        alpha = int(200.0 * self.get_percent()+50.0)

        red = min(max(red, 0), 255)
        green = min(max(green, 0), 255)
        blue = min(max(blue, 0), 255)
        alpha = min(max(alpha, 0), 255)
        return QColor(red, green, blue, alpha)
    
    def get_painter(self)->QPainter:
        color = self.get_color()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(color, 8)
        painter.setPen(pen)
        return painter
    
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = self.get_painter()
        rect = QRectF(10, 10, self.width() - 20, self.height() - 20)
        painter.drawRect(rect)
        return super().paintEvent(event)

    
