from src.ClassBase import Base
from src.ClassUserRole import UserRole
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError



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

    def authenticate(self, session, username, password):
        # Hash the password
        hashed_password = self.hash_password(password)

        # Try to establish connection to db
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

    def register(self, session):

        # check if fields are null
        dictToCheck = {"Fullname": self.full_name,
                       "Email": self.email_address,
                       "Username": self.username,
                       "Password": self.password_hashed}

        for attribute, val in dictToCheck.items():
            if val == '':
                return f'the field {attribute} can not be empty'

        else:
            # Try to establish connection to db
            try:
                # Create a session
                with session() as session:
                    # query db for the user
                    user = session.query(User).filter_by(username=self.username).first()
                    # if the user already exists in the database
                    if user:
                        return f'Error!, the username: {self.username} already exists'
                    # if username is not in the database
                    if user is None:
                        session.add(self)
                        session.commit()
                        return 'Registration Successful'
            except SQLAlchemyError as e:
                # Log or handle the exception
                return f'Error during registration: {e}'


    def get_user_fkey(self, session, usernameP):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                # query db for the user
                user = session.query(User).filter_by(username=usernameP).first()
                return user.user_pkey

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error connecting: {e}'


    def get_user(self, session, userName):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                query = (
                    session.query(User)
                    .join(User.user_roles)
                    .filter(User.username == userName)
                    .filter(User.user_pkey != -1)
                    .filter(UserRole.is_active == 1)
                    .options(joinedload(User.user_roles))
                )
                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    def get_users(self, session):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                query = (
                    session.query(User)
                    .join(User.user_roles)
                    .filter(UserRole.is_active == 1)
                    .filter(User.user_pkey != -1)
                    .options(joinedload(User.user_roles))
                )
                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

class UserAdmin(User):
    __tablename__ = 'USER_ADMIN'

    user_admin_pkey = Column(Integer, ForeignKey('USER.user_pkey'), primary_key=True)

class UserProjectOwner(User):
    __tablename__ = 'USER_PROJECT_OWNER'

    user_project_owner_pkey = Column(Integer, ForeignKey('USER.user_pkey'), primary_key=True)


