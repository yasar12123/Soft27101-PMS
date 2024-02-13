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
                    .options(joinedload(Project.owner))
                )
                return query.all()

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error retrieving data: {e}'




