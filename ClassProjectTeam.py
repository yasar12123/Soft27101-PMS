from ClassBase import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


class ProjectTeam(Base):
    __tablename__ = 'PROJECT_TEAM'  # Adjusted table name

