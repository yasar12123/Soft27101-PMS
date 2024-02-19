from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTeam import Team
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment

import matplotlib.pyplot as plt
from datetime import datetime


import datetime

date_str = '09-19-2022'


# Example usage
if __name__ == '__main__':
    # Create a DatabaseConnection instance
    db = DatabaseConnection()
    # Obtain a session using the get_session() method
    session = db.get_session()
    # Use the obtained session to call the get_projects method
    p = Project()
    projects = p.get_project(session, 'Project A')
    # Iterate over the returned projects and print their details
    for project in projects:
        print(f"Project Name: {project.name}, Owner: {project.owner.full_name}")



