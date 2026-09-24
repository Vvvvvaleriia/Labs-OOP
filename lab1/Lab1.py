import sys 
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtGui import QAction
import module1
import module2
import module3

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Lab1")
window.resize(600, 400)

menu_bar = window.menuBar()

work1 = QAction("Робота1", window)
work2 = QAction("Робота2", window)

menu_bar.addAction(work1)
menu_bar.addAction(work2)

group_label = QLabel("", window)
group_label.move(30, 50)

def open_work1_second():
    module2.show_dialog(window, open_work1_first)

def open_work1_first():
    module1.show_dialog(window, open_work1_second)

def group_selected(group):
    group_label.setText(group)

def open_work2():
    module3.show_dialog(window, group_selected)

work1.triggered.connect(lambda: module1.show_dialog(window, open_work1_second))
work2.triggered.connect(open_work2)

window.show()
sys.exit(app.exec())