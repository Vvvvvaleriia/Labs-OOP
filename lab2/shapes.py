from abc import ABC, abstractmethod
from PySide6.QtCore import QPoint
from PySide6.QtGui import QColor, QPainter, QPen, QBrush

class Shape(ABC):
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @abstractmethod
    def draw(self, painter: QPainter):
        pass

class Point(Shape):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, x, y)

    def draw(self, painter: QPainter):
        painter.setPen(QPen(QColor("black"), 3))
        painter.drawPoint(QPoint(self.x1, self.y1))

class Line(Shape):
    def draw(self, painter: QPainter):
        painter.setPen(QPen(QColor("black"), 2))
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)

class Rectangle(Shape):
    def draw(self, painter: QPainter):
        left = min(self.x1, self.x2)
        top = min(self.y1, self.y2)
        width = abs(self.x2 - self.x1)
        height = abs(self.y2 - self.y1)

        painter.setPen(QPen(QColor("black"), 2))
        painter.setBrush(QBrush(QColor("#87CEFA")))
        painter.drawRect(left, top, width, height)

class Ellipse(Shape):
    def draw(self, painter: QPainter):
        radius_x = abs(self.x2 - self.x1)
        radius_y = abs(self.y2 - self.y1)

        left = self.x1 - radius_x
        top = self.y1 - radius_y
        width = radius_x * 2
        height = radius_y * 2

        painter.setPen(QPen(QColor("black"), 2))
        painter.setBrush(QBrush(QColor("white")))
        painter.drawEllipse(left, top, width, height)