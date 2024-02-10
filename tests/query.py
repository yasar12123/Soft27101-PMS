from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTeam import Team

from sqlalchemy.orm import sessionmaker


# Define the SQLAlchemy engine and metadata
db = DatabaseConnection()
engine = db.get_engine()
metadata = db.get_metadata()


# create a session to manage the connection to the database
Session = sessionmaker(bind=engine)
session = Session()


users = session.query(User).all()
#projects = session.query(Project).all()
#projectTeams = session.query(ProjectTeam).all()
#teams = session.query(Team).all()
# tasks = session.query(Task).all()

# Assuming you have a User instance
#user = session.query(User).filter_by(username='teamMember1').first()

# for project in projects:
#     print(project.status)
#     project.update_status('closed', session)
#     print(project.status)
#     session.commit()