from src.ClassBase import Base
from src.ClassUser import User
from src.ClassProject import Project
from sqlalchemy.orm import relationship, joinedload, aliased
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class Task(Base):
    __tablename__ = 'TASK'  # Adjusted table name

    task_pkey = Column(Integer, primary_key=True, autoincrement=True)
    project_fkey = Column(Integer, ForeignKey('PROJECT.project_pkey'), nullable=False)
    name = Column(String(255), nullable=False)
    desc = Column(String, nullable=False)
    status = Column(String(100), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime)
    due_date = Column(DateTime)
    assignee_fkey = Column(Integer, ForeignKey('USER.user_pkey'), nullable=False)
    assigner_fkey = Column(Integer, ForeignKey('USER.user_pkey'), nullable=False)

    # Define the relationships
    project = relationship('Project', back_populates='tasks')
    assignee = relationship('User', back_populates='assigned_tasks', foreign_keys=[assignee_fkey])
    assigner = relationship('User', back_populates='assigner_of_tasks', foreign_keys=[assigner_fkey])
    communication_log = relationship('CommunicationLog', back_populates='task')


    def get_tasks_for_team_member(self, session, team_member_username, projectPkey=None):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                query = (
                    session.query(Task)
                    .join(User, Task.assignee_fkey == User.user_pkey)
                    .join(Project, Task.project_fkey == Project.project_pkey)
                    .filter(User.username == team_member_username)
                )
                # If project is specified, filter tasks based on the project
                if projectPkey:
                    query = query.filter(Project.project_pkey == projectPkey)

                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'


    def get_tasks(self, session, projectPkey=None):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                query = (
                    session.query(Task)
                    .join(User, Task.assignee_fkey == User.user_pkey)
                    .join(Project, Task.project_fkey == Project.project_pkey)
                    .options(joinedload(Task.assignee), joinedload(Task.assigner), joinedload(Task.project))
                    .filter(Project.is_removed == 0)
                )
                # If project is specified, filter tasks based on the project
                if projectPkey:
                    query = query.filter(Project.project_pkey == projectPkey)

                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

