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

class LineWithCircles(Line, Ellipse):
    name = "Лінія з кружечками"

    def _circles(self):
        radius = 10

        circle1 = Ellipse(
        self.x1 - radius,
        self.y1 - radius,
        self.x1 + radius,
        self.y1 + radius
        )
        
        circle2 = Ellipse(
        self.x2 - radius,
        self.y2 - radius,
        self.x2 + radius,
        self.y2 + radius
        )

        return circle1, circle2

    def draw(self, painter: QPainter):
        circle1, circle2 = self._circles()

        Line.draw(self, painter)
        Ellipse.draw(circle1, painter)
        Ellipse.draw(circle2, painter)
        
    def draw_preview(self, painter: QPainter):
        circle1, circle2 = self._circles()

        Line.draw_preview(self, painter)
        Ellipse.draw_preview(circle1, painter)
        Ellipse.draw_preview(circle2, painter)

class Cube(Line, Rectangle):
    name = "Куб"

    def _geometry(self, painter: QPainter, preview: bool):
        width = abs(self.x2 - self.x1)
        height = abs(self.y2 - self.y1)

        side = int(min(width, height) / 1.3)
        side = (side // 2) * 2

        if side < 2:
            return
        
        depth = int(side * 0.3)
        half = side // 2
        total = side + depth

        if self.x2 >= self.x1:
            left = self.x1
        else: left = self.x1 - total
        
        if self.y2 >= self.y1:
            top = self.y1
        else: top = self.y1 - total

        back = Rectangle(
            left + depth + half,
            top + half,
            left + depth + side, 
            top + side,
        )

        front = Rectangle(
            left + half,
            top + depth + half,
            left + side, 
            top + depth + side,
        )

        top_face = QPolygon([
            QPoint(left + depth, top),
            QPoint(left + depth + side, top),
            QPoint(left + side, top + depth),
            QPoint(left, top + depth)
        ])

        right_face = QPolygon([
            QPoint(left + depth + side, top),
            QPoint(left + depth + side, top + side),
            QPoint(left + side, top + depth + side),
            QPoint(left + side, top + depth)
        ])

        if preview:
            draw_rect = Rectangle.draw_preview
        else: draw_rect = Rectangle.draw

        draw_rect(back, painter)

        if preview: 
            painter.setPen(QPen(QColor("black"), 3, Qt.PenStyle.DashLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPolygon(top_face)
            painter.drawPolygon(right_face)
        else:
            painter.setPen(QPen(QColor("black"), 3))
            painter.setBrush(QBrush(QColor("#F5D0EF")))
            painter.drawPolygon(top_face)

            painter.setBrush(QBrush(QColor("#D98FCF")))
            painter.drawPolygon(right_face)

        draw_rect(front, painter)

        if preview:
            hidden_edge = Line(
                left + depth, 
                top + side,
                left,
                top + depth + side
            )
            Line.draw_preview(hidden_edge, painter)

    def draw(self, painter: QPainter):
        self._geometry(painter, False)

    def draw_preview(self, painter: QPainter):
        self._geometry(painter, True)