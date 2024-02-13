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



# Example usage
if __name__ == '__main__':
    # Create a session
    db = DatabaseConnection()
    session = db.get_session()


    # Get the ID of the team member (replace 1 with the actual ID)
    team_member_username = 'tm1'

    #Query all projects for the team member
    a = Project()
    projects = a.get_projects_for_team_member(session, team_member_username)
    # Iterate over the projects and print the project name and owner
    for project in projects:
        print(project.owner.full_name)
        #print(f"Project Name: {project.name}, Owner: {owner.full_name}")



