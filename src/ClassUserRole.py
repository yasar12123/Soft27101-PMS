from src.ClassBase import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


class UserRole(Base):
    """
    A class to represent a user role in the database
    Attributes:
        user_role_pkey: The primary key of the user role
        user_fkey: The foreign key of the user associated with the role
        role_type: The type of role
        role_desc: A description of the role
        start_date: The date the role was assigned
        end_date: The date the role was removed
        is_active: A flag indicating if the role is currently active
        user: The user associated with the role

    Methods:
        add_user_role(session, user_fkey, role_type_specified): Add a new user role to the database
        delete_user_role(session, user_fkey, role_type=None): Delete a user role from the database
    """
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

    @classmethod
    def add_user_role(cls, session, user_fkey, role_type_specified):
        """
        Add a new user role to the database
        :param session: The session to use for the database interaction
        :type session: sqlalchemy.orm.session.Session
        :param user_fkey: The foreign key of the user to add the role to
        :type user_fkey: int
        :param role_type_specified: The type of role to add
        :type role_type_specified: str
        :return: A message indicating the success or failure of the operation

        """
        # check if the mentioned role can be used
        add_role = False
        if role_type_specified == 'Admin':
            role_desc_derived = 'Administrator privileges'
            add_role = True
        if role_type_specified == 'StandardUser':
            role_desc_derived = 'Standard user of system'
            add_role = True

        # boolean to run query if a specified role is given
        if add_role:
            try:
                with session() as session:

                    # Create a new UserRole instance with the provided values
                    new_user_role = cls(user_fkey=user_fkey, role_type=role_type_specified, role_desc=role_desc_derived)
                    # Add the new user role instance to the session
                    session.add(new_user_role)
                    # Commit the session to persist the changes to the database
                    session.commit()
                    return f'{role_desc_derived} added successfully'

            except SQLAlchemyError as e:
                # Handle the exception or log the error
                return f"Error adding user role: {e}"
        else:
            return 'Specified role is not a part of the system'

    @classmethod
    def delete_user_role(cls, session, user_fkey, role_type=None):
        """
        Delete a user role from the database
        :param session: The session to use for the database interaction
        :type session: sqlalchemy.orm.session.Session
        :param user_fkey: The foreign key of the user to delete the role from
        :type user_fkey: int
        :param role_type: The type of role to delete. If None, all roles for the user will be deleted
        :type role_type: str

        :return: A message indicating the success or failure of the operation
        """
        try:
            with session() as session:
                user_roles_query = session.query(cls).filter(cls.user_fkey == user_fkey)
                if role_type:
                    user_roles_query = user_roles_query.filter(cls.role_type == role_type)
                    deleted_count = user_roles_query.delete()
                    if deleted_count > 0:
                        return f"User role '{role_type}' deleted successfully"
                    else:
                        return f"No user roles found with type '{role_type}'"
                else:
                    deleted_count = user_roles_query.delete()
                    if deleted_count > 0:
                        return "All user roles deleted successfully"
                    else:
                        return "No user roles found for deletion"
        except SQLAlchemyError as e:
            # Log or handle the exception
            return f'Error deleting user role(s): {e}'



