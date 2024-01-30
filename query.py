from dbConnection import dbInitalise
from ClassUser import User
from ClassProject import Project
from ClassTask import Task
from sqlalchemy.orm import sessionmaker


# Define the SQLAlchemy engine and metadata
engine, metadata = dbInitalise()


# create a session to manage the connection to the database
Session = sessionmaker(bind=engine)
session = Session()


users = session.query(User).all()
projects = session.query(Project).all()
tasks = session.query(Task).all()
print(users)