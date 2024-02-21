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
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QDialog, QMessageBox
from PyQt6.QtCore import QDate
from generated.AddProjectDialog import Ui_AddProjectDialog
from generated.HomeWindow import Ui_HomeWindow
from generated.ViewProjectDialog import Ui_ViewProjectDialog

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



import sys
import datetime



class HomeWindow(QMainWindow, Ui_HomeWindow):
    def __init__(self, activeUser):
        super().__init__()
        self.setupUi(self)
        self.activeUser = activeUser
        self.projectAllTableItemSelected = None

        # Hide pkey for tables
        self.ProjectsOngoingTable.setColumnHidden(0, True)
        self.ProjectsAllTable.setColumnHidden(0, True)
        self.TasksOngoingTable.setColumnHidden(0, True)

        self.populate_projects_ongoing_table()
        self.populate_tasks_ongoing_table()

        self.ProjectsOngoingTable.itemClicked.connect(self.on_project_ongoing_table_item_clicked)

        self.dashButton.clicked.connect(self.on_dash_button)
        self.projectsButton.clicked.connect(self.on_projects_button)
        self.tasksButton.clicked.connect(self.on_tasks_button)

        self.ProjectsAllTable.itemClicked.connect(self.on_project_all_table_item_clicked)
        self.plot_project_gantt_chart()
        self.ProjectsOngoingTable.itemClicked.connect(self.populate_projects_ongoing_table)

        self.AddProjectButton.clicked.connect(self.on_add_project_button)
        self.addCommentButton.clicked.connect(self.on_add_comment_button)
        self.ViewProjectButton.clicked.connect(self.on_view_project_button)




    def populate_projects_ongoing_table(self):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        # project instance
        p = Project()
        projects = p.get_projects_for_team_member(session, self.activeUser)

        # Populate the projects table
        row = 0
        if projects:
            self.ProjectsOngoingTable.setRowCount(0)
            for project in projects:
                self.ProjectsOngoingTable.insertRow(row)
                self.ProjectsOngoingTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(project.project_pkey)))
                self.ProjectsOngoingTable.setItem(row, 1, QtWidgets.QTableWidgetItem(project.name))
                self.ProjectsOngoingTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(project.start_date)))
                self.ProjectsOngoingTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(project.due_date)))
                self.ProjectsOngoingTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(project.status)))
                self.ProjectsOngoingTable.setItem(row, 5, QtWidgets.QTableWidgetItem(str(project.owner.full_name)))
                row += 1


    def populate_tasks_ongoing_table(self):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        # project instance
        t = Task()
        tasks = t.get_tasks_for_team_member(session, self.activeUser)
        # Populate the projects table
        row = 0
        if tasks:
            self.TasksOngoingTable.setRowCount(0)
            for task in tasks:
                self.TasksOngoingTable.insertRow(row)
                self.TasksOngoingTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(task.task_pkey)))
                self.TasksOngoingTable.setItem(row, 1, QtWidgets.QTableWidgetItem(task.name))
                self.TasksOngoingTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(task.start_date)))
                self.TasksOngoingTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(task.due_date)))
                self.TasksOngoingTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(task.status)))
                row += 1


    def on_project_ongoing_table_item_clicked(self, item):
        if item is None:
            self.populate_tasks_ongoing_table()

        else:
            # get project
            row = item.row()
            projectPkey = self.ProjectsOngoingTable.item(row, 0).text()

            #Create a database connection
            db = DatabaseConnection()
            session = db.get_session()
            # project instance
            t = Task()
            tasks = t.get_tasks_for_team_member(session, self.activeUser, int(projectPkey))
            # Populate the projects table
            row = 0
            if tasks:
                self.TasksOngoingTable.setRowCount(0)
                for task in tasks:
                    self.TasksOngoingTable.insertRow(row)
                    self.TasksOngoingTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(task.task_pkey)))
                    self.TasksOngoingTable.setItem(row, 1, QtWidgets.QTableWidgetItem(task.name))
                    self.TasksOngoingTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(task.start_date)))
                    self.TasksOngoingTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(task.due_date)))
                    self.TasksOngoingTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(task.status)))
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


    def populate_projects_all_table(self):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        # project instance
        p = Project()
        projects = p.get_projects(session)

        # Populate the projects table
        row = 0
        if projects:
            self.ProjectsAllTable.setRowCount(0)
            for project in projects:
                self.ProjectsAllTable.insertRow(row)
                self.ProjectsAllTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(project.project_pkey)))
                self.ProjectsAllTable.setItem(row, 1, QtWidgets.QTableWidgetItem(project.name))
                self.ProjectsAllTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(project.start_date)))
                self.ProjectsAllTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(project.due_date)))
                self.ProjectsAllTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(project.end_date)))
                self.ProjectsAllTable.setItem(row, 5, QtWidgets.QTableWidgetItem(str(project.status)))
                self.ProjectsAllTable.setItem(row, 6, QtWidgets.QTableWidgetItem(str(project.owner.full_name)))
                row += 1



    def populate_project_comments(self, projectPkey):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        comLog = CommunicationLog()
        projectLog = comLog.get_project_communication_log(session, projectPkey)
        self.commentListWidget.clear()
        for log in projectLog:
            self.commentListWidget.addItem('')
            self.commentListWidget.addItem(f'Posted: {log.timestamp}, User: {log.user.full_name} \n {log.comment} ')


    def on_add_comment_button(self):
        # Create a session
        db = DatabaseConnection()
        session = db.get_session()

        # get user fkey
        user = User()
        userFkey = user.get_user_fkey(session, self.activeUser)

        # get project fkey
        projectFkey = self.projectAllTableItemSelected

        commentToAdd = self.newCommentTE.toPlainText()

        # add comment
        new_comment = CommunicationLog(user_fkey=userFkey, project_fkey=projectFkey, task_fkey=-1, comment=commentToAdd,
                                       timestamp=datetime.datetime.now())
        addComment = new_comment.add_project_comment(session)

        if addComment == 'successful':
            #self.addProjectStatusLabel.setText(f'The project, {Pname}! has now been added.')
            self.populate_project_comments(projectPkey=projectFkey)
            self.newCommentTE.clear()

        else:
            print(addComment)
            #self.addProjectStatusLabel.setText(addProject)



    def on_project_all_table_item_clicked(self, item):
        # get project name
        row = item.row()
        project = self.ProjectsAllTable.item(row, 0).text()
        self.projectAllTableItemSelected = int(project)
        self.populate_project_comments(int(project))

        # set button to enable
        self.ViewProjectButton.setEnabled(True)


    def on_dash_button(self):
        self.stackedWidget.setCurrentIndex(0)
        self.populate_projects_ongoing_table()
        self.populate_tasks_ongoing_table()
        self.plot_project_gantt_chart()


    def on_projects_button(self):
        self.stackedWidget.setCurrentIndex(1)
        self.commentListWidget.clear()
        self.populate_projects_all_table()

    def on_tasks_button(self):
        self.stackedWidget.setCurrentIndex(2)

    def on_add_project_button(self):
        self.add_project_window = AddProject(self, activeUser=self.activeUser)
        self.add_project_window.show()

    def on_view_project_button(self):
        projectPk = self.projectAllTableItemSelected
        self.view_project_window = ViewProject(self, projectPkey=projectPk, activeUser=self.activeUser)
        self.view_project_window.show()



