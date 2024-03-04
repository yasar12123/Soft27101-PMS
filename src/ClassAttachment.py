from src.ClassBase import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BINARY, Numeric
from datetime import datetime


class Attachment(Base):
    """
    Class to represent the ATTACHMENT table in the database.

    Attributes:
        attachment_pkey: int, primary key, autoincrement
        communication_log_fkey: int, foreign key to COMMUNICATION_LOG
        file_name: str, name of the file
        data: bytes, binary data of the file
        size: float, size of the file in KB
        upload_datetime: datetime, date and time of the upload
        communication_log: relationship to CommunicationLog
    """
    __tablename__ = 'ATTACHMENT'

    attachment_pkey = Column(Integer, primary_key=True, autoincrement=True)
    communication_log_fkey = Column(Integer, ForeignKey('COMMUNICATION_LOG.communication_log_pkey'), nullable=False)
    file_name = Column(String(255), nullable=False)
    data = Column(BINARY, nullable=False)
    size = Column(Numeric(9, 2), nullable=False)
    upload_datetime = Column(DateTime, default=datetime.utcnow)

    # Define relationship
    communication_log = relationship('CommunicationLog', back_populates='attachments')

