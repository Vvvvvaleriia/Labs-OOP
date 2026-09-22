import sys 
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QAction
import module1
import module2

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Lab1")
window.resize(600, 400)

menu_bar = window.menuBar()

work1 = QAction("Робота1", window)
work2 = QAction("Робота2", window)

menu_bar.addAction(work1)
menu_bar.addAction(work2)

def open_work1_second():
    module2.show_dialog(window, open_work1_first)

def open_work1_first():
    module1.show_dialog(window, open_work1_second)

work1.triggered.connect(lambda: module1.show_dialog(window, open_work1_second))

window.show()
sys.exit(app.exec())