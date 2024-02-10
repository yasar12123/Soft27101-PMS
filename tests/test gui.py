from PyQt6.QtWidgets import QApplication, QMainWindow
from generated.LoginWindow import Ui_LoginWindow
from generated.RegisterWindow import Ui_RegisterWindow
from src.ClassUser import User  # Import your User class


class LoginWindow(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect signals to slots
        self.loginButton.clicked.connect(self.on_login)
        self.registerButton.clicked.connect(self.open_register_window)

        # Instantiate user
        self.user = User()

    def on_login(self):
        username = self.usernameLE.text()
        password = self.passwordLE.text()
        userAuthentication = self.user.authenticate(username, password)

        if userAuthentication == 'Login Successful':
            self.signInLabel.setText(f'Welcome, {username}! You have now logged in.')
        else:
            self.signInLabel.setText(userAuthentication)

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()




class RegisterWindow(QMainWindow, Ui_RegisterWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)






if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()


