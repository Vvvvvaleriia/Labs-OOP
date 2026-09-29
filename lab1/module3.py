import json
from PySide6.QtWidgets import QDialog, QPushButton, QListWidget

def show_dialog(parent, on_select):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Робота2")
    dialog.resize(400, 300)

    groups_list = QListWidget(dialog)
    groups_list.addItem("")
    groups_list.item(0).setHidden(True)
    
    groups_list.move(30, 30)
    groups_list.resize(340, 180)

    with open("groups.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for group in data:
        groups_list.addItem(group)
    
    groups_list.setCurrentRow(-1)

    yes_button = QPushButton("Так", dialog)
    yes_button.move(100, 230)
    cancel_button = QPushButton("Відміна", dialog)
    cancel_button.move(200, 230)

    def yes_clicked():
        selected_items = groups_list.selectedItems()

        if selected_items:
            on_select(selected_items[0].text())
            dialog.close()

    def cancel_clicked():
        dialog.close()

    yes_button.clicked.connect(yes_clicked)
    cancel_button.clicked.connect(cancel_clicked)

    dialog.exec()