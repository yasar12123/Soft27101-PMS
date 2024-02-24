from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTeam import Team
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment

from PyQt6.QtWidgets import QApplication, QMainWindow
from generated.LoginWindow import Ui_LoginWindow
from src.ClassRegisterWindow import RegisterWindow
from src.ClassHomeWindow import HomeWindow


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
        # input from window
        username = self.usernameLE.text()
        password = self.passwordLE.text()

        # Class user to query
        user = User()
        # authenticate user
        userAuthentication, userInstance = user.authenticate(self.session, username, password)

        if userAuthentication == 'Login Successful':
            self.signInLabel.setText(f'Welcome, {username}! You have now logged in.')
            self.activeUserInstance = userInstance
            self.open_home_window()
            self.close()

        else:
            self.signInLabel.setText(userAuthentication)

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

    def open_home_window(self):
        self.home_window = HomeWindow(activeUserInstance=self.activeUserInstance)
        self.home_window.show()



