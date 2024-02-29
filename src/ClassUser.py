from src.ClassBase import Base
from src.ClassUserRole import UserRole
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import bcrypt



class User(Base):
    __tablename__ = 'USER'

    user_pkey = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    full_name = Column(String(100), nullable=False)
    email_address = Column(String(100), nullable=False)
    password_hashed = Column(String(255), nullable=False)
    date_registered = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1, nullable=False)

    # Define the relationships
    owner_of_projects = relationship('Project', back_populates='owner')
    team_associations = relationship('ProjectTeam', back_populates='user')
    assigned_tasks = relationship('Task', back_populates='assignee', foreign_keys='Task.assignee_fkey')
    assigner_of_tasks = relationship('Task', back_populates='assigner', foreign_keys='Task.assigner_fkey')
    user_roles = relationship('UserRole', back_populates='user')
    communication_log = relationship('CommunicationLog', back_populates='user')
    timeline_events = relationship("TimelineEvent", back_populates="user")

    @staticmethod
    def hash_password(password):
        # Generate a salt and hash the password using bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Return the hashed password as a string
        return hashed_password.decode('utf-8')


    def verify_password(self, password_to_verify):
        # Verify the input password against the hashed password
        verify = bcrypt.checkpw(password_to_verify.encode('utf-8'),
                                self.password_hashed.encode('utf-8'))
        return verify

    @staticmethod
    def authenticate_user(session, username, password):

        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                # query db for the user
                user = session.query(User).filter_by(username=username).first()

                # if user does not exist
                if user is None:
                    return f'The Username: {username} does not exist', None

                verify_password = user.verify_password(password)
                # if user exist but password does not match
                if verify_password is False:
                    return 'Incorrect Password', None

                # if user exists and password matches
                if verify_password is True:
                    return 'Login Successful', user

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error during authentication: {e}', None


    def register_user(self, session):
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

                    # if username is not in the database then add the user
                    if user is None:
                        # hash the password
                        self.password_hashed = self.hash_password(self.password_hashed)
                        # add user to db
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

    def get_user_instance(self, session, user_pkey):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                # query db for the user
                user = session.query(User).filter_by(user_pkey=user_pkey).first()
                return user

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error connecting: {e}'

    @classmethod
    def set_user(cls, session, user_pkey, setUsername, setFullname, setEmailAddress, setPassword=None):
        try:
            # get a list with all users
            users_list = cls.get_users(cls, session)

            # check if username has been taken already
            for userN in users_list:
                if userN.username == setUsername:
                    return f'Username: {setUsername} has already been taken \n Please Try Another'

            with session() as session:
                # check if user exists
                user = session.query(cls).filter_by(user_pkey=user_pkey).first()

                # if user not in db then return message
                if user is None:
                    return 'User does not exist'

                # else update details
                else:
                    if setUsername:
                        user.username = setUsername
                    if setFullname:
                        user.full_name = setFullname
                    if setEmailAddress:
                        user.email_address = setEmailAddress
                    if setPassword:
                        user.password_hashed = setPassword

                    # commit changes
                    session.commit()

                return 'User details updated'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error setting data: {e}'



    def is_user_admin(self, session, user_pkey):
        try:
            with session() as session:
                userRole = (session.query(UserRole).filter(UserRole.is_active == 1,
                                                           UserRole.role_type == 'Admin',
                                                           UserRole.user_fkey == user_pkey).first())
                if userRole:
                    return True
                else:
                    return False

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'


    def delete_user(self, session, user_to_delete_pkey):
        is_admin = self.is_user_admin(session, self.user_pkey)

        # Check if user is an admin or the user to be deleted is the same as the user performing the deletion
        if is_admin or user_to_delete_pkey == self.user_pkey:
            try:
                with session() as session:
                    # query db for the user
                    session.query(User).filter(User.user_pkey == user_to_delete_pkey).delete()
                    session.commit()
                    return 'User has been deleted, You will be logged out shortly.'

            except SQLAlchemyError as e:
                # Log or handle the exception
                return f'Error deleting user: {e}'
        else:
            return 'You do not have the permission to delete this user'










class UserAdmin(User):
    __tablename__ = 'USER_ADMIN'

    user_admin_pkey = Column(Integer, ForeignKey('USER.user_pkey'), primary_key=True)

class UserProjectOwner(User):
    __tablename__ = 'USER_PROJECT_OWNER'

    user_project_owner_pkey = Column(Integer, ForeignKey('USER.user_pkey'), primary_key=True)


