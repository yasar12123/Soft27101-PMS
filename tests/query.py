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

    new_project = Project(name='test', desc='this', start_date=datetime.utcnow, due_date=datetime.utcnow, status='Not Started',
                          owner_fkey=4, is_removed=0)


    # log addition as event
    event = TimelineEvent()
    addEvent = event.log_project_creation(session, new_project)

    print(addEvent)
