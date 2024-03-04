from src.ClassBase import Base
from src.ClassUser import User
from src.ClassProjectTeam import ProjectTeam
from sqlalchemy.orm import relationship, aliased, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from datetime import datetime


class Project(Base):
    """
    Class to represent the Project table in the database.

    Attributes:
        project_pkey: int, primary key, autoincrement
        name: str, not null
        desc: str, not null
        status: str, not null
        start_date: datetime, not null
        end_date: datetime
        due_date: datetime
        owner_fkey: int, foreign key, not null
        project_progress: int, default 0
        is_removed: int, default 0
        owner: relationship, back_populates='owner_of_projects'
        tasks: relationship, back_populates='project'
        project_team_members: relationship, back_populates='project'
        communication_log: relationship, back_populates='project'

    Methods:
        get_projects: Get all projects from the database
        add_owner_to_project_team: Add the owner to the project team
        add_project: Add a project to the database and add the owner to the project team
        set_project: Set the project details
        delete_project: Delete a project from the database
        close_project: Close a project
        unassign_projects: Un-assign projects from a user
        get_project: Get a project from the database
        get_project_team: Get all users assigned to a project
        get_projects_user_member_of: Get all projects that a user is a member of
    """
    # Define the table name
    __tablename__ = 'PROJECT'

    project_pkey = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    desc = Column(String, nullable=False)
    status = Column(String(100), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime)
    due_date = Column(DateTime)
    owner_fkey = Column(Integer, ForeignKey('USER.user_pkey'), nullable=False)
    project_progress = Column(Integer, default=0)
    is_removed = Column(Integer, default=0)

    # Define the relationships
    owner = relationship('User', back_populates='owner_of_projects')
    tasks = relationship('Task', back_populates='project')
    project_team_members = relationship('ProjectTeam', back_populates='project')
    communication_log = relationship('CommunicationLog', back_populates='project')

    @classmethod
    def get_projects(cls, session, team_member_user_pkey=None, completed=None):
        """
        Get all projects from the database
        if task_member_user_pkey is not None, then query for projects assigned to the team member
        if task_member_user_pkey is None, then query for all projects
        if completed is True, then filter by project status for completed projects
        if completed is False, then filter by project status for non-completed projects

        :param session: the session to use
        :type session: sqlalchemy.orm.session.Session
        :param team_member_user_pkey: the team members user primary key
        :type team_member_user_pkey: int
        :param completed: the project status (true or false)
        :type completed: bool
        :return: a list of projects
        :rtype: list
        """
        try:
            with session() as session:

                # if team_member_user_pkey is not None, then query for projects assigned to the team member
                if team_member_user_pkey:
                    teamUser = aliased(User)
                    query = (session.query(cls)
                             .join(cls.owner)
                             .join(cls.project_team_members)
                             .join(teamUser, ProjectTeam.user_fkey == teamUser.user_pkey)
                             .filter(cls.is_removed == 0, ProjectTeam.is_removed == 0, cls.project_pkey != -1)
                             .options(joinedload(cls.owner)))

                # if team_member_user_pkey is None, then query for all projects
                else:
                    query = (session.query(cls)
                             .join(cls.owner)
                             .filter(cls.is_removed == 0)
                             .options(joinedload(cls.owner)))

                # if completed is True, then filter by project status for completed projects
                if query and completed is True:
                    query = query.filter(cls.status == 'Completed')

                # if completed is False, then filter by project status for non-completed projects
                if query and completed is False:
                    query = query.filter(cls.status != 'Completed')

                # Order by due date
                if query:
                    query = query.order_by(cls.due_date)

                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    def add_owner_to_project_team(self, session):
        """
        Add the owner to the project team
        :param session: the session to use
        :type session: sqlalchemy.orm.session.Session
        :return: a string indicating the result of the operation
        :rtype: str
        """
        pt = ProjectTeam(user_fkey=self.owner_fkey, project_fkey=self.project_pkey)
        projectUser = pt.add_team_member_to_project(session)
        if projectUser == 'successful':
            return 'owner has been added'
        else:
            return projectUser

    def add_project(self, session):
        """
        Add a project to the database and add the owner to the project team
        :param session: the session to use
        :type session: sqlalchemy.orm.session.Session
        :param owner_fkey: the owner's user primary key
        :type owner_fkey: int
        :return: a string indicating the result of the operation
        :rtype: str
        """
        session1 = session
        session2 = session
        # check if fields are null
        fields_to_check = {"Project Name": self.name, "Project Description": self.desc, "Project Status": self.status,
                           "Project Stat Date": self.start_date, "Project Due Date": self.due_date}
        for attribute, val in fields_to_check.items():
            if val == '':
                return f'the field {attribute} can not be empty'

        else:
            try:
                with session1() as session:

                    # query db for the project
                    project = (session.query(Project)
                               .filter(Project.name == self.name, Project.is_removed == 0).first())

                    # if project is in the database
                    if project:
                        return f'Error!, the project: {self.name} already exists'

                    # if project is not in the database
                    if project is None:
                        session.add(self)
                        session.commit()

                        # add the owner to the project team
                        self.add_owner_to_project_team(session2)

                        return 'successful'

            except SQLAlchemyError as e:
                # Log or handle the exception
                return f'Error during adding project: {e}'

    @classmethod
    def set_project(cls, session, userInstance, projectPkey, setName, setDesc, setStatus, setStartDate, setDueDate, setProjectProgress):
        """
        Set the project details
        :param session: the session to use
        :type session: sqlalchemy.orm.session.Session
        :param userInstance: the user instance
        :type userInstance: src.ClassUser.User
        :param projectPkey: the project primary key
        :type projectPkey: int
        :param setName: the project name
        :type setName: str
        :param setDesc: the project description
        :type setDesc: str
        :param setStatus: the project status
        :type setStatus: str
        :param setStartDate: the project start date
        :type setStartDate: datetime
        :param setDueDate: the project due date
        :type setDueDate: datetime
        :param setProjectProgress: the project progress
        :type setProjectProgress: int
        """
        # check if fields are null
        fields_to_check = {"Project Name": setName, "Project Description": setDesc, "Project Status": setStatus,
                           "Project Stat Date": setStartDate, "Project Due Date": setDueDate}
        for attribute, val in fields_to_check.items():
            if val == '':
                return f'the field {attribute} can not be empty'

        # check if project due date is not greater than the start date
        if setDueDate < setStartDate:
            return 'Project due date can not be less than the start date'

        # find if user is admin
        is_admin = userInstance.is_user_admin(session, userInstance.user_pkey)

        try:

            with session() as session:
                # query db for the project
                project = session.query(cls).filter_by(project_pkey=projectPkey).first()
                # if project does not exit
                if project is None:
                    return 'Project does not exist'

                else:
                    # check if user is an admin or the project owner
                    if is_admin or userInstance.user_pkey == project.owner_fkey:
                        project.name = setName
                        project.desc = setDesc
                        project.status = setStatus
                        project.start_date = setStartDate
                        project.due_date = setDueDate
                        project.project_progress = setProjectProgress
                        session.commit()
                        return 'Project updated'

                    # else return no permissions to update
                    else:
                        return 'You do not have permissions to update this project'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error setting data: {e}'

    @classmethod
    def delete_project(cls, session, user_instance, project_pkey):
        """
        Delete a project from the database
        :param session: the session to use
        :type session: sqlalchemy.orm.session.Session
        :param user_instance: the user instance
        :type user_instance: src.ClassUser.User
        :param project_pkey: the project primary key
        :type project_pkey: int
        :return: a string indicating the result of the operation
        :rtype: str
        """

        # find if user is admin
        is_admin = user_instance.is_user_admin(session, user_instance.user_pkey)

        try:

            with session() as session:
                # query db for the project
                project = session.query(cls).filter_by(project_pkey=project_pkey).first()

                # check if user is an admin or the project owner
                if is_admin or user_instance.user_pkey == project.owner_fkey:

                    if project:
                        project.is_removed = 1
                        session.commit()
                        return 'Project deleted successfully'
                    else:
                        return 'Project not found'

                # else return no permissions to delete
                else:
                    return 'You do not have permissions to delete this project'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error deleting project: {e}'

    @classmethod
    def close_project(cls, session, user_instance, project_pkey):
        """
        Close a project
        :param session: the session to use
        :type session: sqlalchemy.orm.session.Session
        :param user_instance: the user instance
        :type user_instance: src.ClassUser.User
        :param project_pkey: the project primary key
        :type project_pkey: int
        :return: a string indicating the result of the operation
        :rtype: str
        """

        # find if user is admin
        is_admin = user_instance.is_user_admin(session, user_instance.user_pkey)

        try:
            with session() as session:
                # query db for the project
                project = session.query(cls).filter_by(project_pkey=project_pkey).first()

                # check if user is an admin or the project owner
                if is_admin or user_instance.user_pkey == project.owner_fkey:

                    # if project does not exit
                    if project is None:
                        return 'Project does not exist'

                    # mark project as completed, update the end date and project progress to 100
                    else:
                        project.status = 'Completed'
                        project.end_date = datetime.utcnow()
                        project.project_progress = 100
                        session.commit()
                        return 'Project Closed'

                else:
                    return 'You do not have permissions to close this project'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error closing project: {e}'

    @classmethod
    def unassign_projects(cls, session, user_pkey):
        """
        Un-assign projects from a user
        :param session: the session to use
        :type session: sqlalchemy.orm.session.Session
        :param user_pkey: the user primary key
        :type user_pkey: int
        :return: a string indicating the result of the operation
        :rtype: str
        """

        try:
            with session() as session:
                # query db for the projects assigned to the user
                projects = (session.query(cls)
                            .filter(cls.owner_fkey == user_pkey)).all()

                # if user has projects assigned
                if projects:
                    for project in projects:
                        project.owner_fkey = -1
                    session.commit()
                    return 'Projects un-assigned successfully'

                # if user has no projects assigned
                else:
                    return 'User has no projects assigned'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error un-assigning projects: {e}'

    @staticmethod
    def get_project(session, project_pkey):
        """
        Get a project from the database
        :param session: the session to use
        :type session: sqlalchemy.orm.session.Session
        :param project_pkey: the project primary key
        :type project_pkey: int
        :return: the project
        :rtype: src.ClassProject.Project
        """

        try:
            with session() as session:
                # query db for the project
                project = (session.query(Project)
                           .options(joinedload(Project.owner))
                           .filter_by(project_pkey=project_pkey)
                           .first())

                # if project is in the database
                if project:
                    return project
                # if project is not in the database
                else:
                    return 'Project not found'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    @staticmethod
    def get_project_team(session, project_pkey=None):
        """
        Get all users assigned to a project
        :param session: the session to use
        :type session: sqlalchemy.orm.session.Session
        :param project_pkey: the project primary key
        :type project_pkey: int
        :return: a list of project team members
        :rtype: list
        """

        try:
            with session() as session:
                # query db for the project team
                query = (session.query(ProjectTeam)
                         .join(ProjectTeam.user)
                         .join(ProjectTeam.project)
                         .options(joinedload(ProjectTeam.user))
                         .options(joinedload(ProjectTeam.project))
                         .filter(ProjectTeam.is_removed == 0, Project.is_removed == 0))

                # If projectPkey is specified, filter on project primary key
                if project_pkey:
                    query = query.filter(ProjectTeam.project.has(project_pkey=project_pkey))

                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    @staticmethod
    def is_user_project_owner(session, user_pkey, project_pkey):
        """
        Check if a user is the owner of a project
        :param session: the session to use
        :type session: sqlalchemy.orm.session.Session
        :param user_pkey: the user primary key
        :type user_pkey: int
        :param project_pkey: the project primary key
        :type project_pkey: int
        :return: a boolean indicating if the user is the owner of the project
        :rtype: bool
        """
        try:
            with session() as session:

                # query db for the project
                project = (session.query(Project)
                           .filter_by(project_pkey=project_pkey)
                           .first())

                # if project is in the database
                if project:

                    # check if user is the owner of the project
                    if project.owner_fkey == user_pkey:
                        return True

                    # if user is not the owner of the project
                    else:
                        return False

                # if project is not in the database
                else:
                    return False

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    @classmethod
    def get_projects_user_member_of(cls, session, user_pkey):
        """
        Get all projects that a user is a member of that have not been completed
        :param session: the session to use
        :type session: sqlalchemy.orm.session.Session
        :param user_pkey: the user primary key
        :type user_pkey: int
        :return: a list of projects
        :rtype: list
        """
        try:
            with session() as session:
                # Query db for the projects that the user is a member of that have not been completed
                query = (session.query(cls)
                         .join(cls.owner)
                         .join(cls.project_team_members)
                         .options(joinedload(cls.owner))
                         .filter(cls.is_removed == 0, cls.status != 'Completed',
                                 cls.project_team_members.any(ProjectTeam.is_removed == 0),
                                 cls.project_team_members.any(ProjectTeam.user_fkey == user_pkey)))

                # Order by due date
                if query:
                    query = query.order_by(cls.due_date)
                    return query.all()
                else:
                    return 'No projects found'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'
