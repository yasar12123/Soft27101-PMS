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

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()

class EmailSender:
    def __init__(self):
        self.email = os.getenv('OUTLOOK_USER')
        self.password = os.getenv('OUTLOOK_PASS')
        self.smtp_server = os.getenv('OUTLOOK_SMTP_SERVER')
        self.smtp_port = os.getenv('OUTLOOK_SMTP_PORT')
        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()
        self.recipient = None
        self.actionUser = None
        self.project = None
        self.task = None
        self.taskName = None

    def set_project(self, project_pkey):
        p = Project()
        project = p.get_project(self.session, project_pkey)
        self.project = project

    def set_task(self, task_pkey):
        t = Task()
        task = t.get_task(self.session, task_pkey)
        self.task = task

    def set_task_name(self, task_name):
        self.taskName = task_name

    def set_recipient(self, recipient_fkey):
        u = User()
        recipient = u.get_user_instance(self.session, recipient_fkey)
        self.recipient = recipient
        return self.recipient.email_address

    def set_action_user(self, action_user_fkey):
        u = User()
        actionUser = u.get_user_instance(self.session, action_user_fkey)
        self.actionUser = actionUser
        return self.actionUser.username

    def send_email(self, recipient_email, subject, message):
        try:
            # Create email
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = ', '.join(recipient_email)
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp_server:
                smtp_server.starttls()
                smtp_server.login(self.email, self.password)
                smtp_server.sendmail(self.email, recipient_email, msg.as_string())

            return "Message sent!"

        except Exception as e:
            return f"An error occurred while sending the email: {e}"

    def on_project_creation(self, project_name):
        to = self.recipient.email_address
        subject = f'TT_CROP - Project: {project_name} has been created'
        message = f'you have created a new project: {project_name}'
        email = self.send_email(recipient_email=[to], subject=subject, message=message)
        return email

    def on_task_creation(self):
        to = self.recipient.email_address
        subject = f'TT_CROP - Task: {self.taskName} for Project: {self.project.name} has been created'
        message = f'you have created a new task named {self.taskName} for the project {self.project.name}'
        email = self.send_email(recipient_email=[to], subject=subject, message=message)
        return email

    def on_task_assign(self):
        to = self.recipient.email_address
        subject = f'TT_CROP - Task: {self.taskName} for Project: {self.project.name} - ASSIGNED'
        message = f'you have been assigned a task named: {self.taskName} for the project: {self.project.name}, by {self.actionUser.full_name} ({self.actionUser.username})'
        sendEmail = self.send_email(recipient_email=[to], subject=subject, message=message)
        return sendEmail

    def on_task_close(self):
        to = self.recipient.email_address
        subject = f'TT_CROP - Task: {self.taskName} for Project: {self.project.name} - CLOSED'
        message = f'The task named: {self.taskName} for the project: {self.project.name} has now been closed, by {self.actionUser.full_name} ({self.actionUser.username})'
        sendEmail = self.send_email(recipient_email=[to], subject=subject, message=message)
        return sendEmail

    def on_project_close(self):
        #send to list
        sendList = []

        #get list of all team members and append to sendList
        pt = ProjectTeam()
        projectTeam = pt.get_team_of_project(self.session, self.project.project_pkey)
        for user in projectTeam:
            sendList.append(user.user.email_address)

        # message
        subject = f'TT_CROP - Project: {self.project.name} - CLOSED'
        message = f'The project named: {self.project.name} has now been closed by {self.actionUser.full_name} ({self.actionUser.username})'
        sendEmail = self.send_email(recipient_email=sendList, subject=subject, message=message)
        return sendEmail

    def on_project_delete(self):
        #send to list
        sendList = []

        #get list of all team members and append to sendList
        pt = ProjectTeam()
        projectTeam = pt.get_team_of_project(self.session, self.project.project_pkey)
        for user in projectTeam:
            sendList.append(user.user.email_address)

        # message
        subject = f'TT_CROP - Project: {self.project.name} - DELETED'
        message = f'The project named: {self.project.name} has now been deleted by {self.actionUser.full_name} ({self.actionUser.username})'
        sendEmail = self.send_email(recipient_email=sendList, subject=subject, message=message)
        return sendEmail

    def on_add_to_project(self):
        to = self.recipient.email_address
        subject = f'TT_CROP - Project: {self.project.name} - You have been added'
        message = f'you have been added to the project: {self.project.name}, by {self.actionUser.full_name} ({self.actionUser.username})'
        sendEmail = self.send_email(recipient_email=[to], subject=subject, message=message)
        return sendEmail