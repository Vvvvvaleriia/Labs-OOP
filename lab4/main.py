import sys
from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QAction, QPainter, QPen, QColor, QPalette, QIcon, QPixmap, QBrush, QMouseEvent, QPolygon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QToolBar,
    QMessageBox,
)
from shapes import Shape, Point, Line, Rectangle, Ellipse, LineWithCircles, Cube
from icons import create_icon

N = 127

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

            elif self.current_shape == "Лінія з колами":
                shape = LineWithCircles(self.x1, self.y1, self.x2, self.y2)
            
            elif self.current_shape == "Куб":
                shape = Cube(self.x1, self.y1, self.x2, self.y2)

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

            if self.current_shape == "Лінія":
                preview_shape = Line(self.x1, self.y1, self.x2, self.y2)

            elif self.current_shape == "Прямокутник":
                preview_shape = Rectangle(self.x1, self.y1, self.x2, self.y2)

            elif self.current_shape == "Еліпс":
                preview_shape = Ellipse(self.x1, self.y1, self.x2, self.y2)

            elif self.current_shape == "Лінія з колами":
                preview_shape = LineWithCircles(self.x1, self.y1, self.x2, self.y2)

            elif self.current_shape == "Куб":
                preview_shape = Cube(self.x1, self.y1, self.x2, self.y2)


            preview_shape.draw_preview(painter)

class MyEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lab4")
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

        shape_names = ["Крапка", "Лінія", "Прямокутник", "Еліпс", "Лінія з колами", "Куб"]

        self.shape_actions: dict[str, QAction] = {} 

        for name in shape_names:
            action = QAction(create_icon(name), name, self)
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

        self.setWindowTitle(f"Lab4 - {shape_name}")

    def clear_canvas(self):
        self.drawing_area.pcshape.clear()
        self.drawing_area.update()

    def show_about(self):
        QMessageBox.about(self, "Про програму", "Lab4 - графічний редактор\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyEditor()
    window.show()

    exit_code = app.exec()

    del window

    sys.exit(exit_code)
