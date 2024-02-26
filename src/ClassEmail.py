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


    def on_project_creation(self, recipient_email, project_name):
        to = recipient_email
        subject = f'TT_CROP - Project: {project_name} has been created'
        message = f'you have created a new project name {project_name}'
        email = self.send_email(recipient_email=to, subject=subject, message=message)
        return email

    def on_task_creation(self, recipient_email, project_name, task_name):
        to = recipient_email
        subject = f'TT_CROP - Task: {task_name} for Project: {project_name} has been created'
        message = f'you have created a new task named {task_name} for the project {project_name}'
        email = self.send_email(recipient_email=to, subject=subject, message=message)
        return email

    def on_task_assign(self, recipient_email, project_name, task_name, assigner_name):
        to = recipient_email
        subject = f'TT_CROP - Task: {task_name} for Project: {project_name}'
        message = f'you have been assigned a task named: {task_name} for the project: {project_name}, by {assigner_name}'
        email = self.send_email(recipient_email=to, subject=subject, message=message)
        return email


# # Initialize and use the EmailSender class
# email_sender = EmailSender()
# email_sender.send_email(['yasar1212@hotmail.co.uk'], 'test', 'this is a test message')

