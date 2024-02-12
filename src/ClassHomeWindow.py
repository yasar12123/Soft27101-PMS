from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTeam import Team
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from generated.HomeWindow import Ui_HomeWindow


import sys



class HomeWindow(QMainWindow, Ui_HomeWindow):
    def __init__(self, activeUser):
        super().__init__()
        self.setupUi(self)
        self.activeUser = activeUser
        self.populate_projects_table()



    def populate_projects_table(self):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        # project instance
        p = Project()
        projects = p.get_projects_for_team_member(session, self.activeUser)
        # Populate the projects table
        row = 0
        if projects:
            for project in projects:
                self.ProjectsTable.insertRow(row)
                self.ProjectsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(project.name))
                self.ProjectsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(str(project.start_date)))
                self.ProjectsTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(project.due_date)))
                row += 1





#
# def main():
#     app = QApplication(sys.argv)
#     window = HomeWindow(activeUser='po1')
#     window.show()
#     sys.exit(app.exec())
#
#
# if __name__ == "__main__":
#     main()