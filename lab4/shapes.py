from abc import ABC, abstractmethod
from PySide6.QtCore import Qt
from PySide6.QtCore import QPoint
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QPolygon

class Shape(ABC):
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @abstractmethod
    def draw(self, painter: QPainter):
        pass

    @abstractmethod
    def draw_preview(self, painter: QPainter):
        pass

class Point(Shape):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, x, y)

    def draw(self, painter: QPainter):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("black"))
        painter.drawEllipse(QPoint(self.x1, self.y1), 4, 4)

    def draw_preview(self, painter: QPainter):
        pass

class Line(Shape):
    def draw(self, painter: QPainter):
        painter.setPen(QPen(QColor("black"), 3))
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)

    def draw_preview(self, painter: QPainter):
        painter.setPen(QPen(QColor("black"), 3, Qt.PenStyle.DashLine))
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)

class Rectangle(Shape):
    def _geometry(self):
        radius_x = abs(self.x2 - self.x1)
        radius_y = abs(self.y2 - self.y1)

        left = self.x1 - radius_x
        top = self.y1 - radius_y
        width = radius_x * 2
        height = radius_y * 2

        return left, top, width, height

    def draw(self, painter: QPainter):
        left, top, width, height = self._geometry()

        painter.setPen(QPen(QColor("black"), 3))
        painter.setBrush(QBrush(QColor("#EFB3E5")))
        painter.drawRect(left, top, width, height)

    def draw_preview(self, painter: QPainter):
        left, top, width, height = self._geometry()

        painter.setPen(QPen(QColor("black"), 3, Qt.PenStyle.DashLine))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(left, top, width, height)

class Ellipse(Shape):
    def _geometry(self):
        left = min(self.x1, self.x2)
        top = min(self.y1, self.y2)
        width = abs(self.x2 - self.x1)
        height = abs(self.y2 - self.y1)

        return left, top, width, height

    def draw(self, painter: QPainter):
        left, top, width, height = self._geometry()

        painter.setPen(QPen(QColor("black"), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(left, top, width, height)

    def draw_preview(self, painter: QPainter):
        left, top, width, height = self._geometry()

        painter.setPen(QPen(QColor("black"), 3, Qt.PenStyle.DashLine))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(left, top, width, height)

class LineWithCircles(Shape):
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        super().__init__(x1, y1, x2, y2)

        radius = 10

        self.line = Line(x1, y1, x2, y2)

        self.circle1 = Ellipse(
        x1 - radius,
        y1 - radius,
        x1 + radius,
        y1 + radius
        )
        
        self.circle2 = Ellipse(
        x2 - radius,
        y2 - radius,
        x2 + radius,
        y2 + radius
        )

    def draw(self, painter: QPainter):
        self.line.draw(painter)
        self.circle1.draw(painter)
        self.circle2.draw(painter)
        
    def draw_preview(self, painter: QPainter):
        self.line.draw_preview( painter)
        self.circle1.draw_preview(painter)
        self.circle2.draw_preview( painter)

class Cube(Shape):
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        super().__init__(x1, y1, x2, y2)

        width = abs(x2 - x1)
        height = abs(y2 - y1)

        side = int(min(width, height) / 1.3)
        side = (side // 2) * 2

        self.valid = side >= 2
        if not self.valid:
            return
        
        depth = int(side * 0.3)
        half = side // 2
        total = side + depth

        if x2 >= x1:
            left = x1
        else: left = x1 - total
        
        if y2 >= y1:
            top = y1
        else: top = y1 - total

        self.back = Rectangle(
            left + depth + half,
            top + half,
            left + depth + side, 
            top + side,
        )

        self.front = Rectangle(
            left + half,
            top + depth + half,
            left + side, 
            top + depth + side,
        )

        self.top_face = QPolygon([
            QPoint(left + depth, top),
            QPoint(left + depth + side, top),
            QPoint(left + side, top + depth),
            QPoint(left, top + depth)
        ])

        self.right_face = QPolygon([
            QPoint(left + depth + side, top),
            QPoint(left + depth + side, top + side),
            QPoint(left + side, top + depth + side),
            QPoint(left + side, top + depth)
        ])

        self.edges = [
            Line(left + depth, top, left, top + depth),                           
            Line(left + depth + side, top, left + side, top + depth),             
            Line(left + depth + side, top + side, left + side, top + depth + side),  
            Line(left + depth, top + side, left, top + depth + side),             
        ]

    def draw(self, painter: QPainter):
        if not self.valid:
            return
        
        self.back.draw(painter)

        painter.setPen(QPen(QColor("black"), 3))
        painter.setBrush(QBrush(QColor("#F5D0EF")))
        painter.drawPolygon(self.top_face)

        painter.setBrush(QBrush(QColor("#D98FCF")))
        painter.drawPolygon(self.right_face)

        self.front.draw(painter)

    def draw_preview(self, painter: QPainter):
        if not self.valid:
            return

        self.back.draw_preview(painter)
        self.front.draw_preview(painter)

        for edge in self.edges:
            edge.draw_preview(painter)