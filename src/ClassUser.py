from src.ClassBase import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime


class User(Base):
    __tablename__ = 'USER'

    user_pkey = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    full_name = Column(String(100), nullable=False)
    email_address = Column(String(100), nullable=False)
    password_hashed = Column(String(255), nullable=False)
    date_registered = Column(DateTime, default=datetime.utcnow)

    # Define the relationships
    owner_of_projects = relationship('Project', back_populates='owner')
    team_associations = relationship('ProjectTeam', back_populates='user')
    assigned_tasks = relationship('Task', back_populates='assignee', foreign_keys='Task.assignee_fkey')
    assigner_of_tasks = relationship('Task', back_populates='assigner', foreign_keys='Task.assigner_fkey')
    user_roles = relationship('UserRole', back_populates='user')
    communication_log = relationship('CommunicationLog', back_populates='user')


class UserAdmin(User):
    __tablename__ = 'USER_ADMIN'

    user_admin_pkey = Column(Integer, ForeignKey('USER.user_pkey'), primary_key=True)

class UserProjectOwner(User):
    __tablename__ = 'USER_PROJECT_OWNER'

    user_project_owner_pkey = Column(Integer, ForeignKey('USER.user_pkey'), primary_key=True)


