from PyQt6.QtWidgets import QApplication
from src.ClassLoginWindow import LoginWindow


app = QApplication([])
window = LoginWindow()
window.show()
app.exec()
