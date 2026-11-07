import sys
from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QAction, QPainter, QPen, QColor, QPalette, QIcon, QPixmap, QBrush, QMouseEvent
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QToolBar,
    QMessageBox,
)
from shapes import Shape, Point, Line, Rectangle, Ellipse

N = 127

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

    painter.end()

    return QIcon(pixmap)       

class DrawingArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pcshape = []

        self.current_shape = "Крапка"

        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        self.drawing = False

        self.setMinimumSize(600, 400)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("white"))
        self.setPalette(palette)

    def set_shape(self, shape_name):
        self.current_shape = shape_name

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.x1 = int(event.position().x())
            self.y1 = int(event.position().y())

            self.x2 = self.x1
            self.y2 = self.y1

            self.drawing = True

            if self.current_shape == "Крапка":
                self.add_shape(Point(self.x1, self.y1))

                self.drawing = False

            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drawing:
            self.x2 = int(event.position().x())
            self.y2 = int(event.position().y())
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if (event.button() == Qt.MouseButton.LeftButton and self.drawing):
            self.x2 = int(event.position().x())
            self.y2 = int(event.position().y())

            if self.current_shape == "Лінія":
                shape = Line(self.x1, self.y1, self.x2, self.y2)

            elif self.current_shape == "Прямокутник":
                shape = Rectangle(self.x1, self.y1, self.x2, self.y2)

            elif self.current_shape == "Еліпс":
                shape = Ellipse(self.x1, self.y1, self.x2, self.y2)

            else: shape = None

            if shape is not None:
                self.add_shape(shape) 

            self.drawing = False    
            self.update()

    def add_shape(self, shape):
        if len(self.pcshape) >= N:
            QMessageBox.warning(self, "Увага", "Досягнуто максимальної кількості фігур: 127")
            return
        
        self.pcshape.append(shape)

    def paintEvent(self, event):
        painter = QPainter(self)

        for shape in self.pcshape:
            shape: Shape
            shape.draw(painter)

        if self.drawing and self.current_shape != "Крапка":
            painter.setPen(QPen(QColor("black"), 3, Qt.PenStyle.DashLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)

            if self.current_shape == "Лінія":
                painter.drawLine(self.x1, self.y1, self.x2, self.y2)

            elif self.current_shape == "Прямокутник":
                radius_x = abs(self.x2 - self.x1)
                radius_y = abs(self.y2 - self.y1)

                left = self.x1 - radius_x
                top = self.y1 - radius_y
                width = radius_x * 2
                height = radius_y * 2

                painter.drawRect(left, top, width, height)

            elif self.current_shape == "Еліпс":
                left = min(self.x1, self.x2)
                top = min(self.y1, self.y2)
                width = abs(self.x2 - self.x1)
                height = abs(self.y2 - self.y1)

                painter.drawEllipse(left, top, width, height)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lab3")
        self.resize(800, 600)

        self.drawing_area = DrawingArea(self)
        self.setCentralWidget(self.drawing_area)

        self.shape_actions = {}

        self.create_menu()
        self.create_toolbar()

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Файл")
        clear_action = QAction("Очистити", self)
        clear_action.triggered.connect(self.clear_canvas)
        file_menu.addAction(clear_action)

        self.objects_menu = menu_bar.addMenu("Об'єкти")

        shape_names = ["Крапка", "Лінія", "Прямокутник", "Еліпс"]

        self.shape_actions: dict[str, QAction] = {} 

        for name in shape_names:
            action = QAction(create_icon(name), name, self)
            action.setToolTip(name)
            action.triggered.connect(lambda checked=False, n=name: self.select_shape(n))

            self.objects_menu.addAction(action)
            self.shape_actions[name] = action

        help_menu = menu_bar.addMenu("Довідка")
        about_action = QAction("Про програму", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        toolbar = QToolBar("Інструменти", self)
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(32,32))

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        self.toolbar_actions: dict[str, QAction] = {} 

        for name in self.shape_actions:
            action = QAction(create_icon(name), name, self)
            action.setCheckable(True)
            action.setToolTip(name)
            action.triggered.connect(lambda checked=False, n=name: self.select_shape(n))

            toolbar.addAction(action)
            self.toolbar_actions[name] = action

        self.toolbar_actions["Крапка"].setChecked(True)

    def select_shape(self, shape_name):
        self.drawing_area.set_shape(shape_name)

        for name, action in self.toolbar_actions.items():
            action.setChecked(name == shape_name)

        self.setWindowTitle(f"Lab3 - {shape_name}")

    def clear_canvas(self):
        self.drawing_area.pcshape.clear()
        self.drawing_area.update()

    def show_about(self):
        QMessageBox.about(self, "Про програму", "Lab3 - графічний редактор\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
