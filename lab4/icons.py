from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QPen, QColor, QPalette, QIcon, QPixmap, QBrush, QPolygon

def create_icon(shape_name):
    pixmap = QPixmap(32, 32)
    pixmap.fill(QColor("#343333"))

    painter = QPainter(pixmap)

    if shape_name == "Крапка":
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("black"))
        painter.drawEllipse(QPoint(16, 16), 3, 3)

    elif shape_name == "Лінія":
        painter.setPen(QPen(QColor("black"), 2))
        painter.drawLine(4, 27, 28, 5)

    elif shape_name == "Прямокутник":
        painter.setPen(QPen(QColor("black"), 2))
        painter.setBrush(QBrush(QColor("#EFB3E5")))
        painter.drawRect(4, 7, 24, 18)
    
    elif shape_name == "Еліпс":
        painter.setPen(QPen(QColor("black"), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(4, 7, 24, 18)

    elif shape_name == "Лінія з колами":
        painter.setPen(QPen(QColor("black"), 2))
        painter.drawLine(4, 27, 28, 5)

        painter.setBrush(Qt.BrushStyle.BDiagPattern)
        painter.drawEllipse(1, 24, 6, 6)
        painter.drawEllipse(25, 2, 6, 6)

    elif shape_name == "Куб":
        painter.setPen(QPen(QColor("black"), 2))
        
        painter.setBrush(QBrush(QColor("#EFB3E5")))
        painter.drawRect(11, 5, 16, 16)

        painter.setBrush(QBrush(QColor("#F5D0EF")))
        painter.drawPolygon(QPolygon([
            QPoint(11, 5),
            QPoint(27, 5),
            QPoint(21, 11),
            QPoint(5, 11),
        ]))

        painter.setBrush(QBrush(QColor("#D98FCF")))
        painter.drawPolygon(QPolygon([
            QPoint(27, 5),
            QPoint(27, 21),
            QPoint(21, 27),
            QPoint(21, 11),
        ]))

        painter.setBrush(QBrush(QColor("#EFB3E5")))
        painter.drawRect(5, 11, 16, 16)

    painter.end()

    return QIcon(pixmap)