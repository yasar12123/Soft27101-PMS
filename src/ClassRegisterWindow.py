from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QTimer
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
import threading


class RegisterWindow(QMainWindow, Ui_RegisterWindow):
    def __init__(self, loginInstance=None):
        super().__init__()
        self.setupUi(self)
        self.loginInstance = loginInstance
        self.remaining_time = 5  # Initial remaining time in seconds

        # database connection
        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()

        # Connect signals to slots
        self.AcceptRadioButton.toggled.connect(self.toggle_register_button)
        self.RegisterButton.clicked.connect(self.start_registration_thread)

    def toggle_register_button(self, state):
        if state:
            self.RegisterButton.setEnabled(True)
        else:
            self.RegisterButton.setEnabled(False)

    def start_registration_thread(self):
        self.RegistrationLabel.setText('Please wait while we register you')
        # Start a new thread for registration
        registration_thread = threading.Thread(target=self.on_registration)
        registration_thread.start()

    def on_registration(self):
        # get input from window
        fullname = self.FullnameLE.text()
        email = self.EmailLE.text()
        username = self.UsernameLE.text()
        password = self.PasswordLE.text()

        # Create a new user instance
        new_user = User(username=username, password_hashed=password, email_address=email, full_name=fullname)
        # register user
        registerUser = new_user.register_user(self.session)

        if registerUser == 'Registration Successful':
            self.RegistrationLabel.setText(f'You are now registered, please close this window and sign in.')
            self.disable_fields()
            self.after_registration()

            # add user role as standard user
            user_pkey = User().get_user_fkey(self.session, username)
            user_role = UserRole()
            add_user_role = user_role.add_user_role(self.session, user_pkey, 'StandardUser')
        else:
            self.RegistrationLabel.setText(registerUser)

    def after_registration(self):
        # Start a timer to update the remaining time every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_remaining_time)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

    def update_remaining_time(self):
        self.remaining_time -= 1
        self.RegistrationLabel.signInLabel.setText(
            f'You are now registered, Please close this window and sign in. '
            f'\nClosing in {self.remaining_time} seconds')

        if self.remaining_time <= 0:
            # Close the window after 5 seconds
            self.timer.stop()
            self.close()

    def disable_fields(self):
        self.FullnameLE.setEnabled(False)
        self.EmailLE.setEnabled(False)
        self.UsernameLE.setEnabled(False)
        self.PasswordLE.setEnabled(False)
        self.AcceptRadioButton.setEnabled(False)
        self.RegisterButton.setEnabled(False)
