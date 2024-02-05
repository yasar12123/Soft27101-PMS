from src.ClassBase import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime


class ProjectTeam(Base):
    __tablename__ = 'PROJECT_TEAM'

    project_team_pkey = Column(Integer, primary_key=True, autoincrement=True)
    user_fkey = Column(Integer, ForeignKey('USER.user_pkey'), nullable=False)
    project_fkey = Column(Integer, ForeignKey('PROJECT.project_pkey'), nullable=False)
    team_fkey = Column(Integer, ForeignKey('TEAM.team_pkey'), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime)

    # Define the relationships
    user = relationship('User', back_populates='team_associations')
    project = relationship('Project', back_populates='project_team_members')
    team = relationship('Team', back_populates='project_associations')
