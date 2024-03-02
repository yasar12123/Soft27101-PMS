from src.ClassBase import Base
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy import Column, Integer, DateTime, ForeignKey, delete
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime




class ProjectTeam(Base):
    __tablename__ = 'PROJECT_TEAM'

    project_team_pkey = Column(Integer, primary_key=True, autoincrement=True)
    user_fkey = Column(Integer, ForeignKey('USER.user_pkey'), nullable=False)
    project_fkey = Column(Integer, ForeignKey('PROJECT.project_pkey'), nullable=False)
    team_fkey = Column(Integer, ForeignKey('TEAM.team_pkey'), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime)
    is_removed = Column(Integer, default=0)

    # Define the relationships
    user = relationship('User', back_populates='team_associations')
    project = relationship('Project', back_populates='project_team_members')
    team = relationship('Team', back_populates='project_associations')



    def add_team_member_to_project(self, session):

        # check if fields are null
        dictToCheck = {"Project": self.project_fkey,
                       "User": self.user_fkey,
                       "Team": self.team_fkey}

        for attribute, val in dictToCheck.items():
            if val == '':
                return f'the field {attribute} can not be empty'

        else:
            # Try to establish connection to db
            try:
                # Create a session
                with session() as session:
                    # query db for the project team
                    projectTeam = (
                        session.query(ProjectTeam)
                        .filter(ProjectTeam.project_fkey == self.project_fkey,
                                ProjectTeam.user_fkey == self.user_fkey,
                                ProjectTeam.is_removed == 0)
                        .first()
                    )

                    # if the user already exists in the team
                    if projectTeam:
                        return f'Error!, {projectTeam.user.full_name} ({projectTeam.user.username}) is already a team member'
                    # if project is not in the database
                    if projectTeam is None:
                        session.add(self)
                        session.commit()
                        return 'successful'
            except SQLAlchemyError as e:
                # Log or handle the exception
                return f'Error during adding user to project team: {e}'

    @classmethod
    def delete_team_member_from_project(cls, session, user_pkey, project_pkey):
        try:
            with session() as session:
                # Get the rows to delete
                project_teams = (session.query(cls)
                                 .filter(cls.user_fkey == user_pkey,
                                         cls.project_fkey == project_pkey).all())

                # Delete the rows
                if project_teams:
                    session.execute(delete(cls)
                                    .where(cls.user_fkey == user_pkey
                                           and cls.project_fkey == project_pkey))
                    session.commit()
                    return 'Deleted successfully from team'
                else:
                    return 'User not in team'

        except SQLAlchemyError as e:
            return f'Error during removing user from team: {e}'


