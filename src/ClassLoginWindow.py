from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTeam import Team
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow
from generated.LoginWindow import Ui_LoginWindow
from src.ClassRegisterWindow import RegisterWindow
from src.ClassHomeWindow import HomeWindow


class ConnectionThread(QThread):
    connection_status = pyqtSignal(str)

    def __init__(self, db_con):
        super().__init__()
        self.db_con = db_con

    def run(self):
        try:
            # Test database connectivity
            self.db_con.test_connectivity()
            self.connection_status.emit('Connection Established')
        except RuntimeError as e:
            # Emit error signal if an exception occurs
            self.connection_status.emit(str(e))


class AuthThread(QThread):
    authentication_done = pyqtSignal(str, object)

    def __init__(self, user, session, username, password):
        super().__init__()
        self.user = user
        self.session = session
        self.username = username
        self.password = password

    def run(self):
        try:
            # Authenticate user
            user_authentication, user_instance = self.user.authenticate_user(self.session, self.username, self.password)
            self.authentication_done.emit(user_authentication, user_instance)
        except RuntimeError as e:
            # Emit error signal if an exception occurs
            self.authentication_done.emit(str(e), None)



class LoginWindow(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.activeUserInstance = None

        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()

        # Connect signals to slots
        self.loginButton.clicked.connect(self.on_login)
        self.registerButton.clicked.connect(self.open_register_window)

    def on_login(self):
        #change label
        self.signInLabel.setText(f'Please wait, trying to log you in.')

        # Create connection thread and run
        self.connection_thread = ConnectionThread(self.dbCon)
        self.connection_thread.connection_status.connect(self.handle_connection_result)
        self.connection_thread.start()

    def handle_connection_result(self, connection_status):
        if connection_status == 'Connection Established':
            # Input from window
            username = self.usernameLE.text()
            password = self.passwordLE.text()
            # Start authentication thread
            self.auth_thread = AuthThread(User(), self.session, username, password)
            self.auth_thread.authentication_done.connect(self.handle_authentication_result)
            self.auth_thread.start()
        else:
            self.signInLabel.setText(connection_status)

    def handle_authentication_result(self, authentication_status, user_instance):
        if authentication_status == 'Login Successful':
            self.signInLabel.setText(f'Welcome, {user_instance.username}! You have now logged in.')
            self.activeUserInstance = user_instance
            self.open_home_window()
            self.close()
        else:
            self.signInLabel.setText(authentication_status)

    def open_register_window(self):
        self.register_window = RegisterWindow(self)
        self.register_window.show()

    def open_home_window(self):
        self.home_window = HomeWindow(activeUserInstance=self.activeUserInstance)
        self.home_window.show()