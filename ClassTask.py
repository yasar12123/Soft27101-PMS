
from ClassBase import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
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

    # Define the relationships
    project = relationship('Project', back_populates='tasks')
    assignee = relationship('User', back_populates='assigned_tasks', foreign_keys=[assignee_fkey])
    assigner = relationship('User', back_populates='assigner_of_tasks', foreign_keys=[assigner_fkey])

