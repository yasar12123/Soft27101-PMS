import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment
from src.ClassEmail import EmailSender


# Define a fixture to set up a database connection and session
@pytest.fixture(scope="module")
def db_session():
    dbCon = DatabaseConnection()
    return dbCon.get_session()

def user_to_test():
    user = User(username='test_user', full_name='Test User', email_address='test@example.com',
                password_hashed='password')
    return user
def test_register_user(db_session):
    # Arrange
    user = user_to_test()

    # Act
    result = user.register_user(db_session)

    # Assert
    assert result == 'Registration Successful'


def test_authenticate_user(db_session):

    # Act
    message, authenticated_user = User.authenticate_user(db_session, 'test_user', 'password')

    # Assert
    assert message == 'Login Successful'
    assert authenticated_user.username == 'test_user'


def test_set_user(db_session):
    # get user instance
    user = user_to_test()
    user_fkey = User.get_user_fkey(db_session, user.username)
    user = User.get_user_instance(db_session, user_fkey)

    # Act
    result = user.set_user(db_session, user.user_pkey, setFullname='Updated Name', setEmailAddress='updated@example.com')

    # Assert
    assert result == 'User details updated'
    updated_user = User.get_user_instance(db_session, user.user_pkey)
    assert updated_user.full_name == 'Updated Name'
    assert updated_user.email_address == 'updated@example.com'


def test_delete_user(db_session):
    # get user instance
    user = user_to_test()
    user_fkey = User.get_user_fkey(db_session, user.username)
    user = User.get_user_instance(db_session, user_fkey)

    # Act
    result = user.delete_user(db_session, user.user_pkey)

    # Assert
    assert result == 'User has been deleted'
    assert User.get_user_instance(db_session, user.user_pkey) is None
