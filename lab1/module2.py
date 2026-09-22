from PySide6.QtWidgets import QDialog, QPushButton

def show_dialog(parent, on_back):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Робота1")
    dialog.resize(300, 200)

    back_button = QPushButton("Назад <", dialog)
    back_button.move(20, 140)
    yes_button = QPushButton("Так", dialog)
    yes_button.move(110, 140)
    cancel_button = QPushButton("Відміна", dialog)
    cancel_button.move(200, 140)

    def back_clicked():
        dialog.close()
        on_back()

    def yes_clicked():
        dialog.close()

    def cancel_clicked():
        dialog.close()

    back_button.clicked.connect(back_clicked)
    yes_button.clicked.connect(yes_clicked)
    cancel_button.clicked.connect(cancel_clicked)

    dialog.exec()
