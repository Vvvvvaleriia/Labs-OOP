import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QPainter, QColor, QPalette, QMouseEvent, QPen
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QToolBar, QMessageBox, QFileDialog
)
from shapes import Shape
from icons import create_icon
from editor import MyEditor
from my_table import MyTable

class DrawingArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.editor = MyEditor.get_instance()
        self.editor.subscribe(self.update)

        self.current_shape = "Крапка"

        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        self.drawing = False

        self.selected_index = None

        self.setMinimumSize(600, 400)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("white"))
        self.setPalette(palette)

    def set_shape(self, shape_name):
        self.current_shape = shape_name

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        
        self.x1 = self.x2 = int(event.position().x())
        self.y1 = self.y2 = int(event.position().y())

        shape_class: type[Shape] = Shape.registry[self.current_shape]

        if shape_class.click_only:
            self.add_shape(shape_class(self.x1, self.y1))
        else:
            self.drawing = True

        self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drawing:
            self.x2 = int(event.position().x())
            self.y2 = int(event.position().y())

        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.x2 = int(event.position().x())
            self.y2 = int(event.position().y())

            shape_class = Shape.registry[self.current_shape]
            self.add_shape(shape_class(self.x1, self.y1, self.x2, self.y2))

            self.drawing = False
            self.update()

    def add_shape(self, shape):
        if not self.editor.add_shape(shape):
            QMessageBox.warning(self, "Увага",
                f"Досягнуто максимальної кількості фігур: {self.editor.MAX_SHAPES}")

    def paintEvent(self, event):
        painter = QPainter(self)

        for shape in self.editor.shapes:
            shape.draw(painter)

        if self.selected_index is not None and self.selected_index < len(self.editor.shapes):
            left, top, width, height = self.editor.shapes[self.selected_index].bounds()
            painter.setPen(QPen(QColor("red"), 2, Qt.PenStyle.DashLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(left - 4, top - 4, width + 8, height + 8)

        if self.drawing:
            shape_class = Shape.registry[self.current_shape]
            shape_class(self.x1, self.y1, self.x2, self.y2).draw_preview(painter)

    def set_selected(self, index):
        self.selected_index = index
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab5")
        self.resize(800, 600)

        self.editor = MyEditor.get_instance()
        self.table = None

        self.drawing_area = DrawingArea(self)
        self.setCentralWidget(self.drawing_area)

        self.create_menu()
        self.create_toolbar()

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Файл")
        save_action = QAction("Зберегти як CSV", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        open_action = QAction("Відкрити CSV", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        clear_action = QAction("Очистити", self)
        clear_action.triggered.connect(self.clear_canvas)
        file_menu.addAction(clear_action)

        self.objects_menu = menu_bar.addMenu("Об'єкти")

        self.shape_actions: dict[str, QAction] = {}

        for name in Shape.registry:                      
            action = QAction(create_icon(name), name, self)
            action.triggered.connect(lambda checked=False, n=name: self.select_shape(n))
            
            self.objects_menu.addAction(action)
            self.shape_actions[name] = action

        self.table_action = QAction("Таблиця", self)
        self.table_action.setCheckable(True)
        self.table_action.triggered.connect(self.toggle_table)
        menu_bar.addAction(self.table_action)

        help_menu = menu_bar.addMenu("Довідка")
        about_action = QAction("Про програму", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        toolbar = QToolBar("Інструменти", self)
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        self.toolbar_actions: dict[str, QAction] = {}

        for name in Shape.registry:
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

        self.setWindowTitle(f"Lab5 - {shape_name}")

    def toggle_table(self, checked):
        if checked:
            self.table = MyTable(self)
            self.table.set_select_callback(self.drawing_area.set_selected)
    
            self.table.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.table.finished.connect(self.on_table_closed)

            self.table.show()                  
        elif self.table is not None:
            self.table.close()

    def on_table_closed(self):
        self.table = None
        self.table_action.setChecked(False)
        self.drawing_area.set_selected(None)

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Зберегти", "shapes.csv", "CSV (*.csv)")
        ##[path, _]
        if path:
            self.editor.save_csv(path)

    def clear_canvas(self):
        self.editor.clear()
        self.drawing_area.set_selected(None)
        self.drawing_area.update()

    def show_about(self):
        QMessageBox.about(self, "Про програму", "Lab5 - графічний редактор\n")

    def closeEvent(self, event):
        if self.table is not None:
            self.table.close()                  
        event.accept()
        self.editor.unsubscribe(self.drawing_area.update)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Відкрити", "", "CSV (*.csv)")
        if not path:
            return
        
        try: 
            self.editor.load_csv(path)
        except OSError as err:
          QMessageBox.warning(self, "Помилка", f"Не вдалося відкрити файл:\n{err}") 
          return
        self.drawing_area.set_selected(None) 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    exit_code = app.exec()

    del window
    MyEditor.release()
    
    sys.exit(exit_code)