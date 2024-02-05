from src.ClassBase import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Team(Base):
    __tablename__ = 'TEAM'

    team_pkey = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String(255), nullable=False)
    team_desc = Column(String(255))
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime)

    # Define the relationships
    project_associations = relationship('ProjectTeam', back_populates='team')

