from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from generated.LoginWindow import Ui_LoginWindow
from src.ClassRegisterWindow import RegisterWindow
from src.ClassHomeWindow import HomeWindow


class ConnectionThread(QThread):
    """Thread to test database connectivity.
    Emits a signal with the result of the connection test.
    :param db_con: DatabaseConnection instance
    :type db_con: DatabaseConnection
    :return: None
    """
    connection_status = pyqtSignal(str)

    def __init__(self, db_con):
        """Constructor method"""
        super().__init__()
        self.db_con = db_con

    def run(self):
        """Run method for the thread to test database connectivity"""
        try:
            # Test database connectivity
            self.db_con.test_connectivity()
            self.connection_status.emit('Connection Established')
        except RuntimeError as e:
            # Emit error signal if an exception occurs
            self.connection_status.emit(str(e))


class AuthThread(QThread):
    """Thread to authenticate a user.
    Emits a signal with the result of the authentication.
    :param user: User instance
    :type user: User
    :param session: Database session
    :type session: sqlalchemy.orm.session.Session
    :param username: Username
    :type username: str
    :param password: Password
    :type password: str
    :return: None
    """
    authentication_done = pyqtSignal(str, object)

    def __init__(self, user, session, username, password):
        """Constructor method"""
        super().__init__()
        self.user = user
        self.session = session
        self.username = username
        self.password = password

    def run(self):
        """Run method for the thread to authenticate a user"""
        try:
            # Authenticate user
            user_authentication, user_instance = self.user.authenticate_user(self.session, self.username, self.password)
            self.authentication_done.emit(user_authentication, user_instance)
        except RuntimeError as e:
            # Emit error signal if an exception occurs
            self.authentication_done.emit(str(e), None)



class LoginWindow(QMainWindow, Ui_LoginWindow):
    """Class for the login window.
    Inherits from QMainWindow and Ui_LoginWindow.
    :param QMainWindow: Inherited from QMainWindow
    :param Ui_LoginWindow: Inherited from Ui_LoginWindow
    :return: None
    """

    def __init__(self):
        """Constructor method"""
        super().__init__()
        self.setupUi(self)
        self.activeUserInstance = None

        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()

        # Connect signals to slots
        self.loginButton.clicked.connect(self.on_login)
        self.registerButton.clicked.connect(self.open_register_window)

    def on_login(self):
        """Method to handle the login process."""
        # Set label to show that the user is being logged in
        self.signInLabel.setText(f'Please wait, trying to log you in.')

        # Start a new thread for database connectivity
        self.connection_thread = ConnectionThread(self.dbCon)
        self.connection_thread.connection_status.connect(self.handle_connection_result)
        self.connection_thread.start()

    def handle_connection_result(self, connection_status):
        """Method to handle the result of the database connectivity test.
        :param connection_status: Result of the database connectivity test
        :type connection_status: str
        :return: None"""

        # If the connection is established, proceed with the authentication process
        if connection_status == 'Connection Established':
            # Input from window
            username = self.usernameLE.text()
            password = self.passwordLE.text()
            # Start a new thread for authentication
            self.auth_thread = AuthThread(User(), self.session, username, password)
            self.auth_thread.authentication_done.connect(self.handle_authentication_result)
            self.auth_thread.start()
        # If the connection fails, display the error message
        else:
            self.signInLabel.setText(connection_status)

    def handle_authentication_result(self, authentication_status, user_instance):
        """Method to handle the result of the user authentication.
        :param authentication_status: Result of the user authentication
        :type authentication_status: str
        :param user_instance: User instance
        :type user_instance: User
        :return: None"""
        # If the authentication is successful, display a welcome message and open the home window
        if authentication_status == 'Login Successful':
            self.signInLabel.setText(f'Welcome, {user_instance.username}! You have now logged in.')
            self.activeUserInstance = user_instance
            self.open_home_window()
            self.close()
        # If the authentication fails, display the error message
        else:
            self.signInLabel.setText(authentication_status)

    def open_register_window(self):
        """Method to open the register window."""
        self.register_window = RegisterWindow(self)
        self.register_window.show()

    def open_home_window(self):
        """Method to open the home window."""
        self.home_window = HomeWindow(activeUserInstance=self.activeUserInstance)
        self.home_window.show()

