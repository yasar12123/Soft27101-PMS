from src.ClassBase import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime

class UserRole(Base):
    __tablename__ = 'USER_ROLE'

    user_role_pkey = Column(Integer, primary_key=True, autoincrement=True)
    user_fkey = Column(Integer, ForeignKey('USER.user_pkey'), nullable=False)
    role_type = Column(String(100), nullable=False)
    role_desc = Column(String(255), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=False, nullable=False)

    # Define the relationship
    user = relationship('User', back_populates='user_roles')