class AddProject(QDialog, Ui_AddProjectDialog):
    def __init__(self, home_window_instance, activeUser):
        super().__init__()
        self.setupUi(self)
        self.activeUser = activeUser
        self.home_window_instance = home_window_instance
        self.addProjectButton.clicked.connect(self.on_add_project_button)

        #set date defaults
        self.projectStartDE.setDate(QDate.currentDate())
        self.projectDueDE.setDate(QDate.currentDate())

    def on_add_project_button(self):
        # input from window
        Pname = self.projectNameLE.text()
        Pdesc = self.projectDescTE.toPlainText()
        Pstatus = self.projectStatusCB.currentText()

        startDate = self.projectStartDE.date()
        startDateDT = datetime.date(startDate.year(), startDate.month(), startDate.day())
        Pstart = datetime.datetime.strptime(str(startDateDT), '%Y-%m-%d')

        dueDate = self.projectDueDE.date()
        dueDateDT = datetime.date(dueDate.year(), dueDate.month(), dueDate.day())
        Pdue = datetime.datetime.strptime(str(dueDateDT), '%Y-%m-%d')

        # Create a session
        db = DatabaseConnection()
        session = db.get_session()
        # get owner fkey
        owner = User()
        ownerfkey = owner.get_user_fkey(session, self.activeUser)

        # db session
        dbCon = DatabaseConnection()
        session = dbCon.get_session()

        # Create a new project instance
        new_project = Project(name=Pname, desc=Pdesc, start_date=Pstart, due_date=Pdue, status=Pstatus,
                              owner_fkey=ownerfkey, is_removed=0)
        # add project to db
        addProject = new_project.add_project(session)

        if addProject == 'successful':
            self.addProjectStatusLabel.setText(f'The project, {Pname}! has now been added.')
            self.home_window_instance.populate_projects_all_table()

            # disable fields
            self.projectNameLE.setEnabled(False)
            self.projectDescTE.setEnabled(False)
            self.projectStatusCB.setEnabled(False)
            self.projectStartDE.setEnabled(False)
            self.projectDueDE.setEnabled(False)
            self.addProjectButton.setEnabled(False)
            self.exitProjectButton.setEnabled(False)
        else:
            self.addProjectStatusLabel.setText(addProject)



