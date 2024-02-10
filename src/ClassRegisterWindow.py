from PyQt6.QtWidgets import QMainWindow
from generated.RegisterWindow import Ui_RegisterWindow
from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTeam import Team
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment


class RegisterWindow(QMainWindow, Ui_RegisterWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect signals to slots
        self.AcceptRadioButton.toggled.connect(self.toggle_register_button)
        self.RegisterButton.clicked.connect(self.on_registration)

    def toggle_register_button(self, state):
        if state: # radio is checked
            self.RegisterButton.setEnabled(True)
        else:
            self.RegisterButton.setEnabled(False)

    def on_registration(self):
        # input from window
        fullname = self.FullnameLE.text()
        email = self.EmailLE.text()
        username = self.UsernameLE.text()
        password = self.PasswordLE.text()

        # db session
        dbCon = DatabaseConnection()
        session = dbCon.get_session()

        # Create a new user instance
        new_user = User(username=username, password_hashed=password, email_address=email, full_name=fullname)
        # register user
        registerUser = new_user.register(session)
        if registerUser == 'Registration Successful':
            self.RegistrationLabel.setText(f'Welcome, {username}! You are now registered.')
        else:
            self.RegistrationLabel.setText(registerUser)


