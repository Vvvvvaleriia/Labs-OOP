from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView
)
from editor import MyEditor

class MyTable(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Таблиця графічних об'єктів")
        self.resize(450, 300)

        self.table = QTableWidget(0, 5, self)
        self.table.setHorizontalHeaderLabels(["Назва", "x1", "y1", "x2", "y2"])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

        self.editor = MyEditor.get_instance()
        self.editor.subscribe(self.refresh)
        self.refresh()

    def refresh(self):
        shapes = self.editor.shapes
        self.table.setRowCount(len(shapes))
        for row, shape in enumerate(shapes):
            values = [shape.name, *shape.coords()]
            for col, value in enumerate(values):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def done(self, result):
        self.editor.unsubscribe(self.refresh)
        super().done(result)