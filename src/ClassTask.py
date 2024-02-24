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
    is_removed = Column(Integer, default=0)

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
                    .options(joinedload(Task.project))
                    .filter(User.username == team_member_username, Task.is_removed == 0)
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
                    .filter(Project.is_removed == 0, Task.is_removed == 0)
                )
                # If project is specified, filter tasks based on the project
                if projectPkey:
                    query = query.filter(Project.project_pkey == projectPkey)

                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'


    def get_task(self, session, taskPkey):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                query = (
                    session.query(Task)
                    .join(User, Task.assignee_fkey == User.user_pkey)
                    .join(Project, Task.project_fkey == Project.project_pkey)
                    .options(joinedload(Task.assignee), joinedload(Task.assigner), joinedload(Task.project))
                    .filter(Project.is_removed == 0, Task.is_removed == 0, Task.task_pkey == taskPkey)
                )
                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    def set_task(self, session, taskPkey, setName, setDesc, setStatus, setStartDate, setDueDate, assigneeFkey):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                task = session.query(Task).filter_by(task_pkey=taskPkey).first()
                if task is None:
                    return 'Project does not exist'

                else:
                    task.name = setName
                    task.desc = setDesc
                    task.status = setStatus
                    task.start_date = setStartDate
                    task.due_date = setDueDate
                    task.assignee_fkey = assigneeFkey
                    session.commit()
                return 'Project updated'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error setting data: {e}'

    def delete_task(self, session, taskPkey):
        try:
            # Create a session
            with session() as session:
                task = session.query(Task).filter_by(task_pkey=taskPkey).first()
                if task:
                    task.is_removed = 1
                    session.commit()
                    return 'Task deleted successfully'
                else:
                    return 'Task not found'
        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error deleting project: {e}'


    def close_task(self, session, taskPkey):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                task = session.query(Task).filter_by(task_pkey=taskPkey).first()
                if task is None:
                    return 'Task does not exist'
                else:
                    task.status = 'Completed'
                    task.end_date = datetime.utcnow()
                    session.commit()
                return 'Task Closed'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error closing project: {e}'

    def add_task(self, session):

        # check if fields are null
        dictToCheck = {"Project FKEY": self.project_fkey,
                       "Task Name": self.name,
                       "Task Description": self.desc,
                       "Task Status": self.status,
                       "Task Stat Date": self.start_date,
                       "Task Due Date": self.due_date,
                       "Assignee": self.assignee_fkey,
                       "Assigner": self.assigner_fkey}

        for attribute, val in dictToCheck.items():
            if val == '':
                return f'the field {attribute} can not be empty'

        else:
            # Try to establish connection to db
            try:
                # Create a session
                with session() as session:
                    # query db for the task
                    projectTask = (
                        session.query(Project)
                        .options(joinedload(Project.tasks))
                        .filter(
                            Project.project_pkey == self.project_fkey,
                            Project.is_removed == 0,
                            Task.is_removed == 0,
                            Task.name == self.name
                        )
                        .join(Task)
                        .first()
                    )
                    # if the task of project already exists in the database
                    if projectTask:
                        return f'Error!, the task: {self.name} already exists'
                    # if project is not in the database
                    if projectTask is None:
                        session.add(self)
                        session.commit()
                        return 'successful'
            except SQLAlchemyError as e:
                # Log or handle the exception
                return f'Error during adding project: {e}'

