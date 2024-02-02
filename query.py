from dbConnection import dbInitalise
from ClassUser import User
from ClassUserRole import UserRole
from ClassProject import Project
from ClassProjectTeam import ProjectTeam
from ClassTeam import Team
from ClassCommunicationLog import CommunicationLog
from ClassAttachment import Attachment
from ClassTask import Task
from sqlalchemy.orm import sessionmaker


# Define the SQLAlchemy engine and metadata
engine, metadata = dbInitalise()


# create a session to manage the connection to the database
Session = sessionmaker(bind=engine)
session = Session()


users = session.query(User).all()
projects = session.query(Project).all()
projectTeams = session.query(ProjectTeam).all()
teams = session.query(Team).all()
# tasks = session.query(Task).all()

# Assuming you have a User instance
#user = session.query(User).filter_by(username='teamMember1').first()

# for project in projects:
#     print(project.status)
#     project.update_status('closed', session)
#     print(project.status)
#     session.commit()