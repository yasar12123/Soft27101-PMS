from src.ClassBase import Base
from src.ClassUser import User
from src.ClassProjectTeam import ProjectTeam

from src.ClassDatabaseConnection import DatabaseConnection

from sqlalchemy.orm import relationship, aliased, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from datetime import datetime



class Project(Base):

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
        """Get all projects
        :param session: the session to use
        :type session: sqlalchemy.orm.session.Session
        :param team_member_user_pkey: the team member user primary key
        :type team_member_user_pkey: int
        :param completed: the status of the project
        :type completed: bool
        :return: all projects for a team member
        """
        try:
            with session() as session:

                # if team_member_user_pkey is not None, then query for projects assigned to the team member
                if team_member_user_pkey:
                    teamUser = aliased(User)
                    query = (
                        session.query(cls)
                        .join(cls.owner)
                        .join(cls.project_team_members)
                        .join(teamUser, ProjectTeam.user_fkey == teamUser.user_pkey)
                        .filter(cls.is_removed == 0, ProjectTeam.is_removed == 0)
                        .options(joinedload(Project.owner)))

                # if team_member_user_pkey is None, then query for all projects
                else:
                    query = (
                        session.query(cls)
                        .join(cls.owner)
                        .filter(cls.is_removed == 0)
                        .options(joinedload(Project.owner)))

                # if completed is not None, then query for completed projects
                if completed:
                    query = query.filter(cls.status != 'Completed')

                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    def add_owner_to_project_team(self, owner_fkey):
        # Create a session
        db = DatabaseConnection()
        session = db.get_session()

        pt = ProjectTeam(user_fkey=owner_fkey, project_fkey=self.project_pkey, team_fkey=-1)
        projectUser = pt.add_team_member_to_project(session)
        if projectUser == 'successful':
            return 'owner has been added'
        else:
            return projectUser

    def add_project(self, session, owner_fkey):

        # check if fields are null
        dictToCheck = {"Project Name": self.name,
                       "Project Description": self.desc,
                       "Project Status": self.status,
                       "Project Stat Date": self.start_date,
                       "Project Due Date": self.due_date}

        for attribute, val in dictToCheck.items():
            if val == '':
                return f'the field {attribute} can not be empty'

        else:
            # Try to establish connection to db
            try:
                # Create a session
                with session() as session:
                    # query db for the project
                    project = (
                        session.query(Project)
                        .filter(Project.name == self.name,  # Filter by project name
                                Project.is_removed == 0)  # Filter by is_removed status
                        .first()
                    )
                    # if the project already exists in the database
                    if project:
                        return f'Error!, the project: {self.name} already exists'
                    # if project is not in the database
                    if project is None:
                        session.add(self)
                        session.commit()
                        #add owner to project team
                        self.add_owner_to_project_team(owner_fkey=owner_fkey)
                        return 'successful'
            except SQLAlchemyError as e:
                # Log or handle the exception
                return f'Error during adding project: {e}'

    @classmethod
    def set_project(cls, session, projectPkey, setName, setDesc, setStatus, setStartDate, setDueDate, setProjectProgress):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                project = session.query(cls).filter_by(project_pkey=projectPkey).first()
                if project is None:
                    return 'Project does not exist'

                else:
                    project.name = setName
                    project.desc = setDesc
                    project.status = setStatus
                    project.start_date = setStartDate
                    project.due_date = setDueDate
                    project.project_progress = setProjectProgress
                    session.commit()
                return 'Project updated'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error setting data: {e}'

    @classmethod
    def delete_project(cls, session, project_pkey):
        try:
            # Create a session
            with session() as session:
                project = session.query(cls).filter_by(project_pkey=project_pkey).first()
                if project:
                    project.is_removed = 1
                    session.commit()
                    return 'Project deleted successfully'
                else:
                    return 'Project not found'
        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error deleting project: {e}'

    @classmethod
    def close_project(cls, session, project_pkey):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                project = session.query(cls).filter_by(project_pkey=project_pkey).first()
                # if project does not exit
                if project is None:
                    return 'Project does not exist'


                else:
                    project.status = 'Completed'
                    project.end_date = datetime.utcnow()
                    project.project_progress = 100
                    session.commit()
                return 'Project Closed'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error closing project: {e}'

    @classmethod
    def get_project_fkey(cls, session, projectName):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                # query db for the user
                project = session.query(cls).filter_by(name=projectName).first()
                return project.project_pkey

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error connecting: {e}'

    def get_project(self, session, project_pkey):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                # query db for project
                project = (
                    session.query(Project)
                    .options(joinedload(Project.owner))
                    .filter_by(project_pkey=project_pkey)
                    .first()
                )

                if project:
                    return project

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'

    def unassign_projects(self, session, user_pkey):
        try:
            with session() as session:
                projects = (
                    session.query(Project)
                    .filter(Project.owner_fkey == user_pkey)
                ).all()

                # un-assign from projects
                if projects:
                    for project in projects:
                        project.owner_fkey = -1
                    session.commit()
                    return 'Projects un-assigned successfully'

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error un-assigning projects: {e}'


    def get_project_team(self, session, projectPkey=None, userPkey=None):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session_obj:
                query = (
                    session_obj.query(ProjectTeam)
                    .join(ProjectTeam.user)
                    .join(ProjectTeam.project)
                    .options(joinedload(ProjectTeam.user))
                    .options(joinedload(ProjectTeam.project))
                    .filter(ProjectTeam.is_removed == 0, Project.is_removed == 0)
                )

                # If projectPkey is specified, filter on project primary key
                if projectPkey:
                    query = query.filter(ProjectTeam.project.has(project_pkey=projectPkey))

                # If userPkey is specified, filter on user primary key
                if userPkey:
                    query = query.filter(ProjectTeam.user.has(user_pkey=userPkey))

                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'


