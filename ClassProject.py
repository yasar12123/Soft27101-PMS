
from ClassBase import Base

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
    owner = relationship('User', back_populates='projects')
    tasks = relationship('Task', back_populates='project')

    def update_status(self, new_status, session):
        """Update the status of the project."""
        if self.status == new_status:
            raise UserWarning(f'the status is already set to {new_status}')
        else:
            # Print the current status
            print("Current Project Status:", self.status)

            # Update the status
            self.status = new_status

            # Commit the changes
            #session.commit()
