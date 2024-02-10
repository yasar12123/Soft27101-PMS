
from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from src.ClassUser import User
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTeam import Team
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment


# input from window
fullname = 'test user'
email = 'test@mail.com'
username = 'test12'
password = '12345'

# db session
dbCon = DatabaseConnection()
session = dbCon.get_session()
# Create a new user instance
new_user = User(username=username, password_hashed=password, email_address=email, full_name=fullname)
new_user.register(session)
