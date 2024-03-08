from src.ClassBase import Base
from src.ClassUserRole import UserRole
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import bcrypt


class User(Base):
    """Class to represent the User table in the database.
    Attributes:
        user_pkey: Primary key for the user table
        username: Username of the user
        full_name: Full name of the user
        email_address: Email address of the user
        password_hashed: Hashed password of the user
        date_registered: Date the user was registered
        is_active: Flag indicating if the user is active or not
        owner_of_projects: Relationship to the Project table
        team_associations: Relationship to the ProjectTeam table
        assigned_tasks: Relationship to the Task table
        assigner_of_tasks: Relationship to the Task table
        user_roles: Relationship to the UserRole table
        communication_log: Relationship to the CommunicationLog table

    Methods:
        hash_password(password: str): Hash a password using bcrypt
        authenticate_user(session: Database session, username: str, password: str): Authenticate a user
        get_user_instance(session: Database session, user_pkey: int): Get a user instance from the database
        get_user_fkey(session: Database session, username: str): Get the user primary key
        get_users(session: Database session): Get all users from the database
        is_user_admin(session: Database session, user_pkey: int): Check if a user is an admin
        verify_password(password_to_verify: str): Verify a password against the hashed password
        register_user(session: Database session): Register a new user
        set_user(session: Database session, user_to_set_pkey: int, setFullname: str, setEmailAddress: str, setPassword: str): Set user details
        delete_user(session: Database session, user_to_delete_pkey: int): Delete a user from the database
        get_roles(session: Database session): Get the roles of a user
    """
    # Define the table name
    __tablename__ = 'USER'

    # Define the columns
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

    @staticmethod
    def hash_password(password):
        """Hash a password using bcrypt.
        :param password: Password to hash
        :type password: str
        :return: Hashed password as a string
        :rtype: str"""
        # Generate a salt and hash the password using bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Return the hashed password as a string
        return hashed_password.decode('utf-8')

    @staticmethod
    def authenticate_user(session, username, password):
        """Authenticate a user.
        :param session: Database session
        :type session: sqlalchemy.orm.session.Session
        :param username: Username
        :type username: str
        :param password: Password
        :type password: str
        :return: Tuple with a message and the (user instance - if successful) or (None - if unsuccessful)"""

        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                # query db for the user
                user = session.query(User).filter_by(username=username).first()

                # if user does not exist
                if user is None:
                    return f'The Username: {username} does not exist', None

                # if user exist but password does not match
                verify_password = user.verify_password(password)
                if verify_password is False:
                    return 'Incorrect Password', None

                # if user exists and password matches
                if verify_password is True:
                    return 'Login Successful', user

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error during authentication: {e}', None

    @staticmethod
    def get_user_instance(session, user_pkey):
        """Get a user instance from the database.
        :param session: Database session
        :type session: sqlalchemy.orm.session.Session
        :param user_pkey: User primary key
        :type user_pkey: int
        :return: User instance
        :rtype: User instance"""
        try:
            with session() as session:
                # query db for the user
                user = session.query(User).filter_by(user_pkey=user_pkey).first()
                return user

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error connecting: {e}'

    @staticmethod
    def get_user_fkey(session, username):
        """Get the user primary key.
        :param session: Database session
        :type session: sqlalchemy.orm.session.Session
        :param username: Username
        :type username: str
        :return: User primary key as an integer
        :rtype: int"""
        try:
            # Create a session
            with session() as session:
                # query db for the user
                user = session.query(User).filter_by(username=username).first()
                return user.user_pkey

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error connecting: {e}'

    @staticmethod
    def get_users(session):
        """Get all users from the database.
        :param session: Database session
        :type session: sqlalchemy.orm.session.Session
        :return: List of User instances
        :rtype: list of User instances"""
        try:
            with session() as session:
                query = (
                    session.query(User)
                    .join(User.user_roles)
                    .filter(UserRole.is_active == 1)
                    .filter(User.user_pkey != -1)
                    .options(joinedload(User.user_roles)))

                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    @staticmethod
    def is_user_admin(session, user_pkey):
        """Check if a user is an admin.
        :param session: Database session
        :type session: sqlalchemy.orm.session.Session
        :param user_pkey: User primary key
        :type user_pkey: int
        :return: True if the user is an admin, False otherwise
        :rtype: bool"""
        try:
            with session() as session:
                # query db for the user roles that are active and of type 'Admin'
                userRole = (session.query(UserRole)
                            .filter(UserRole.is_active == 1,
                                    UserRole.role_type == 'Admin',
                                    UserRole.user_fkey == user_pkey).first())
                if userRole:
                    return True
                else:
                    return False

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    def verify_password(self, password_to_verify):
        """Verify a password against the hashed password.
        :param password_to_verify: Password to verify
        :type password_to_verify: str
        :return: True if the password matches, False otherwise
        :rtype: bool"""
        # Verify the input password against the hashed password
        verify = bcrypt.checkpw(password_to_verify.encode('utf-8'),
                                self.password_hashed.encode('utf-8'))
        return verify

    def register_user(self, session):
        """Register a new user.
        :param session: Database session
        :type session: sqlalchemy.orm.session.Session
        :return: Message indicating the result of the registration attempt."""
        # check if fields are null
        dictToCheck = {"Fullname": self.full_name, "Email": self.email_address,
                       "Username": self.username, "Password": self.password_hashed}

        for attribute, val in dictToCheck.items():
            if val == '':
                return f'the field {attribute} can not be empty'

        else:
            try:
                # Create a session
                with session() as session:
                    # query db for the user
                    user = session.query(User).filter_by(username=self.username).first()

                    # if the user already exists in the database return message
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

    def set_user(self, session, user_to_set_pkey, setFullname, setEmailAddress, setPassword=None):
        """Set user details.
        :param session: Database session
        :type session: sqlalchemy.orm.session.Session
        :param user_to_set_pkey: User primary key
        :type user_to_set_pkey: int
        :param setFullname: Full name to set
        :type setFullname: str
        :param setEmailAddress: Email address to set
        :type setEmailAddress: str
        :param setPassword: Password to set
        :type setPassword: str
        :return: Message indicating the result of the update attempt."""
        # Check if user is an admin or the same as the user performing the update
        is_admin = self.is_user_admin(session, self.user_pkey)
        if is_admin or user_to_set_pkey == self.user_pkey:
            try:

                with session() as session:
                    # check if user exists
                    user = session.query(User).filter_by(user_pkey=user_to_set_pkey).first()

                    # if user not in db then return message
                    if user is None:
                        return 'User does not exist'

                    # else update details
                    else:
                        if setFullname:
                            user.full_name = setFullname
                        if setEmailAddress:
                            user.email_address = setEmailAddress
                        if setPassword:
                            user.password_hashed = self.hash_password(setPassword)

                        # commit changes
                        session.commit()

                    return 'User details updated'

            except SQLAlchemyError as e:
                # Log or handle the exception
                return f'Error setting data: {e}'
        else:
            return 'You do not have permissions to update this user'

    def delete_user(self, session, user_to_delete_pkey):
        """Delete a user from the database.
        :param session: Database session
        :type session: sqlalchemy.orm.session.Session
        :param user_to_delete_pkey: User primary key
        :type user_to_delete_pkey: int
        :return: Message indicating the result of the deletion attempt."""
        # Check if user is an admin or the user to be deleted is the same as the user performing the deletion
        is_admin = self.is_user_admin(session, self.user_pkey)
        if is_admin is True or user_to_delete_pkey == self.user_pkey:
            try:
                with session() as session:
                    # query db for the user and delete
                    session.query(User).filter(User.user_pkey == user_to_delete_pkey).delete()
                    session.commit()
                    return 'User has been deleted'

            except SQLAlchemyError as e:
                # Log or handle the exception
                return f'Error deleting user: {e}'
        else:
            return 'You do not have permissions to delete this user'

    def get_roles(self, session):
        try:
            # Create a session
            with session() as session:
                # Query the database to fetch user roles
                user_roles = session.query(UserRole).filter(UserRole.user_fkey == self.user_pkey).all()
                # Return the list of user roles
                return user_roles
        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error fetching user roles: {e}'


