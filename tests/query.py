from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTeam import Team
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment
from src.ClassTimelineEvent import TimelineEvent
from src.ClassEmail import EmailSender

import matplotlib.pyplot as plt
from datetime import datetime


date_str = '09-19-2022'


# Example usage
if __name__ == '__main__':
    # Create a DatabaseConnection instance
    db = DatabaseConnection()
    # Obtain a session using the get_session() method
    session = db.get_session()

    t = Task()
    remove_from_tasks = t.unassign_tasks(session, 14)

    p = Project()
    remove_from_projects = p.unassign_projects(session, 14)

    print(remove_from_tasks)
    print(remove_from_projects)

    pt = ProjectTeam()
    delete_from_teams = pt.delete_team_member_from_projects(session, 14)
    print(delete_from_teams)

    delete_user = self.activeUserInstance.delete_user(self.session)
