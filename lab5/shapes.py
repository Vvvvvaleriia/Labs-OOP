from abc import ABC, abstractmethod
from PySide6.QtCore import Qt
from PySide6.QtCore import QPoint
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QPolygon

class Shape(ABC):
    name = ""
    click_only = False
    registry: dict[str, type["Shape"]] = {}

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __init_subclass__(cls):
        ##super().__init_subclass__()
        if "name" in cls.__dict__:
            Shape.registry[cls.name] = cls

    def coords(self):
        return self.x1, self.y1, self.x2, self.y2
    
    def bounds(self):
        return (min(self.x1, self.x2), min(self.y1, self.y2),
            abs(self.x2 - self.x1), abs(self.y2 - self.y1))

    @abstractmethod
    def draw(self, painter: QPainter):
        pass

    @abstractmethod
    def draw_preview(self, painter: QPainter):
        pass

class Point(Shape):
    name = "Крапка"
    click_only = True

    def __init__(self, x: int, y: int):
        super().__init__(x, y, x, y)

    def draw(self, painter: QPainter):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("black"))
        painter.drawEllipse(QPoint(self.x1, self.y1), 4, 4)

    def draw_preview(self, painter: QPainter):
        pass

class Line(Shape):
    name = "Лінія"

    def draw(self, painter: QPainter):
        painter.setPen(QPen(QColor("black"), 3))
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)

    def draw_preview(self, painter: QPainter):
        painter.setPen(QPen(QColor("black"), 3, Qt.PenStyle.DashLine))
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)

class Rectangle(Shape):
    name = "Прямокутник"

    def _geometry(self):
        radius_x = abs(self.x2 - self.x1)
        radius_y = abs(self.y2 - self.y1)

        left = self.x1 - radius_x
        top = self.y1 - radius_y
        width = radius_x * 2
        height = radius_y * 2

        return left, top, width, height
    
    def bounds(self):
        return self._geometry()

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
    name = "Еліпс"

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
    name = "Лінія з кружечками"

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

    def bounds(self):
        r = 10
        return (min(self.x1, self.x2) - r, min(self.y1, self.y2) - r,
            abs(self.x2 - self.x1) + 2 * r, abs(self.y2 - self.y1) + 2 * r)

    def draw(self, painter: QPainter):
        self.line.draw(painter)
        self.circle1.draw(painter)
        self.circle2.draw(painter)
        
    def draw_preview(self, painter: QPainter):
        self.line.draw_preview( painter)
        self.circle1.draw_preview(painter)
        self.circle2.draw_preview( painter)

class Cube(Shape):
    name = "Куб"

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        super().__init__(x1, y1, x2, y2)

        width = abs(x2 - x1)
        height = abs(y2 - y1)

        side = int(min(width, height) / 1.3)
        side = (side // 2) * 2

        self.valid = side >= 2
        self._bounds = (x1, y1, 0, 0)
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

        self._bounds = (left, top, total, total)

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

    def bounds(self):
        return self._bounds

    def draw(self, painter: QPainter):
        
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