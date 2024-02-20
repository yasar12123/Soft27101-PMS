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

    # get user fkey
    user = User()
    userFkey = user.get_user_fkey(session, 'po1')
    # get project fkey
    project = Project()
    projectFkey = project.get_project_fkey(session, 'project A')

    commentToAdd = 'new comment'

    db = DatabaseConnection()
    session = db.get_session()
    # Create a new comment instance
    new_comment = CommunicationLog(user_fkey=userFkey, project_fkey=projectFkey, task_fkey=-1, comment=commentToAdd,
                                   timestamp=datetime.datetime.now())
    # register user
    new_comment.add_project_comment(session)
    #print(new_comment.comment, new_comment.timestamp, new_comment.user_fkey)



