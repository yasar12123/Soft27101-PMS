from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QTimer, pyqtSignal
from generated.RegisterWindow import Ui_RegisterWindow
from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from src.ClassUserRole import UserRole
import threading


class RegisterWindow(QMainWindow, Ui_RegisterWindow):
    """Register window class.
    :param loginInstance: Instance of the login window
    :type loginInstance: LoginWindow
    :return: None
          attributes:
        - registration_completed: Signal emitted when registration is completed
        - setupUi: Method to set-up the UI
        - loginInstance: Instance of the login window
        - remaining_time: Initial remaining time in seconds
        - dbCon: DatabaseConnection instance
        - session: Database session
        signals:
        - registration_completed: Signal emitted when registration is completed
        - acceptRadioButton.toggled: Signal emitted when the accept radio button is toggled
        - registerButton.clicked: Signal emitted when the register button is clicked
        methods:
        - __init__: Constructor method
        - toggle_register_button: Toggle the register button based on the state of the accept radio button
        - start_registration_thread: Start the registration thread
        - on_registration: Register the user
        - disable_fields: Disable the input fields and buttons in the window
        - close_window: Close the window after a certain time
    """

    # Signals for the window class to emit when registration is completed
    registration_completed = pyqtSignal()

    def __init__(self, loginInstance=None):
        """Constructor method
        :param loginInstance: Instance of the login window
        :type loginInstance: LoginWindow
        :return: None
        """
        super().__init__()
        self.setupUi(self)
        self.loginInstance = loginInstance
        self.remaining_time = 5  # Initial remaining time in seconds

        # database connection
        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()

        # Connect signals to functions
        self.AcceptRadioButton.toggled.connect(self.toggle_register_button)
        self.RegisterButton.clicked.connect(self.start_registration_thread)
        # Connect registration_completed signal to close_window slot
        self.registration_completed.connect(self.close_window)

    def toggle_register_button(self, state):
        """Toggle the register button based on the state of the accept radio button.
        :param state: State of the accept radio button
        :type state: bool
        :return: None"""
        if state:
            self.RegisterButton.setEnabled(True)
        else:
            self.RegisterButton.setEnabled(False)

    def start_registration_thread(self):
        """Start the registration thread.
        :return: None"""

        # Start a new thread for registration
        registration_thread = threading.Thread(target=self.on_registration)
        registration_thread.start()

    def on_registration(self):
        """Register the user.
        :return: None"""

        # get input from window
        fullname = self.FullnameLE.text()
        email = self.EmailLE.text()
        username = self.UsernameLE.text()
        password = self.PasswordLE.text()

        # Test database connectivity
        self.RegistrationLabel.setText('Testing database connectivity')
        connectivity_result = self.dbCon.test_connectivity()

        if connectivity_result == 'Connection Established':
            # update the label to show the user that registration is in progress
            self.RegistrationLabel.setText('Please wait while we register you')

            # Create a new user instance
            new_user = User(username=username, password_hashed=password, email_address=email, full_name=fullname)
            # register user
            register_user = new_user.register_user(self.session)

            # update the label to show the user the result of the registration
            if register_user == 'Registration Successful':
                self.disable_fields()

                # add user role as standard user
                user_pkey = User().get_user_fkey(self.session, username)
                add_user_role = UserRole().add_user_role(self.session, user_pkey, 'StandardUser')

                # Once registration is completed, emit the registration_completed signal
                self.registration_completed.emit()

            # If the registration fails, display the error message
            else:
                self.RegistrationLabel.setText(register_user)
        else:
            self.RegistrationLabel.setText(connectivity_result)

    def disable_fields(self):
        """Disable the input fields and buttons in the window.
        :return: None"""
        self.FullnameLE.setEnabled(False)
        self.EmailLE.setEnabled(False)
        self.UsernameLE.setEnabled(False)
        self.PasswordLE.setEnabled(False)
        self.AcceptRadioButton.setEnabled(False)
        self.NotAcceptRadioButton.setEnabled(False)
        self.TermsAndCondTE.setEnabled(False)
        self.RegisterButton.setEnabled(False)

    def close_window(self):
        """Close the window after a certain time.
        :return: None"""
        self.remaining_time -= 1
        if self.remaining_time == 0:
            self.close()
        else:
            self.RegistrationLabel.setText(f'You are now registered, please close this window and sign in. '
                                           f'This window will close in {self.remaining_time} seconds.')
            QTimer.singleShot(1000, self.close_window)

