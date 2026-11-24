from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, QPushButton
)
from PySide6.QtCore import Qt
from editor import MyEditor

class MyTable(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Таблиця графічних об'єктів")
        self.resize(450, 300)
        
        self.table = QTableWidget(0, 5, self)
        self.table.setHorizontalHeaderLabels(["Назва", "x1", "y1", "x2", "y2"])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.on_select = None
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
       
        self.delete_btn = QPushButton("Видалити")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self._delete_selected)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.delete_btn)
        
        self.table.itemSelectionChanged.connect(self._selection_changed)

        self.editor = MyEditor.get_instance()
        self.editor.subscribe(self.refresh)
        self.refresh()

    def set_select_callback(self, callback):
        self.on_select = callback

    def _selection_changed(self):
        rows = self.table.selectionModel().selectedRows()
        self.delete_btn.setEnabled(bool(rows))
        if self.on_select is not None:
            self.on_select(rows[0].row() if rows else None)

    def _delete_selected(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.clearSelection()
            self.table.setCurrentCell(-1, -1)
            self.editor.remove_shape(row)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self._delete_selected()
            return
        
        super().keyPressEvent(event)

    def refresh(self):
        selected = self.table.currentRow()
        shapes = self.editor.shapes
        self.table.setRowCount(len(shapes))
        
        for row, shape in enumerate(shapes):
            values = [shape.name, *shape.coords()]
            for col, value in enumerate(values):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        if 0 <= selected < len(shapes):
            self.table.selectRow(selected)
        else:
            self.table.clearSelection()

    def done(self, result):
        self.editor.unsubscribe(self.refresh)
        super().done(result)