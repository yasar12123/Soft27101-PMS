from src.ClassBase import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class TimelineEvent(Base):
    __tablename__ = 'TIMELINE_EVENT'

    timeline_event_pkey = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String, nullable=False)
    event_desc = Column(String, nullable=False)
    event_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    project_fkey = Column(Integer, ForeignKey('PROJECT.project_pkey'))
    task_fkey = Column(Integer, ForeignKey('TASK.task_pkey'))
    user_fkey = Column(Integer, ForeignKey('USER.user_pkey'))

    # Define relationships to the Project and Task tables
    project = relationship("Project", back_populates="timeline_events")
    task = relationship("Task", back_populates="timeline_events")
    user = relationship("User", back_populates="timeline_events")

    @classmethod
    def log_project_creation(cls, session, project):
        try:
            # Create a new TimelineEvent instance
            event = cls(
                event_type="Project Creation", event_desc=f"Project '{project.name}' was created.",
                project_fkey=project.project_pkey, task_fkey=-1, user_fkey=project.owner_fkey
            )
            with session() as session:
                session.add(event)
                session.commit()
                return "Project creation logged successfully."

        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error logging project creation: {e}'