class ViewProject(QDialog, Ui_ViewProjectDialog):
    def __init__(self, home_window_instance, projectPkey, activeUser):
        super().__init__()
        self.setupUi(self)
        self.home_window_instance = home_window_instance
        self.projectPkey = projectPkey
        self.activeUser = activeUser
        self.populate_project()
        self.populate_team_members_table()
        self.deleteProjectButton.clicked.connect(self.on_delete_project)
        self.saveChangesButton.clicked.connect(self.on_save_changes)

    def populate_project(self):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        # project instance
        p = Project()
        projectSelected = p.get_project(session, self.projectPkey)
        for project in projectSelected:
            self.projectNameLE.setText(project.name)
            self.projectDescTE.setText(project.desc)
            self.projectStatusCB.setCurrentText(project.status)
            self.projectStartDE.setDate(project.start_date)
            self.projectDueDE.setDate(project.due_date)
            if project.end_date:
                self.projectEndDE.setDate(project.end_date)
            else:
                self.projectEndDE.setDate(QDate())
            self.projectOwnerLE.setText(project.owner.full_name)

    def populate_team_members_table(self):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        # project team instance
        pt = ProjectTeam()
        teamMembers = pt.get_team_of_project(session, self.projectPkey)

        # Populate the projects table
        row = 0
        if teamMembers:
            self.TeamMembersTable.setRowCount(0)
            for teamMember in teamMembers:
                self.TeamMembersTable.insertRow(row)
                self.TeamMembersTable.setItem(row, 0, QtWidgets.QTableWidgetItem(teamMember.user.username))
                self.TeamMembersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(teamMember.user.full_name))
                self.TeamMembersTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(teamMember.start_date)))
                row += 1


    def on_delete_project(self):
        confirmation = QMessageBox.question(self, "Confirm Deletion",
                                            "Are you sure you want to delete this project?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.StandardButton.Yes:
            # Proceed with deletion
            # Create a database connection
            db = DatabaseConnection()
            session = db.get_session()
            # project instance
            p = Project()
            projects = p.get_project(session, self.projectPkey)
            for project in projects:
                projectName = project.name
            projectDelete = p.delete_project(session, self.projectPkey)
            if projectDelete == 'Project deleted successfully':
                self.projectChangesLabel.setText(f'The project, {projectName}! has now been removed.')
                self.home_window_instance.populate_projects_all_table()

                #disable fields after deletion
                self.projectNameLE.setEnabled(False)
                self.projectDescTE.setEnabled(False)
                self.projectStatusCB.setEnabled(False)
                self.projectStartDE.setEnabled(False)
                self.projectDueDE.setEnabled(False)
                self.projectEndDE.setEnabled(False)
                self.projectOwnerLE.setEnabled(False)
                self.saveChangesButton.setEnabled(False)
                self.exitWithoutSavingButton.setEnabled(False)
                self.closeProjectButton.setEnabled(False)
                self.deleteProjectButton.setEnabled(False)
                self.TeamMembersTable.setEnabled(False)
                self.addMemberButton.setEnabled(False)
                self.removeMemberButton.setEnabled(False)

            else:
                return projectDelete
        else:
            # Cancelled by the user
            return

    def on_save_changes(self):
        currentName = self.projectNameLE.text()
        currentDesc = self.projectDescTE.toPlainText()
        currentStatus = self.projectStatusCB.currentText()

        currentStartDate = self.projectStartDE.date()
        startDateDT = datetime.date(currentStartDate.year(), currentStartDate.month(), currentStartDate.day())
        Pstart = datetime.datetime.strptime(str(startDateDT), '%Y-%m-%d')

        currentEndDate = self.projectEndDE.date()
        endDateDT = datetime.date(currentEndDate.year(), currentEndDate.month(), currentEndDate.day())
        Pend = datetime.datetime.strptime(str(endDateDT), '%Y-%m-%d')

        currentDueDate = self.projectDueDE.date()
        dueDateDT = datetime.date(currentDueDate.year(), currentDueDate.month(), currentDueDate.day())
        Pdue = datetime.datetime.strptime(str(dueDateDT), '%Y-%m-%d')

        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        p = Project()
        updateProject = p.set_project(session, self.projectPkey, currentName, currentDesc,
                                      currentStatus, Pstart, Pend, Pdue)

        if updateProject:
            print('updated')
            self.projectChangesLabel.setText(f'The project, {currentName}! has now been updated.')
            self.home_window_instance.populate_projects_all_table()
        else:
            self.projectChangesLabel.setText(updateProject)










def main():
    app = QApplication(sys.argv)
    window = HomeWindow(activeUser='tm1')
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()