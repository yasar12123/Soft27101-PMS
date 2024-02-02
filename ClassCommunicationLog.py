from ClassBase import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text
from datetime import datetime

class CommunicationLog(Base):
    __tablename__ = 'COMMUNICATION_LOG'

    communication_log_pkey = Column(Integer, primary_key=True, autoincrement=True)
    user_fkey = Column(Integer, ForeignKey('USER.user_pkey'), nullable=False)
    project_fkey = Column(Integer, ForeignKey('PROJECT.project_pkey'), nullable=False)
    task_fkey = Column(Integer, ForeignKey('TASK.task_pkey'), nullable=False)
    comment = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Define relationships
    user = relationship('User', back_populates='communication_log')
    project = relationship('Project', back_populates='communication_log')
    task = relationship('Task', back_populates='communication_log')
    attachments = relationship('Attachment', back_populates='communication_log')

