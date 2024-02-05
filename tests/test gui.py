from PyQt6.QtWidgets import QApplication, QMainWindow
from generated.MainWindow import Ui_MainWindow

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Setup the UI

        # Connect signals to slots
        self.loginButton.clicked.connect(self.on_login)
        #self.registerButton.clicked.connect(self.on_login())

    def authenticate(self, username, password):
        # Replace with your authentication logic (e.g., check credentials against a database)
        # Return True if authentication succeeds, False otherwise
        return username == 'admin' and password == 'adminpass'

    def on_login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        # Perform login logic (replace with your authentication logic)
        if self.authenticate(username, password):
            self.label.setText(f'Welcome, {username}! You are logged in.')
        else:
            self.label.setText('Login failed. Please try again.')



if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec()