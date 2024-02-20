from src.ClassBase import Base
from src.ClassUser import User
from src.ClassProjectTeam import ProjectTeam

from src.ClassDatabaseConnection import DatabaseConnection

from sqlalchemy.orm import relationship, aliased, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
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
    is_removed = Column(Integer, default=0)

    # Define the relationships
    owner = relationship('User', back_populates='owner_of_projects')
    tasks = relationship('Task', back_populates='project')
    project_team_members = relationship('ProjectTeam', back_populates='project')
    communication_log = relationship('CommunicationLog', back_populates='project')


    def get_projects_for_team_member(self, session, team_member_username):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                teamUser = aliased(User)
                query = (
                    session.query(Project)
                    .join(Project.owner)
                    .join(Project.project_team_members)
                    .join(teamUser, ProjectTeam.user_fkey == teamUser.user_pkey)
                    .filter(teamUser.username == team_member_username)
                    .filter(Project.is_removed == 0)
                    .options(joinedload(Project.owner))
                )
                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'


    def get_projects(self, session):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                query = (
                    session.query(Project)
                    .join(Project.owner)
                    .filter(Project.is_removed == 0)
                    .options(joinedload(Project.owner))
                )
                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'



    def add_project(self, session):

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
                        .filter(Project.name == self.name)  # Filter by project name
                        .filter(Project.is_removed == 0)  # Filter by is_removed status
                        .first()
                    )
                    # if the project already exists in the database
                    if project:
                        return f'Error!, the project: {self.name} already exists'
                    # if project is not in the database
                    if project is None:
                        session.add(self)
                        session.commit()
                        return 'successful'
            except SQLAlchemyError as e:
                # Log or handle the exception
                return f'Error during adding project: {e}'


    def get_project(self, session, projectName):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                query = (
                    session.query(Project)
                    .join(Project.owner)
                    .options(joinedload(Project.owner))
                    .filter(Project.name == projectName)
                )
                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'


    def get_project_fkey(self, session, projectName):
        # Try to establish connection to db
        try:
            # Create a session
            with session() as session:
                # query db for the user
                project = session.query(Project).filter_by(name=projectName).first()
                return project.project_pkey

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error connecting: {e}'

    def delete_project(self, session, projectName):
        try:
            # Create a session
            with session() as session:
                project = session.query(Project).filter_by(name=projectName).first()
                if project:
                    project.is_removed = 1
                    session.commit()
                    return 'Project deleted successfully'
                else:
                    return 'Project not found'
        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error deleting project: {e}'

