from src.ClassBase import Base
from src.ClassUser import User
from src.ClassProject import Project
from sqlalchemy.orm import relationship, joinedload, aliased
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, or_
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
    task_progress = Column(Integer, default=0)
    is_removed = Column(Integer, default=0)

    # Define the relationships
    project = relationship('Project', back_populates='tasks')
    assignee = relationship('User', back_populates='assigned_tasks', foreign_keys=[assignee_fkey])
    assigner = relationship('User', back_populates='assigner_of_tasks', foreign_keys=[assigner_fkey])
    communication_log = relationship('CommunicationLog', back_populates='task')
    timeline_events = relationship("TimelineEvent", back_populates="task")


    @classmethod
    def get_tasks_for_team_member(cls, session, team_member_username, project_fkey=None):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                query = (
                    session.query(cls)
                    .join(User, cls.assignee_fkey == User.user_pkey)
                    .join(Project, cls.project_fkey == Project.project_pkey)
                    .options(joinedload(cls.project))
                    .filter(User.username == team_member_username, cls.is_removed == 0)
                )
                # If project is specified, filter tasks based on the project
                if project_fkey:
                    query = query.filter(Project.project_pkey == project_fkey)

                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    @classmethod
    def get_tasks(cls, session, project_fkey=None):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                query = (
                    session.query(cls)
                    .join(User, cls.assignee_fkey == User.user_pkey)
                    .join(Project, cls.project_fkey == Project.project_pkey)
                    .options(joinedload(cls.assignee), joinedload(cls.assigner), joinedload(cls.project))
                    .filter(Project.is_removed == 0, cls.is_removed == 0)
                )
                # If project is specified, filter tasks based on the project
                if project_fkey:
                    query = query.filter(Project.project_pkey == project_fkey)

                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    @classmethod
    def set_task(cls, session, task_pkey, setName=None, setDesc=None, setStatus=None,
                 setStartDate=None, setDueDate=None, assigneeFkey=None, assignerFkey = None, taskProgress=None):
        try:
            with session() as sess:
                task = sess.query(cls).filter_by(task_pkey=task_pkey).first()
                if task is None:
                    return 'Task does not exist'
                else:
                    if setName:
                        task.name = setName
                    if setDesc:
                        task.desc = setDesc
                    if setStatus:
                        task.status = setStatus
                    if setStartDate:
                        task.start_date = setStartDate
                    if setDueDate:
                        task.due_date = setDueDate
                    if assigneeFkey:
                        task.assignee_fkey = assigneeFkey
                    if assignerFkey:
                        task.assigner_fkey = assignerFkey
                    if taskProgress:
                        task.task_progress = taskProgress
                    sess.commit()
                return 'Task updated'
        except SQLAlchemyError as e:
            return f'Error setting data: {e}'

    @classmethod
    def delete_task(cls, session, task_pkey):
        try:
            # Create a session
            with session() as session:
                task = session.query(cls).filter_by(task_pkey=task_pkey).first()
                if task:
                    task.is_removed = 1
                    session.commit()
                    return 'Task deleted successfully'
                else:
                    return 'Task not found'
        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error deleting project: {e}'

    @classmethod
    def close_task(cls, session, task_pkey):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                task = session.query(cls).filter_by(task_pkey=task_pkey).first()
                if task is None:
                    return 'Task does not exist'
                if task.end_date:
                    return 'The task has already been closed'
                else:
                    task.status = 'Completed'
                    task.task_progress = 100
                    task.end_date = datetime.utcnow()
                    session.commit()
                return 'Task Closed'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error closing project: {e}'


    def add_task(self, session):

        dictToCheck = {"Project FKEY": self.project_fkey,
                       "Task Name": self.name,
                       "Task Description": self.desc,
                       "Task Status": self.status,
                       "Task Stat Date": self.start_date,
                       "Task Due Date": self.due_date,
                       "Assignee": self.assignee_fkey,
                       "Assigner": self.assigner_fkey}
        # check if fields are null
        for attribute, val in dictToCheck.items():
            if val == '':
                return f'the field {attribute} can not be empty'

        # if fields are not null
        else:
            try:
                # Create a session
                with session() as session:
                    # query db for the task
                    projectTask = (
                        session.query(Project)
                        .options(joinedload(Project.tasks))
                        .filter(Project.project_pkey == self.project_fkey,
                                Project.is_removed == 0,
                                Task.is_removed == 0,
                                Task.name == self.name)
                        .join(Task)
                        .first())

                    # if the task of project already exists in the database
                    if projectTask:
                        return f'Error!, the task: {self.name} already exists'

                    # if project is not in the database the add
                    if projectTask is None:
                        session.add(self)
                        session.commit()
                        return 'successful'

            #exception with sql alchemy
            except SQLAlchemyError as e:
                return f'Error during adding project: {e}'

    def get_task(self, session, task_pkey):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                # query db for project
                task = (
                    session.query(Task)
                    .join(User, Task.assignee_fkey == User.user_pkey)
                    .join(Project, Task.project_fkey == Project.project_pkey)
                    .options(joinedload(Task.assignee), joinedload(Task.assigner), joinedload(Task.project))
                    .filter(Project.is_removed == 0, Task.is_removed == 0, Task.task_pkey == task_pkey)
                    .first()
                )

                if task:
                    return task

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'


    def unassign_tasks(self, session, user_pkey):
        try:
            # Create a session
            with session() as session:
                # get tasks assigned to or assigned by the user
                tasks = session.query(Task).filter(
                    or_(Task.assignee_fkey == user_pkey, Task.assigner_fkey == user_pkey)
                ).all()

               # un-assign the tasks
                if tasks:
                    for task in tasks:
                        if task.assignee_fkey == user_pkey:
                            task.assignee_fkey = -1
                        if task.assigner_fkey == user_pkey:
                            task.assigner_fkey = -1
                    session.commit()
                    return 'Tasks un-assigned successfully'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error un-assigning tasks: {e}'


    # def get_project_progress(self, session):
    #     """Get the progress of the project in percentage
    #     :param session: the session to use
    #     :return: total tasks, completed tasks, progress percentage
    #     """
    #     try:
    #         # Create a session
    #         with session() as session:
    #             # Query the database for the total number of tasks in the project
    #             total_tasks = session.query(func.count(Project.tasks.task_pkey)).filter(
    #                 Project.Task.project_fkey == self.project_pkey, Project.Task.is_removed == 0).scalar()
    #             # Query the database for the total number of completed tasks in the project
    #             completed_tasks = session.query(func.count(Task.task_pkey)).filter(
    #                 Task.project_fkey == self.project_pkey, Task.status == 'Completed', Task.is_removed == 0).scalar()
    #
    #             # If there are no tasks in the project, set to 0
    #             if total_tasks == 0:
    #                 return 0
    #             else:
    #                 # Calculate the progress percentage
    #                 progress_percentage = (completed_tasks / total_tasks) * 100
    #                 return total_tasks, completed_tasks, progress_percentage
    #
    #     except SQLAlchemyError as e:
    #         return f'Error retrieving project progress: {e}'