from src.ClassBase import Base
from src.ClassProject import Project
from src.ClassTask import Task
from src.ClassUser import User

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from datetime import datetime
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.exc import SQLAlchemyError


class CommunicationLog(Base):
    """
    Class to represent the communication log table

    Attributes:
        communication_log_pkey: primary key
        user_fkey: foreign key to the user table
        project_fkey: foreign key to the project table
        task_fkey: foreign key to the task table
        comment: text field for the comment
        timestamp: timestamp for the comment
        user: relationship to the user table
        project: relationship to the project table
        task: relationship to the task table
        attachments: relationship to the attachment table

    Methods:
        get_project_communication_log: get all communication logs for a project
        add_comment: add a new comment to the database
        get_task_communication_log: get all communication logs for a task
        get_user_communication_log: get all communication logs by a user
    """
    __tablename__ = 'COMMUNICATION_LOG'

    communication_log_pkey = Column(Integer, primary_key=True, autoincrement=True)
    user_fkey = Column(Integer, ForeignKey('USER.user_pkey'), nullable=False)
    project_fkey = Column(Integer, ForeignKey('PROJECT.project_pkey'), nullable=False)
    task_fkey = Column(Integer, ForeignKey('TASK.task_pkey'), nullable=False)
    comment = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Define relationships
    user = relationship('User', back_populates='communication_log')
    project = relationship('Project', back_populates='communication_log')
    task = relationship('Task', back_populates='communication_log')
    attachments = relationship('Attachment', back_populates='communication_log')

    def add_comment(self, session):
        """
        Add a new comment to the database
        :param session: session object
        :type session: sqlalchemy.orm.session.Session
        :return: success message or error message
        :rtype: str
        """

        # check if fields are null
        if self.comment == '':
            return f'the field comment can not be empty'

        else:
            try:
                with session() as session:
                    # Add the new comment to the database
                    session.add(self)
                    session.commit()
                    return 'successful'

            except SQLAlchemyError as e:
                # Log or handle the exception
                return f'Error during adding comment: {e}'

    @classmethod
    def get_project_communication_log(cls, session, project_fkey):
        """
        Get all communication logs for a project
        :param session: session object
        :type session: sqlalchemy.orm.session.Session
        :param project_fkey: project primary key
        :type project_fkey: int
        :return: list of communication logs for a project
        :rtype: list
        """
        try:
            with session() as session:
                # query for all communication logs in a project
                query = (
                    session.query(cls)
                    .join(cls.project)
                    .join(cls.user)
                    .options(joinedload(cls.project))
                    .options(joinedload(cls.user))
                    .filter(Project.project_pkey == project_fkey)
                )
            return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    @classmethod
    def get_task_communication_log(cls, session, task_fkey):
        """
        Get all communication logs for a task
        :param session: session object
        :type session: sqlalchemy.orm.session.Session
        :param task_fkey: task primary key
        :type task_fkey: int
        :return: list of communication logs for a task
        :rtype: list
        """
        try:
            with session() as session:
                # query for all communication logs in a task
                query = (
                    session.query(cls)
                    .join(cls.project)
                    .join(cls.task)
                    .join(cls.user)
                    .options(joinedload(cls.project))
                    .options(joinedload(cls.user))
                    .filter(Task.task_pkey == task_fkey)
                )
            return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    @classmethod
    def get_user_communication_log(cls, session, user_fkey):
        """
        Get all communication logs for a user
        :param session: session object
        :type session: sqlalchemy.orm.session.Session
        :param user_fkey: user primary key
        :type user_fkey: int
        :return: list of communication logs by a user
        :rtype: list
        """

        try:
            with session() as session:
                # query for all communication logs by a user
                query = (
                    session.query(cls)
                    .join(cls.project)
                    .join(cls.task)
                    .join(cls.user)
                    .options(joinedload(cls.project))
                    .options(joinedload(cls.user))
                    .filter(User.user_pkey == user_fkey))

            return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

