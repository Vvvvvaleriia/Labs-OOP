from PySide6.QtWidgets import QDialog, QPushButton

def show_dialog(parent, on_next):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Робота1")
    dialog.resize(300, 200)

    next_button = QPushButton("Далі >", dialog)
    next_button.move(50, 140)
    cancel_button = QPushButton("Відміна", dialog)
    cancel_button.move(160, 140)

    def next_clicked():
        dialog.close()
        on_next()

    def cancel_clicked():
        dialog.close()

    next_button.clicked.connect(next_clicked)
    cancel_button.clicked.connect(cancel_clicked)

    dialog.exec()