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
    tasks = t.get_tasks_for_team_member(session, 'tm1')  # , project_fkey=self.project_pkey)

    completed_tasks = sum(1 for task in tasks if task.status == 'Completed')
    #in_progress_tasks = sum(1 for task in tasks if task.status == 'In-Progress')