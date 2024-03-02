from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from generated.LoginWindow import Ui_LoginWindow
from src.ClassRegisterWindow import RegisterWindow
from src.ClassHomeWindow import HomeWindow
import threading




# QObject subclass to open home window once authentiation has finished
class SignalEmitter(QObject):

    open_home_window = pyqtSignal()


class LoginWindow(QMainWindow, Ui_LoginWindow):
    """Class for the login window."""

    def __init__(self):
        """Constructor method"""
        super().__init__()
        self.setupUi(self)
        self.home_window = None
        self.activeUserInstance = None
        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()

        # Connect signals to slots
        self.loginButton.clicked.connect(self.start_login_thread)
        self.registerButton.clicked.connect(self.open_register_window)

        # SignalEmitter - authentication_finished
        self.authentication_finished = SignalEmitter()
        self.authentication_finished.open_home_window.connect(self.open_home_window)

    def start_login_thread(self):
        # Disable UI elements during login attempt
        self.loginButton.setEnabled(False)
        self.registerButton.setEnabled(False)
        # Start a new thread for login
        login_thread = threading.Thread(target=self.on_login)
        login_thread.start()

    def on_login(self):
        """Method to handle the login process."""
        # get input from window
        username = self.usernameLE.text()
        password = self.passwordLE.text()

        # Test database connectivity
        self.signInLabel.setText('Establishing Database Connection.')
        connectivity_result = self.dbCon.test_connectivity()
        # if connection is established
        if connectivity_result == 'Connection Established':

            # authenticate user
            self.signInLabel.setText('Please wait, trying to log you in.')
            authentication_status, user_instance = User().authenticate_user(self.session, username, password)
            # If the authentication is successful
            if authentication_status == 'Login Successful':
                # Set active user instance
                self.activeUserInstance = user_instance
                # Emit signal to open the home window
                self.authentication_finished.open_home_window.emit()

            # If the authentication fails, display the error message
            else:
                self.signInLabel.setText(authentication_status)
                # Re-enable UI elements
                self.loginButton.setEnabled(True)
                self.registerButton.setEnabled(True)

        else:
            # Update UI with connectivity result
            self.signInLabel.setText(connectivity_result)
            self.loginButton.setEnabled(True)
            self.registerButton.setEnabled(True)

    def open_register_window(self):
        """Method to open the register window."""
        self.register_window = RegisterWindow(self)
        self.register_window.show()

    def open_home_window(self):
        """Method to open the home window."""
        self.home_window = HomeWindow(activeUserInstance=self.activeUserInstance)
        self.home_window.show()
        # close login window
        self.close()

