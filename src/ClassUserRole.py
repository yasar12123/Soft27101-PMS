from src.ClassBase import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class UserRole(Base):
    __tablename__ = 'USER_ROLE'

    user_role_pkey = Column(Integer, primary_key=True, autoincrement=True)
    user_fkey = Column(Integer, ForeignKey('USER.user_pkey'), nullable=False)
    role_type = Column(String(100), nullable=False)
    role_desc = Column(String(255), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime)
    is_active = Column(Integer, default=1, nullable=False)

    # Define the relationship
    user = relationship('User', back_populates='user_roles')


    def add_user_role(self, session, user_fkey, role_type, role_desc):
        try:
            with session() as session:
                # Create a new UserRole instance with the provided values
                new_user_role = UserRole(user_fkey=user_fkey, role_type=role_type, role_desc=role_desc)
                # Add the new user role instance to the session
                session.add(new_user_role)
                # Commit the session to persist the changes to the database
                session.commit()
                return 'User role added successfully'

        except SQLAlchemyError as e:
            # Handle the exception or log the error
            print(f"Error adding user role: {e}")
