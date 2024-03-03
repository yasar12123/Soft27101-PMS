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

    @classmethod
    def get_assigned_tasks(cls, session, user_pkey, project_pkey=None):
        """
        Get tasks assigned to a user (for a project if specified)
        :param session: The session to use
        :param user_pkey: The user primary key
        :param project_pkey: The project primary key
        :return: A list of tasks assigned to the user (for the project if specified)
        :rtype: list
        """
        try:
            with session() as session:
                # query database for tasks
                query = (
                    session.query(cls)
                    .join(User, cls.assignee_fkey == User.user_pkey)
                    .join(Project, cls.project_fkey == Project.project_pkey)
                    .options(joinedload(cls.project))
                    .filter(cls.is_removed == 0, cls.assignee_fkey == user_pkey))

                # If project is specified, filter tasks based on the project
                if project_pkey:
                    query = query.filter(Project.project_pkey == project_pkey)

                # Order by due date
                query = query.order_by(cls.due_date)

                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    @classmethod
    def get_tasks(cls, session, project_pkey=None, project_completed=None):
        """
        Get tasks (for a project if specified) and or (completed or uncompleted if specified)
        :param session: The session to use
        :param project_pkey: The project primary key
        :param project_completed: The project status
        :return: A list of tasks (for the project if specified) and or (completed or uncompleted if specified)
        :rtype: list
        """
        try:
            with session() as session:

                # query database for tasks
                query = (
                    session.query(cls)
                    .join(User, cls.assignee_fkey == User.user_pkey)
                    .join(Project, cls.project_fkey == Project.project_pkey)
                    .options(joinedload(cls.assignee), joinedload(cls.assigner), joinedload(cls.project))
                    .filter(Project.is_removed == 0, cls.is_removed == 0))

                if query:

                    # If project is specified, filter tasks based on the project
                    if project_pkey:
                        query = query.filter(Project.project_pkey == project_pkey)

                    # If project_completed is True, filter only completed projects
                    if project_completed is True:
                        query = query.filter(Project.status == 'Completed')

                    # If project_completed is False, filter only uncompleted projects
                    if project_completed is False:
                        query = query.filter(Project.status != 'Completed')

                    # Order by due date
                    query = query.order_by(cls.due_date)

                    return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    @classmethod
    def set_task(cls, session, userInstance, project_pkey, task_pkey, setName=None, setDesc=None, setStatus=None,
                 setStartDate=None, setDueDate=None, assigneeFkey=None, assignerFkey = None, taskProgress=None):

        # find out if the user is an admin or the owner of the project
        is_admin = userInstance.is_user_admin(session, userInstance.user_pkey)
        owner = Project.is_user_project_owner(session, userInstance.user_pkey, project_pkey)

        try:
            with session() as session:
                task = session.query(cls).filter_by(task_pkey=task_pkey).first()

                if task is None:
                    return 'Task does not exist'

                else:
                    # check if the user has permission to update the task
                    if is_admin or owner or (task.assignee_fkey == userInstance.user_pkey):
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
                        session.commit()
                        return 'Task updated'

                    # if the user does not have permission to update the task
                    else:
                        return 'You do not have permission to update this task'

        except SQLAlchemyError as e:
            return f'Error setting data: {e}'

    @classmethod
    def delete_task(cls, session, userInstance, project_pkey, task_pkey):

        # find out if the user is an admin or the owner of the project
        is_admin = userInstance.is_user_admin(session, userInstance.user_pkey)
        owner = Project.is_user_project_owner(session, userInstance.user_pkey, project_pkey)

        try:
            with session() as session:
                # query db for the task
                task = session.query(cls).filter_by(task_pkey=task_pkey).first()

                if task:

                    # check if the user has permission to delete the task
                    if is_admin or owner:
                        task.is_removed = 1
                        session.commit()
                        return 'Task deleted successfully'

                    # if the user does not have permission to delete the task
                    else:
                        return 'You do not have permission to delete this task'

                else:
                    return 'Task not found'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error deleting project: {e}'

    @classmethod
    def delete_tasks_for_project(cls, session, userInstance, project_pkey):
        # find if the user is an admin
        is_admin = userInstance.is_user_admin(session, userInstance.user_pkey)
        owner = Project.is_user_project_owner(session, userInstance.user_pkey, project_pkey)

        try:
            with session() as session:
                # query db for the tasks in project
                tasks = session.query(cls).filter_by(project_fkey=project_pkey).all()

                # check if the user has permission to delete the tasks
                if is_admin or owner:

                    # if the tasks exist
                    if tasks:
                        # delete the tasks
                        for task in tasks:
                            task.is_removed = 1
                            session.commit()
                            return 'Task(s) deleted successfully'
                    else:
                        return 'No tasks found for the project'

                # if the user does not have permission to delete the tasks
                else:
                    return 'You do not have permission to delete the tasks'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error deleting project: {e}'

    @classmethod
    def close_task(cls, session, userInstance, project_pkey, task_pkey):
        # find out if the user is an admin or the owner of the project
        is_admin = userInstance.is_user_admin(session, userInstance.user_pkey)
        owner = Project.is_user_project_owner(session, userInstance.user_pkey, project_pkey)

        try:
            with session() as session:
                # query db for the task
                task = session.query(cls).filter_by(task_pkey=task_pkey).first()

                if is_admin or owner:
                    # if the task does not exist
                    if task is None:
                        return 'Task does not exist'

                    # if the task has already been closed
                    if task.end_date:
                        return 'The task has already been closed'

                    # if the task exists and has not been closed
                    else:
                        task.status = 'Completed'
                        task.task_progress = 100
                        task.end_date = datetime.utcnow()
                        session.commit()
                        return 'Task Closed'

                else:
                    return 'You do not have permission to close this task'

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

    def unassign_tasks_from_project(self, session, user_pkey, project_pkey):
        try:
            # Create a session
            with session() as session:
                # get tasks assigned to or assigned by the user for the project
                tasks = session.query(Task).filter(
                    or_(Task.assignee_fkey == user_pkey, Task.assigner_fkey == user_pkey),
                    Task.project_fkey == project_pkey
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

