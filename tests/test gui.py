from PyQt6.QtWidgets import QApplication, QMainWindow
from generated.LoginWindow import Ui_LoginWindow
from src.ClassUser import User  # Import your User class


class LoginWindow(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Setup the UI

        # Connect signals to slots
        self.loginButton.clicked.connect(self.on_login)
        #self.registerButton.clicked.connect(self.on_login())

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


        # # Perform login logic (replace with your authentication logic)
        # if self.user.authenticate(username, password):
        #     self.label.setText(f'Welcome, {username}! You are logged in.')
        # else:
        #     self.label.setText('Login failed. Please try again.')


if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec()


