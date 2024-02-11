from src.ClassBase import Base
from sqlalchemy.orm import relationship
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



