from src.ClassBase import Base
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTeam import Team
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from src.ClassDatabaseConnection import DatabaseConnection
from sqlalchemy.orm import sessionmaker

class User(Base):
    __tablename__ = 'USER'

    user_pkey = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    full_name = Column(String(100), nullable=False)
    email_address = Column(String(100), nullable=False)
    password_hashed = Column(String(255), nullable=False)
    date_registered = Column(DateTime, default=datetime.utcnow)

    # Define the relationships
    owner_of_projects = relationship('Project', back_populates='owner')
    team_associations = relationship('ProjectTeam', back_populates='user')
    assigned_tasks = relationship('Task', back_populates='assignee', foreign_keys='Task.assignee_fkey')
    assigner_of_tasks = relationship('Task', back_populates='assigner', foreign_keys='Task.assigner_fkey')
    user_roles = relationship('UserRole', back_populates='user')
    communication_log = relationship('CommunicationLog', back_populates='user')

    def hash_password(self, password):
        # Implement a secure hash function (e.g., bcrypt, Argon2)
        # Return the hashed password
        hashed_password = password
        return hashed_password

    def authenticate(self, username, password):
        # Hash the provided password
        hashed_password = self.hash_password(password)

        # Create session to db
        db = DatabaseConnection()
        engine = db.get_engine()
        session = sessionmaker(bind=engine)


        #try to establish connection to db
        try:
            # Create a session
            with session() as session:
                # query db for the user
                user = session.query(User).filter_by(username=username).first()

                # if user does not exist
                if user is None:
                    return f'The Username: {username} does not exist'
                # if user exist but password does not match
                if user and user.password_hashed != hashed_password:
                    return 'Incorrect Password'
                # if user exists and password matches
                if user and user.password_hashed == hashed_password:
                    return 'Login Successful'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error during authentication: {e}'




class UserAdmin(User):
    __tablename__ = 'USER_ADMIN'

    user_admin_pkey = Column(Integer, ForeignKey('USER.user_pkey'), primary_key=True)

class UserProjectOwner(User):
    __tablename__ = 'USER_PROJECT_OWNER'

    user_project_owner_pkey = Column(Integer, ForeignKey('USER.user_pkey'), primary_key=True)


