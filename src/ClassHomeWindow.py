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
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from generated.HomeWindow import Ui_HomeWindow

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas




import sys



class HomeWindow(QMainWindow, Ui_HomeWindow):
    def __init__(self, activeUser):
        super().__init__()
        self.setupUi(self)
        self.activeUser = activeUser
        self.populate_projects_table()
        self.populate_tasks_table()
        #self.ProjectsTable.setEditTriggers(QtWidgets.QAbstractItemView.editTriggers.NoEditTriggers)

        #self.TasksTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ProjectsTable.itemClicked.connect(self.on_project_table_item_clicked)
        self.dashButton.clicked.connect(self.on_dash_button)
        self.projectsButton.clicked.connect(self.on_projects_button)

        self.plot_project_gantt_chart()



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
            self.ProjectsTable.setRowCount(0)
            for project in projects:
                self.ProjectsTable.insertRow(row)
                self.ProjectsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(project.name))
                self.ProjectsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(str(project.start_date)))
                self.ProjectsTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(project.due_date)))
                self.ProjectsTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(project.owner.full_name)))

                row += 1


    def populate_tasks_table(self):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        # project instance
        t = Task()
        tasks = t.get_tasks_for_team_member(session, self.activeUser)
        # Populate the projects table
        row = 0
        if tasks:
            self.TasksTable.setRowCount(0)
            for task in tasks:
                self.TasksTable.insertRow(row)
                self.TasksTable.setItem(row, 0, QtWidgets.QTableWidgetItem(task.name))
                self.TasksTable.setItem(row, 1, QtWidgets.QTableWidgetItem(str(task.start_date)))
                self.TasksTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(task.due_date)))
                row += 1


    def on_project_table_item_clicked(self, item):
        # get project name
        row = item.row()
        project = self.ProjectsTable.item(row, 0).text()

        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        # project instance
        t = Task()
        tasks = t.get_tasks_for_team_member(session, self.activeUser, project)
        # Populate the projects table
        row = 0
        if tasks:
            self.TasksTable.setRowCount(0)
            for task in tasks:
                self.TasksTable.insertRow(row)
                self.TasksTable.setItem(row, 0, QtWidgets.QTableWidgetItem(task.name))
                self.TasksTable.setItem(row, 1, QtWidgets.QTableWidgetItem(str(task.start_date)))
                self.TasksTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(task.due_date)))
                row += 1

    def plot_project_gantt_chart(self):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        # project instance
        p = Project()
        projects = p.get_projects_for_team_member(session, self.activeUser)

        # data for plotting
        project_names = [project.name for project in projects]
        start_dates = [project.start_date for project in projects]
        due_dates = [project.due_date for project in projects]

        # Plot Gantt chart
        fig, ax = plt.subplots(figsize=(5, 3))
        for idx, project_name in enumerate(project_names):
            print(type(due_dates[idx]))
            ax.barh(project_name, due_dates[idx], left=start_dates[idx], color='skyblue')
        ax.set_xlabel('Date')
        ax.set_ylabel('Project')
        ax.set_title('Gantt Chart')
        ax.grid(True)
        plt.tight_layout()

        # Embed Gantt chart
        canvas = FigureCanvas(fig)
        layout = QVBoxLayout(self.projectPlotFrame)
        layout.addWidget(canvas)



    def on_dash_button(self):
        self.stackedWidget.setCurrentIndex(0)

    def on_projects_button(self):
        self.stackedWidget.setCurrentIndex(1)






def main():
    app = QApplication(sys.argv)
    window = HomeWindow(activeUser='tm1')
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()