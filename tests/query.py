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

    dbCon = DatabaseConnection()
    session = dbCon.get_session()
    # Class user to query
    user = User()
    # authenticate user
    userAuthentication, userInstance = user.authenticate(session, 'tm1', '12345')

    print(userInstance.username)
