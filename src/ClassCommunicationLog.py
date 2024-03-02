from src.ClassBase import Base
from src.ClassProject import Project
from src.ClassTask import Task
from src.ClassUser import User
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from datetime import datetime

from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.exc import SQLAlchemyError

class CommunicationLog(Base):
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


    @classmethod
    def get_project_communication_log(cls, session, project_fkey):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
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


    def add_comment(self, session):
        # check if fields are null
        if self.comment == '':
            return f'the field comment can not be empty'
        else:
            try:
                # Create a session
                with session() as session:
                    session.add(self)
                    session.commit()
                    return 'successful'
            except SQLAlchemyError as e:
                # Log or handle the exception
                return f'Error during adding comment: {e}'


    @classmethod
    def get_task_communication_log(cls, session, task_fkey):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
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
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                query = (
                    session.query(cls)
                    .join(cls.project)
                    .join(cls.task)
                    .join(cls.user)
                    .options(joinedload(cls.project))
                    .options(joinedload(cls.user))
                    .filter(User.user_pkey == user_fkey)
                )

            return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'