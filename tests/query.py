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

    emailSender = EmailSender()
    emailSender.set_action_user(4)
    emailSender.set_project(47)
    # Create thread for email
    snd = emailSender.on_project_creation('nava nava saa laya')
    print(snd)