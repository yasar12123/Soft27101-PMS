from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassEmail import EmailSender
from src.ClassUser import User
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTeam import Team
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment
from src.ClassTimelineEvent import TimelineEvent

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QDialog, QMessageBox, QSizePolicy, QLabel
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QColor
from generated.AddProjectDialog import Ui_AddProjectDialog
from generated.HomeWindow import Ui_HomeWindow
from generated.ViewProjectDialog import Ui_ViewProjectDialog
from generated.ViewTaskDialog import Ui_ViewTaskDialog
from generated.AddTaskDialog import Ui_AddTaskDialog
from generated.ViewProjectAddTeamMemberDialog import Ui_ViewProjectAddTeamMemberDialog

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import datetime
from datetime import datetime as dt
import threading


class HomeWindow(QMainWindow, Ui_HomeWindow):
    def __init__(self, activeUserInstance):
        super().__init__()
        self.setupUi(self)
        self.activeUserInstance = activeUserInstance
        self.projectNameItemSelected = None
        self.projectItemSelected = None
        self.taskItemSelected = None

        # database connection
        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()

        # Hide pkey for tables
        self.ProjectsOngoingTable.setColumnHidden(0, True)
        self.ProjectsAllTable.setColumnHidden(0, True)
        self.TasksOngoingTable.setColumnHidden(0, True)
        self.TasksOngoingTable.setColumnHidden(5, True)
        self.TaskAllTable.setColumnHidden(0, True)
        self.TaskAllTable.setColumnHidden(2, True)
        self.taskProjectTable.setColumnHidden(0, True)

        # menu
        self.dashButton.clicked.connect(self.on_dash_button)
        self.projectsButton.clicked.connect(self.on_projects_button)
        self.tasksButton.clicked.connect(self.on_tasks_button)
        self.profileButton.clicked.connect(self.on_profile_button)
        self.logOutButton.clicked.connect(self.on_logOut_button)

        # load on start
        self.on_dash_button()
        self.populate_projects_all_table_thread()

        # dash functions
        self.dashViewProjectButton.clicked.connect(self.on_go_to_project_button)
        self.dashViewTaskButton.clicked.connect(self.on_go_to_task_button)
        self.ProjectsOngoingTable.itemClicked.connect(self.on_project_ongoing_table_item_clicked)
        self.TasksOngoingTable.itemClicked.connect(self.on_task_ongoing_table_item_clicked)


        # project function
        self.AddProjectButton.clicked.connect(self.on_add_project_button)
        self.ViewProjectButton.clicked.connect(self.on_view_project_button)
        self.addCommentButton.clicked.connect(self.on_add_project_comment_button)
        self.ProjectsAllTable.itemClicked.connect(self.on_project_all_table_item_clicked)


        # task functions
        self.ViewTaskButton.clicked.connect(self.on_view_task_button)
        self.AddTaskButton.clicked.connect(self.on_add_task_button)
        self.addTaskCommentButton.clicked.connect(self.on_add_task_comment_button)
        self.viewProjectButtonB.clicked.connect(self.on_view_project_button)
        self.taskProjectTable.itemClicked.connect(self.on_task_project_all_table_item_clicked)
        self.TaskAllTable.itemClicked.connect(self.on_task_table_item_clicked)


        # profile - On button click
        self.changeDetailsButton.clicked.connect(self.on_change_personal_details_button)
        self.changePasswordRB.clicked.connect(self.on_change_password_radio_button)
        self.notChangePasswordRB.clicked.connect(self.on_not_change_password_radio_button)
        self.accountDeleteRB.clicked.connect(self.on_account_deletion_understand_button)
        self.accountDoNotDeleteRB.clicked.connect(self.on_account_deletion_cancel_button)
        self.updateDetailsButton.clicked.connect(self.on_update_details_button)
        self.request_password_change = False
        self.accountDeleteButton.clicked.connect(self.on_account_deletion_button)




    # dashboard page functions
    def on_dash_button(self):
        # Switch to the dashboard page
        self.stackedWidget.setCurrentIndex(0)

        #disable buttons
        self.dashViewProjectButton.setEnabled(False)
        self.dashViewTaskButton.setEnabled(False)

        # thread project ongoing and tasks table
        project_thread = threading.Thread(target=self.populate_projects_ongoing_table)
        task_thread = threading.Thread(target=self.populate_tasks_ongoing_table)
        project_thread.start()
        task_thread.start()

        # other funcs
        self.display_stat_counts()

    def display_stat_counts(self):
        t = Task()
        tasks = t.get_tasks_for_team_member(self.session, self.activeUserInstance.username)
        projects = sum(1 for task in tasks if task.project_fkey)
        completed_tasks = sum(1 for task in tasks if task.status == 'Completed')
        in_progress_tasks = sum(1 for task in tasks if task.status == 'In-Progress')
        not_started_tasks = sum(1 for task in tasks if task.status == 'Not Started')
        pending_review_tasks = sum(1 for task in tasks if task.status == 'Pending Review')

        layout = QVBoxLayout(self.statsFrame)

        # Add labels for task counts
        project_label = QLabel(f'No of Projects: {projects}')
        layout.addWidget(project_label)

        completed_label = QLabel(f'Tasks Completed: {completed_tasks}')
        layout.addWidget(completed_label)

        in_progress_label = QLabel(f'Tasks In-Progress: {in_progress_tasks}')
        layout.addWidget(in_progress_label)

        not_started_label = QLabel(f'Tasks Not Started: {not_started_tasks}')
        layout.addWidget(not_started_label)

        pending_review_label = QLabel(f'Tasks Pending Review: {pending_review_tasks}')
        layout.addWidget(pending_review_label)

        # Set size policy to automatically adjust size
        self.statsFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def populate_projects_ongoing_table(self):
        # project instance
        p = Project()
        projects = p.get_projects_for_team_member(self.session, self.activeUserInstance.username, completed='n')

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

    def populate_tasks_ongoing_table(self, projectPkey=None):
        #clear table
        self.TasksOngoingTable.setRowCount(0)

        # task instance
        t = Task()
        if projectPkey:
            tasks = t.get_tasks_for_team_member(self.session, self.activeUserInstance.username, project_fkey=projectPkey)
        else:
            tasks = t.get_tasks_for_team_member(self.session, self.activeUserInstance.username)
        # Populate the tasks table

        if tasks:
            self.TasksOngoingTable.setRowCount(0)
            row = 0
            for task in tasks:
                self.TasksOngoingTable.insertRow(row)
                self.TasksOngoingTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(task.task_pkey)))
                self.TasksOngoingTable.setItem(row, 1, QtWidgets.QTableWidgetItem(task.name))
                self.TasksOngoingTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(task.start_date)))
                self.TasksOngoingTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(task.due_date)))
                self.TasksOngoingTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(task.status)))
                self.TasksOngoingTable.setItem(row, 5, QtWidgets.QTableWidgetItem(str(task.project_fkey)))
                row += 1

    def on_project_ongoing_table_item_clicked(self, item):
        if item:
            # get project pkey of row selected
            row = item.row()
            #set selected project
            projectPkey = self.ProjectsOngoingTable.item(row, 0).text()
            self.projectItemSelected = int(projectPkey)
            self.projectNameItemSelected = self.ProjectsOngoingTable.item(row, 1).text()

            # enable button
            self.dashViewProjectButton.setEnabled(True)

            # populate tasks table
            self.populate_tasks_ongoing_table(projectPkey=int(projectPkey))

    def on_task_ongoing_table_item_clicked(self, item):
        if item:
            # set task instance pkey of row selected
            row = item.row()
            self.taskItemSelected = int(self.TasksOngoingTable.item(row, 0).text())
            self.projectItemSelected = int(self.TasksOngoingTable.item(row, 5).text())

            # enable button
            self.dashViewTaskButton.setEnabled(True)

    def on_go_to_project_button(self):
        # Switch to the projects page
        self.on_projects_button()

        # find a select the project in the project table
        for row in range(self.ProjectsAllTable.rowCount()):
            # Get the value of the pkey in the table
            item = self.ProjectsAllTable.item(row, 0)
            # if the value matches then select the row
            if item is not None and item.text() == str(self.projectItemSelected):
                # Select the row if the value matches
                self.ProjectsAllTable.selectRow(row)
                self.ProjectsAllTable.itemClicked.emit(item)

    def on_go_to_task_button(self):
        # Switch to the tasks page
        self.on_tasks_button()

        # find and select row in the projects table
        for row in range(self.taskProjectTable.rowCount()):
            # Get the value of the pkey in the table
            item = self.taskProjectTable.item(row, 0)
            if item is not None and item.text() == str(self.projectItemSelected):
                # Select the row if the value matches
                self.taskProjectTable.selectRow(row)
                self.taskProjectTable.itemClicked.emit(item)

        # find and select row in the tasks table
        for row in range(self.TaskAllTable.rowCount()):
            # Get the value of the pkey in the table
            item = self.TaskAllTable.item(row, 2)
            if item is not None and item.text() == str(self.taskItemSelected):
                # Select the row if the value matches
                self.TaskAllTable.selectRow(row)
                self.TaskAllTable.itemClicked.emit(item)



    # project page functions
    def on_projects_button(self):
        # switch to project page
        self.stackedWidget.setCurrentIndex(1)
        # clear the comments
        self.commentListWidget.clear()
        # disable button
        self.ViewProjectButton.setEnabled(False)
        # load all projects using threading
        self.populate_projects_all_table_thread()

    def populate_projects_all_table(self):
        # project instance
        p = Project()
        projects = p.get_projects(self.session)

        # Populate the projects table
        if projects:
            # set row number and increment within for loop
            row = 0
            # clear projects table
            self.ProjectsAllTable.setRowCount(0)
            # load data into table
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

    def populate_projects_all_table_thread(self):
        # Create threads for populating project all table
        populate_projects_all_thread = threading.Thread(target=self.populate_projects_all_table)
        populate_projects_all_thread.start()

    def populate_project_comments(self, projectPkey):
        # get project communication log
        comLog = CommunicationLog()
        projectLog = comLog.get_project_communication_log(self.session, projectPkey)
        # Sort the projectLog list by timestamp
        projectLog.sort(key=lambda log: log.timestamp, reverse=True)
        # clear comments list
        self.commentListWidget.clear()
        # load project comments
        for log in projectLog:
            # add new line to space out comments
            timestamp = log.timestamp.strftime('%d/%m/%Y %H:%M:%S')
            self.commentListWidget.addItem('\n')
            self.commentListWidget.addItem(f'Posted: {timestamp}, User: {log.user.full_name} \n {log.comment} ')

    def on_add_project_comment_button(self):
        # get comment text
        commentToAdd = self.newCommentTE.toPlainText()

        # new comment
        new_comment = CommunicationLog(user_fkey=self.activeUserInstance.user_pkey, project_fkey=self.projectItemSelected,
                                       task_fkey=-1, comment=commentToAdd, timestamp=datetime.datetime.now())
        # add comment
        addComment = new_comment.add_comment(self.session)

        if addComment == 'successful':
            # populate comments via thread
            project_comments_thread = threading.Thread(target=self.populate_project_comments(projectPkey=self.projectItemSelected))
            project_comments_thread.start()
            # clear comment box
            self.newCommentTE.clear()
        else:
            return addComment

    def on_project_all_table_item_clicked(self, item):
        if item:
            # set project fkey and name
            row = item.row()
            self.projectItemSelected = int(self.ProjectsAllTable.item(row, 0).text())
            self.projectNameItemSelected = self.ProjectsAllTable.item(row, 1).text()

            # set button to enable
            self.ViewProjectButton.setEnabled(True)

            # populate comments via threading
            project_comments_thread = threading.Thread(target=self.populate_project_comments(self.projectItemSelected))
            project_comments_thread.start()

    def on_add_project_button(self):
        # open add project class
        self.add_project_window = AddProject(self, activeUserInstance=self.activeUserInstance)
        self.add_project_window.show()





    # task page functions
    def on_tasks_button(self):
        # switch Tasks page
        self.stackedWidget.setCurrentIndex(2)

        # disable buttons
        self.viewProjectButtonB.setEnabled(False)
        self.ViewTaskButton.setEnabled(False)
        self.AddTaskButton.setEnabled(False)
        self.addTaskCommentButton.setEnabled(False)

        # clear comments and task table
        self.taskCommentListWidget.clear()
        self.TaskAllTable.setRowCount(0)

        # Create thread for populating task project table
        populate_task_project_thread = threading.Thread(target=self.populate_task_project_table)
        populate_task_project_thread.start()

        # Create thread for populating task project table
        populate_task_thread = threading.Thread(target=self.populate_task_all_table(projectPKEY=-1))
        populate_task_thread.start()

    def populate_task_project_table(self):
        # project instance
        p = Project()
        projects = p.get_projects(self.session)

        # Populate the projects table
        if projects:
            row = 0
            self.taskProjectTable.setRowCount(0)
            for project in projects:
                self.taskProjectTable.insertRow(row)
                self.taskProjectTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(project.project_pkey)))
                self.taskProjectTable.setItem(row, 1, QtWidgets.QTableWidgetItem(project.name))

    def populate_task_all_table(self, projectPKEY):
        #clear table
        self.TaskAllTable.setRowCount(0)

        # get all tasks for project
        t = Task()
        tasks = t.get_tasks(self.session, projectPKEY)

        # Populate the tasks table
        if tasks:
            row = 0
            self.TaskAllTable.setRowCount(0)
            for task in tasks:
                self.TaskAllTable.insertRow(row)
                self.TaskAllTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(task.project_fkey)))
                self.TaskAllTable.setItem(row, 1, QtWidgets.QTableWidgetItem(task.project.name))
                self.TaskAllTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(task.task_pkey)))
                self.TaskAllTable.setItem(row, 3, QtWidgets.QTableWidgetItem(task.name))
                self.TaskAllTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(task.start_date)))
                self.TaskAllTable.setItem(row, 5, QtWidgets.QTableWidgetItem(task.status))
                self.TaskAllTable.setItem(row, 6, QtWidgets.QTableWidgetItem(str(task.due_date)))
                self.TaskAllTable.setItem(row, 7, QtWidgets.QTableWidgetItem(str(task.end_date)))
                self.TaskAllTable.setItem(row, 8, QtWidgets.QTableWidgetItem(task.assignee.full_name))
                self.TaskAllTable.setItem(row, 9, QtWidgets.QTableWidgetItem(task.assigner.full_name))
                row += 1

    def on_task_project_all_table_item_clicked(self, item):
        if item:
            # clear task comments table
            self.taskCommentListWidget.clear()

            # set project pkey
            row = item.row()
            self.projectItemSelected = int(self.taskProjectTable.item(row, 0).text())
            self.projectNameItemSelected = self.taskProjectTable.item(row, 1).text()

            # populate tasks table via threading
            task_all_table_thread = threading.Thread(target=self.populate_task_all_table(projectPKEY=self.projectItemSelected))
            task_all_table_thread.start()

            # enable buttons
            self.AddTaskButton.setEnabled(True)
            self.viewProjectButtonB.setEnabled(True)

            # disable button
            self.ViewTaskButton.setEnabled(False)
            self.addTaskCommentButton.setEnabled(False)

    def populate_task_comments(self, taskPkey):
        # get task communication log
        comLog = CommunicationLog()
        taskLog = comLog.get_task_communication_log(self.session, taskPkey)

        # Sort the taskLog list by timestamp
        taskLog.sort(key=lambda log: log.timestamp, reverse=True)

        # clear task comment list
        self.taskCommentListWidget.clear()

        # load in comments
        for log in taskLog:
            timestamp = log.timestamp.strftime('%d/%m/%Y %H:%M:%S')
            self.taskCommentListWidget.addItem('\n')
            self.taskCommentListWidget.addItem(f'Posted: {timestamp}, User: {log.user.full_name} \n {log.comment} ')

    def on_task_table_item_clicked(self, item):
        if item:
            # set project fkey
            row = item.row()
            self.projectItemSelected = int(self.TaskAllTable.item(row, 0).text())
            self.projectNameItemSelected = self.TaskAllTable.item(row, 1).text()
            self.taskItemSelected = int(self.TaskAllTable.item(row, 2).text())

            # thread task comments
            task_comment_thread = threading.Thread(target=self.populate_task_comments(taskPkey=self.taskItemSelected))
            task_comment_thread.start()

            # enable buttons
            self.ViewTaskButton.setEnabled(True)
            self.addTaskCommentButton.setEnabled(True)

    def on_add_task_comment_button(self):
        # get comment text
        commentToAdd = self.newTaskCommentTE.toPlainText()

        # new comment to add
        new_comment = CommunicationLog(user_fkey=self.activeUserInstance.user_pkey,
                                       project_fkey=self.projectItemSelected,
                                       task_fkey=self.taskItemSelected, comment=commentToAdd,
                                       timestamp=datetime.datetime.now())
        # add comment to db
        addComment = new_comment.add_comment(self.session)

        if addComment == 'successful':
            # thread task comments
            task_comment_thread = threading.Thread(target=self.populate_task_comments(taskPkey=self.taskItemSelected))
            task_comment_thread.start()

            # clear comment box
            self.newTaskCommentTE.clear()
        else:
            return addComment

    def on_add_task_button(self):
        # on add task class window
        self.add_task_window = AddTask(self, projectName=self.projectNameItemSelected,
                                       projectPkey=self.projectItemSelected,
                                       activeUserInstance=self.activeUserInstance)
        self.add_task_window.show()



    # on view project and task buttons
    def on_view_project_button(self):
        projectPk = self.projectItemSelected
        self.view_project_window = ViewProject(self, project_pkey=projectPk, activeUserInstance=self.activeUserInstance)
        self.view_project_window.show()

    def on_view_task_button(self):
        task_pkey = self.taskItemSelected
        self.view_task_window = ViewTask(self, project_pkey=self.projectItemSelected, task_pkey=task_pkey,
                                         activeUserInstance=self.activeUserInstance)
        self.view_task_window.show()


    # log out func and confirmation box
    def confirmation_box(self, title, display_text):
        if title and display_text:
            confirmation = QMessageBox.question(self, title, display_text,
                                                QMessageBox.StandardButton.Yes |
                                                QMessageBox.StandardButton.No)
            return confirmation

    def on_logOut_button(self):
        confirmation = self.confirmation_box('Confirm logging out', 'Are you sure you want to log out?')
        if confirmation == QMessageBox.StandardButton.Yes:
            self.close()



    # profile page functions
    def on_profile_button(self):
        self.stackedWidget.setCurrentIndex(3)
        self.on_profile_load_defaults()
        self.populate_profile_details()

    def on_profile_load_defaults(self):
        self.changeDetailsButton.setText('Change Details')
        self.newPasswordLabel.setText('Password: ')
        self.accountDeleteButton.hide()
        self.pdNameLE.setEnabled(False)
        self.pdEmailLE.setEnabled(False)
        self.pdUsernameLE.setEnabled(False)
        self.pdPasswordLE.setEnabled(False)
        self.updateDetailsButton.setEnabled(False)
        self.changePasswordRB.setChecked(False)
        self.changePasswordRB.hide()
        self.notChangePasswordRB.setChecked(False)
        self.notChangePasswordRB.hide()
        self.updateDetailsButton.hide()
        self.accountDoNotDeleteRB.setChecked(True)
        self.request_password_change = False
        self.pdPasswordLE.setText('**********')

    def on_change_password_radio_button(self):
        self.pdPasswordLE.setEnabled(True)
        self.pdPasswordLE.clear()
        self.newPasswordLabel.setText('Input New Password: ')
        self.request_password_change = True
        self.notChangePasswordRB.show()

    def on_not_change_password_radio_button(self):
        self.pdPasswordLE.setEnabled(False)
        self.request_password_change = False
        self.newPasswordLabel.setText('Password: ')
        self.pdPasswordLE.setText('**********')

    def on_change_personal_details_button(self):
        if self.changeDetailsButton.text() == 'Change Details':
            self.pdNameLE.setEnabled(True)
            self.pdEmailLE.setEnabled(True)
            self.pdUsernameLE.setEnabled(True)
            self.updateDetailsButton.setEnabled(True)
            self.updateDetailsButton.show()
            self.changePasswordRB.show()
            self.changeDetailsButton.setText('Discard Changes')
        else:
            self.on_profile_load_defaults()
            self.populate_profile_details()

    def populate_profile_details(self):
        self.pdNameLE.setText(self.activeUserInstance.full_name)
        self.pdEmailLE.setText(self.activeUserInstance.email_address)
        self.pdUsernameLE.setText(self.activeUserInstance.username)
        self.pdPasswordLE.setText('**********')

    def on_account_deletion_understand_button(self):
        self.accountDeleteButton.show()

    def on_account_deletion_cancel_button(self):
        self.accountDeleteButton.hide()
        self.accountDoNotDeleteRB.setChecked(True)

    def on_update_details_button(self):
        user_pkey = self.activeUserInstance.user_pkey
        name = self.pdNameLE.text()
        emailAdd = self.pdEmailLE.text()
        username = self.pdUsernameLE.text()
        password = self.pdPasswordLE.text()

        #if password not changed
        if self.request_password_change is False:
            set_user = self.activeUserInstance.set_user(self.session, user_pkey=user_pkey,
                                                        setFullname=name, setEmailAddress=emailAdd,
                                                        setUsername=username)
            self.updateStatusLabel.setText(set_user)
            self.on_profile_load_defaults()

        # if password changed
        if self.request_password_change is True:
            set_user = self.activeUserInstance.set_user(self.session, user_pkey=user_pkey,
                                                        setFullname=name, setEmailAddress=emailAdd,
                                                        setUsername=username, setPassword=password)
            self.updateStatusLabel.setText(set_user)
            self.on_profile_load_defaults()


    def on_account_deletion_button(self):
        confirmation = self.confirmation_box('Confirm deletion', 'Are you sure you want to delete your account?')
        if confirmation == QMessageBox.StandardButton.Yes:
            t = Task()
            remove_from_tasks = t.unassign_tasks(self.session, self.activeUserInstance.user_pkey)
            self.deleteStatusLabel.setText(remove_from_tasks)

            p = Project()
            remove_from_projects = p.unassign_projects(self.session, self.activeUserInstance.user_pkey)
            self.deleteStatusLabel.setText(remove_from_projects)

            pt=ProjectTeam()
            delete_from_teams = pt.delete_team_member_from_projects(self.session, self.activeUserInstance.user_pkey)
            self.deleteStatusLabel.setText(delete_from_teams)

            delete_user = self.activeUserInstance.delete_user(self.session, self.activeUserInstance.user_pkey)
            self.deleteStatusLabel.setText(delete_user)
            self.close()


class AddProject(QDialog, Ui_AddProjectDialog):
    def __init__(self, home_window_instance, activeUserInstance):
        super().__init__()
        self.setupUi(self)
        self.activeUserInstance = activeUserInstance
        self.field_changed = False
        self.home_window_instance = home_window_instance

        # database connection
        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()

        # buttons
        self.addProjectButton.clicked.connect(self.on_add_project_button)
        self.exitProjectButton.clicked.connect(self.on_exit_without_save)

        #set date defaults
        self.projectStartDE.setDate(QDate.currentDate())
        self.projectDueDE.setDate(QDate.currentDate())

        #check if fields have changed
        self.projectNameLE.textChanged.connect(self.on_field_changed)
        self.projectDescTE.textChanged.connect(self.on_field_changed)
        self.projectStatusCB.currentTextChanged.connect(self.on_field_changed)
        self.projectStartDE.dateChanged.connect(self.on_field_changed)
        self.projectDueDE.dateChanged.connect(self.on_field_changed)

        # disable button
        self.addProjectButton.setEnabled(False)

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

        # get owner fkey
        ownerfkey = self.activeUserInstance.user_pkey

        # Create a new project instance
        new_project = Project(name=Pname, desc=Pdesc, start_date=Pstart, due_date=Pdue, status=Pstatus,
                              owner_fkey=ownerfkey, is_removed=0)

        # add project to db
        addProject = new_project.add_project(self.session, ownerfkey)

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
            self.exitProjectButton.setText('Exit')

            #log event of creation
            event = TimelineEvent()
            addEvent = event.log_project_creation(self.session, new_project)

        else:
            self.addProjectStatusLabel.setText(addProject)

    def on_exit_without_save(self):
        if self.exitProjectButton.text() == 'Exit':
            self.close()
        else:
            confirmation = QMessageBox.question(self, "Confirm exit",
                                                "Are you sure you want to exit without adding the project?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                self.close()

    def on_field_changed(self):
        self.field_changed = True
        self.addProjectButton.setEnabled(True)
        self.exitProjectButton.setText('Exit (without saving')




class AddTask(QDialog, Ui_AddTaskDialog):
    def __init__(self, home_window_instance, projectName, projectPkey, activeUserInstance):
        super().__init__()
        self.setupUi(self)
        self.activeUserInstance = activeUserInstance
        self.projectName = projectName
        self.projectPkey = projectPkey
        self.field_changed = False
        self.home_window_instance = home_window_instance

        # database connection
        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()

        #thread assign to field populate
        populate_assign_to_thread = threading.Thread(target=self.populate_assign_to)
        populate_assign_to_thread.start()

        # buttons
        self.addTaskButton.clicked.connect(self.on_add_task_button)
        self.exitTaskButton.clicked.connect(self.on_exit_without_save)

        #set date defaults
        self.taskStartDE.setDate(QDate.currentDate())
        self.taskDueDE.setDate(QDate.currentDate())

        #set project name
        self.projectNameLE.setText(projectName)

        #check if fields have changed
        self.taskNameLE.textChanged.connect(self.on_field_changed)
        self.taskDescTE.textChanged.connect(self.on_field_changed)
        self.taskStatusCB.currentTextChanged.connect(self.on_field_changed)
        self.taskStartDE.dateChanged.connect(self.on_field_changed)
        self.taskDueDE.dateChanged.connect(self.on_field_changed)

        # disable button
        self.addTaskButton.setEnabled(False)

    def populate_assign_to(self):
        pt = ProjectTeam()
        project = pt.get_team_of_project(self.session, self.projectPkey)

        for user in project:
            item_text = f'{user.user.full_name} ({user.user.username})'
            item_data = user.user.user_pkey
            self.AssignToCB.addItem(item_text, item_data)

    def on_add_task_button(self):
        # get assignee fkey
        if self.AssignToCB.currentIndex() == -1:
            assignee_fkey = -1
        else:
            AssignToCBIndex = self.AssignToCB.currentIndex()
            assignee_fkey = int(self.AssignToCB.itemData(AssignToCBIndex))

        # get assigner fkey
        assignerfkey = self.activeUserInstance.user_pkey

        # input from window
        Tname = self.taskNameLE.text()
        Tdesc = self.taskDescTE.toPlainText()
        Tstatus = self.taskStatusCB.currentText()
        startDate = self.taskStartDE.date()
        startDateDT = datetime.date(startDate.year(), startDate.month(), startDate.day())
        Tstart = datetime.datetime.strptime(str(startDateDT), '%Y-%m-%d')
        dueDate = self.taskDueDE.date()
        dueDateDT = datetime.date(dueDate.year(), dueDate.month(), dueDate.day())
        Tdue = datetime.datetime.strptime(str(dueDateDT), '%Y-%m-%d')


        # Create a new task instance
        new_task = Task(project_fkey=self.projectPkey, name=Tname, desc=Tdesc, start_date=Tstart, due_date=Tdue, status=Tstatus,
                        assigner_fkey=assignerfkey, assignee_fkey=assignee_fkey, is_removed=0)
        # add project to db
        addTask = new_task.add_task(self.session)

        if addTask == 'successful':
            self.addTaskStatusLabel.setText(f'The task, {Tname}! has now been added in to project: {self.projectName}.')
            self.home_window_instance.populate_task_all_table(projectPKEY=self.projectPkey)

            # disable fields
            self.projectNameLE.setEnabled(False)
            self.taskNameLE.setEnabled(False)
            self.taskDescTE.setEnabled(False)
            self.taskStatusCB.setEnabled(False)
            self.taskStartDE.setEnabled(False)
            self.taskDueDE.setEnabled(False)
            self.addTaskButton.setEnabled(False)
            self.exitTaskButton.setText('Exit')

            # send email if there is an assignee
            if assignee_fkey != -1:
                emailSender = EmailSender()
                emailSender.set_recipient(assignee_fkey)
                emailSender.set_action_user(assignerfkey)
                emailSender.set_project(self.projectPkey)
                emailSender.set_task_name(Tname)

                # Create thread for email
                email_thread = threading.Thread(target=emailSender.on_task_assign)
                email_thread.start()

        else:
            self.addTaskStatusLabel.setText(addTask)

    def on_exit_without_save(self):
        if self.exitTaskButton.text() == 'Exit':
            self.close()
        else:
            confirmation = QMessageBox.question(self, "Confirm exit",
                                                "Are you sure you want to exit without adding the task?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                self.close()

    def on_field_changed(self):
        self.field_changed = True
        self.addTaskButton.setEnabled(True)
        self.exitTaskButton.setText('Exit (without saving')

class ViewProject(QDialog, Ui_ViewProjectDialog):
    def __init__(self, home_window_instance, project_pkey, activeUserInstance):
        super().__init__()
        self.setupUi(self)
        self.home_window_instance = home_window_instance
        self.project_pkey = project_pkey
        self.activeUserInstance = activeUserInstance
        self.projectInstance = None
        self.field_changed = False
        self.is_admin_or_owner = False

        # database connection
        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()

        #disable fields
        self.projectNameLE.setReadOnly(True)
        self.projectDescTE.setReadOnly(True)
        self.projectStatusCB.setEnabled(False)
        self.projectStartDE.setReadOnly(True)
        self.projectDueDE.setReadOnly(True)
        self.projectEndLE.setReadOnly(True)
        self.projectOwnerLE.setReadOnly(True)
        self.projectStatusCB.model().item(2).setEnabled(False)

        # run functions
        self.get_project_instance()
        self.check_project_status()
        self.check_if_user_is_admin_or_owner()

        self.populate_project()

        # thread team members table
        populate_team_members_thread = threading.Thread(target=self.populate_team_members_table)
        populate_team_members_thread.start()

        # on buttons click
        self.deleteProjectButton.clicked.connect(self.on_delete_project)
        self.saveChangesButton.clicked.connect(self.on_save_changes)
        self.exitWithoutSavingButton.clicked.connect(self.on_exit_without_save)
        self.closeProjectButton.clicked.connect(self.on_close_project)
        self.addMemberButton.clicked.connect(self.on_add_member_button)

        # check if fields have changed
        self.projectNameLE.textChanged.connect(self.on_field_changed)
        self.projectDescTE.textChanged.connect(self.on_field_changed)
        self.projectStatusCB.currentTextChanged.connect(self.on_field_changed)
        self.projectStartDE.dateChanged.connect(self.on_field_changed)
        self.projectDueDE.dateChanged.connect(self.on_field_changed)

        # disable buttons
        self.saveChangesButton.setEnabled(False)


    def get_project_instance(self):
        p = Project()
        self.projectInstance = p.get_project(self.session, self.project_pkey)

    def no_permission_to_perform_action(self):
        QMessageBox.critical(self, "Permission denied", "You do not have permissions to perform this action",
                             QMessageBox.StandardButton.Close)

    def check_if_user_is_admin_or_owner(self):

        # check if active user is owner of project
        if self.projectInstance.owner.username == self.activeUserInstance.username:
            self.is_admin_or_owner = True
            self.enable_view_project_fields()

        # check if user is admin
        u = User()
        activeUser = u.get_user(self.session, self.activeUserInstance.username)
        for user in activeUser:
            for userRole in user.user_roles:
                if userRole.role_type == 'Admin':
                    self.is_admin_or_owner = True
                    self.enable_view_project_fields()
                    break

    def check_project_status(self):
        # if the project has ended then disable fields
        if self.projectInstance.status == 'Completed':
            self.closeProjectButton.setEnabled(False)
            self.disable_view_project_fields()
            self.projectStatusCB.setEnabled(False)

    def populate_project(self):
        self.projectNameLE.setText(self.projectInstance.name)
        self.projectDescTE.setText(self.projectInstance.desc)
        self.projectStatusCB.setCurrentText(self.projectInstance.status)
        self.projectStartDE.setDate(self.projectInstance.start_date)
        self.projectDueDE.setDate(self.projectInstance.due_date)
        if self.projectInstance.end_date:
            self.projectEndLE.setText(self.projectInstance.end_date.strftime("%d/%m/%Y"))

        self.projectOwnerLE.setText(self.projectInstance.owner.full_name)

    def populate_team_members_table(self):
        # project team instance
        pt = ProjectTeam()
        teamMembers = pt.get_team_of_project(self.session, self.projectInstance.project_pkey)

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
        if self.is_admin_or_owner is False:
            self.no_permission_to_perform_action()
        else:
            confirmation = QMessageBox.question(self, "Confirm Deletion",
                                                "Are you sure you want to delete this project?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                #delete project
                projectDelete = self.projectInstance.delete_project(self.session, self.projectInstance.project_pkey)
                if projectDelete == 'Project deleted successfully':
                    self.projectChangesLabel.setText(f'The project, {self.projectInstance.name}! has now been removed.')

                    # refresh projects table to include the new project on dash tab home window
                    if self.home_window_instance.stackedWidget.currentIndex() == 0:
                        self.home_window_instance.populate_projects_ongoing_table()

                    if self.home_window_instance.stackedWidget.currentIndex() == 1:
                        self.home_window_instance.populate_projects_all_table()

                    #disable fields after deletion
                    self.disable_view_project_fields()

                    # thread send email on project closure
                    emailSender = EmailSender()
                    emailSender.set_action_user(self.activeUserInstance.user_pkey)
                    emailSender.set_project(self.project_pkey)
                    # Create thread for email
                    email_thread = threading.Thread(target=emailSender.on_project_close)
                    email_thread.start()

                else:
                    return projectDelete

    def on_save_changes(self):
        if self.is_admin_or_owner is False:
            self.no_permission_to_perform_action()
        else:
            currentName = self.projectNameLE.text()
            currentDesc = self.projectDescTE.toPlainText()
            currentStatus = self.projectStatusCB.currentText()

            currentStartDate = self.projectStartDE.date()
            startDateDT = datetime.date(currentStartDate.year(), currentStartDate.month(), currentStartDate.day())
            Pstart = datetime.datetime.strptime(str(startDateDT), '%Y-%m-%d')

            currentDueDate = self.projectDueDE.date()
            dueDateDT = datetime.date(currentDueDate.year(), currentDueDate.month(), currentDueDate.day())
            Pdue = datetime.datetime.strptime(str(dueDateDT), '%Y-%m-%d')

            updateProject = self.projectInstance.set_project(self.session, self.projectInstance.project_pkey,
                                                             currentName, currentDesc, currentStatus, Pstart, Pdue)

            if updateProject:
                print('updated')
                self.projectChangesLabel.setText(f'The project, {currentName}! has now been updated.')
                self.home_window_instance.populate_projects_all_table()
                self.exitWithoutSavingButton.setText('Exit')
                self.saveChangesButton.setEnabled(False)
            else:
                self.projectChangesLabel.setText(updateProject)

    def on_exit_without_save(self):
        if self.exitWithoutSavingButton.text() == 'Exit':
            self.close()
        else:
            confirmation = QMessageBox.question(self, "Confirm exit",
                                                "Are you sure you want to exit without saving the changes?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                self.close()

    def on_close_project(self):
        if self.is_admin_or_owner is False:
            self.no_permission_to_perform_action()
        else:
            confirmation = QMessageBox.question(self, "Confirm Project Closure",
                                                "Are you sure you want to close this project?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                closeProject = self.projectInstance.close_project(self.session, self.projectInstance.project_pkey)
                if closeProject == 'Project Closed':
                    self.projectChangesLabel.setText(f'The project, {self.projectInstance.name}! has now been closed.')
                    self.home_window_instance.populate_projects_all_table()
                    # disable fields after deletion
                    self.disable_view_project_fields()
                else:
                    return closeProject

    def disable_view_project_fields(self):
        self.projectNameLE.setEnabled(False)
        self.projectDescTE.setEnabled(False)
        self.projectStatusCB.setEnabled(False)
        self.projectStartDE.setEnabled(False)
        self.projectDueDE.setEnabled(False)
        self.projectEndLE.setEnabled(False)
        self.projectOwnerLE.setEnabled(False)
        self.saveChangesButton.setEnabled(False)
        self.closeProjectButton.setEnabled(False)
        self.deleteProjectButton.setEnabled(False)
        self.TeamMembersTable.setEnabled(False)
        self.addMemberButton.setEnabled(False)
        self.removeMemberButton.setEnabled(False)

    def enable_view_project_fields(self):
        self.projectNameLE.setReadOnly(False)
        self.projectDescTE.setReadOnly(False)
        self.projectStatusCB.setEnabled(True)
        self.projectStartDE.setReadOnly(False)
        self.projectDueDE.setReadOnly(False)
        self.projectEndLE.setReadOnly(False)
        self.projectOwnerLE.setReadOnly(False)

    def on_field_changed(self):
        self.field_changed = True
        self.saveChangesButton.setEnabled(True)
        self.exitWithoutSavingButton.setText('Exit (without saving')

    def on_add_member_button(self):
        if self.is_admin_or_owner is False:
            self.no_permission_to_perform_action()
        else:
            self.add_member_window = AddTeamMemberDialog(self, projectInstance=self.projectInstance,
                                                         activeUserInstance=self.activeUserInstance)
            self.add_member_window.show()

class AddTeamMemberDialog(QDialog, Ui_ViewProjectAddTeamMemberDialog):
    def __init__(self, view_project_instance, projectInstance, activeUserInstance):
        super().__init__()
        self.setupUi(self)
        self.view_project_instance = view_project_instance
        self.activeUserInstance = activeUserInstance
        self.projectInstance = projectInstance
        self.field_changed = False

        # database connection
        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()

        #run func
        self.populate_project_name()

        # thread username combo box
        populate_user_name_thread = threading.Thread(target=self.populate_user_name)
        populate_user_name_thread.start()

        #on button
        self.addUserButton.clicked.connect(self.on_add_user_button)
        self.exitButton.clicked.connect(self.on_exit_button)

    def populate_project_name(self):
        self.projectNameLE.setText(self.projectInstance.name)

    def populate_user_name(self):
        u = User()
        users = u.get_users(self.session)
        for user in users:
            item_text = f'{user.full_name} ({user.username})'
            item_data = user.user_pkey
            self.userCB.addItem(item_text, item_data)

    def on_add_user_button(self):
        # input from window
        index = self.userCB.currentIndex()
        user_pkey = int(self.userCB.itemData(index))

        #create project team instance
        projectUser = ProjectTeam(user_fkey=user_pkey, project_fkey=self.projectInstance.project_pkey, team_fkey=-1)
        addToPT = projectUser.add_team_member_to_project(self.session)

        if addToPT == 'successful':
            self.addUserConfirmLE.setText(f'{self.userCB.itemText(index)}! has now been added to {self.projectInstance.name}.')
            self.view_project_instance.populate_team_members_table()
        else:
            self.addUserConfirmLE.setText(addToPT)

    def on_exit_button(self):
        self.close()

class ViewTask(QDialog, Ui_ViewTaskDialog):
    def __init__(self, home_window_instance, project_pkey, task_pkey, activeUserInstance):
        super().__init__()
        self.setupUi(self)
        self.home_window_instance = home_window_instance

        self.project_pkey = project_pkey
        self.task_pkey = task_pkey
        self.activeUserInstance = activeUserInstance
        self.projectInstance = None
        self.taskInstance = None

        self.field_changed = False
        self.edit_permissions = False
        self.admin_permissions = False
        self.project_owner_fkey = False
        self.assignee_fkey = False
        self.assignee_reassigned = False

        # database connection
        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()

        # disable fields
        self.taskNameLE.setReadOnly(True)
        self.taskDescTE.setReadOnly(True)
        self.taskStartDE.setReadOnly(True)
        self.taskDueDE.setReadOnly(True)
        self.taskAssigneeCB.setEnabled(False)
        # disable items in task status drop down
        self.taskStatusCB.model().item(2).setEnabled(False)
        self.taskStatusCB.model().item(3).setEnabled(False)

        # run functions
        self.get_project_instance()
        self.get_task_instance()
        self.check_admin_permissions()
        self.check_edit_permissions()
        self.check_project_status()
        self.populate_task_assignee()
        self.populate_task()
        self.change_review_button_state()

        # on buttons click
        self.deleteTaskButton.clicked.connect(self.on_delete_task)
        self.saveChangesButton.clicked.connect(self.on_save_changes)
        self.exitWithoutSavingButton.clicked.connect(self.on_exit_without_save)
        self.closeTaskButton.clicked.connect(self.on_close_task)
        self.sendReviewtButton.clicked.connect(self.on_send_for_review)

        # check if fields have changed
        self.taskNameLE.textChanged.connect(self.on_field_changed)
        self.taskDescTE.textChanged.connect(self.on_field_changed)
        self.taskStatusCB.currentTextChanged.connect(self.on_field_changed)
        self.taskStartDE.dateChanged.connect(self.on_field_changed)
        self.taskDueDE.dateChanged.connect(self.on_field_changed)
        self.taskAssigneeCB.currentIndexChanged.connect(self.on_field_changed)
        self.taskProgressHS.valueChanged.connect(self.on_field_changed)
        self.taskProgressHS.valueChanged.connect(self.task_progress_slider_value_changed)

        # disable buttons
        self.saveChangesButton.setEnabled(False)


    def get_project_instance(self):
        p = Project()
        self.projectInstance = p.get_project(self.session, self.project_pkey)

    def check_project_status(self):
        if self.taskInstance.status == 'Completed':
            self.disable_view_task_fields()
            self.taskStatusCB.setEnabled(False)
            self.taskProgressHS.setEnabled(False)
    def get_task_instance(self):
        t = Task()
        self.taskInstance = t.get_task(self.session, self.task_pkey)

    def populate_task(self):
        self.projectNameLE.setText(self.taskInstance.project.name)
        self.taskNameLE.setText(self.taskInstance.name)
        self.taskDescTE.setText(self.taskInstance.desc)
        self.taskStatusCB.setCurrentText(self.taskInstance.status)
        self.taskStartDE.setDate(self.taskInstance.start_date)
        self.taskDueDE.setDate(self.taskInstance.due_date)
        self.taskProgressHS.setValue(self.taskInstance.task_progress)
        self.tpMinL.setText(str(self.taskInstance.task_progress))
        if self.taskInstance.end_date:
            self.taskEndLE.setText(self.taskInstance.end_date.strftime("%d/%m/%Y"))
            self.taskStatusCB.setCurrentText('Completed')

        self.taskAssignerLE.setText(f'{self.taskInstance.assigner.full_name} ({self.taskInstance.assigner.username})')
        self.taskAssigneeCB.setCurrentText(f'{self.taskInstance.assignee.full_name} ({self.taskInstance.assignee.username})')
        self.assignee_fkey = self.taskInstance.assignee_fkey
        self.project_owner_fkey = self.taskInstance.project.owner_fkey

    def populate_task_assignee(self):
        pt = ProjectTeam()
        project = pt.get_team_of_project(self.session, self.project_pkey)

        for user in project:
            item_text = f'{user.user.full_name} ({user.user.username})'
            item_data = user.user.user_pkey
            self.taskAssigneeCB.addItem(item_text, item_data)

    #permissions
    def no_permission_to_perform_action(self):
        QMessageBox.critical(self, "Permission denied", "You do not have permissions to perform this action",
                             QMessageBox.StandardButton.Close)

    def check_admin_permissions(self):

        #if active user is project owner
        if self.projectInstance.owner.username == self.activeUserInstance.username:
            self.admin_permissions = True
            self.disable_non_admin_features()

        # if active user is admin
        u = User()
        activeUser = u.get_user(self.session, self.activeUserInstance.username)
        for user in activeUser:
            for userRole in user.user_roles:
                if userRole.role_type == 'Admin':
                    self.admin_permissions = True
                    self.disable_non_admin_features()
                    break

    def check_edit_permissions(self):

        #check if task is assigned to active  user
        if self.taskInstance.assignee.username == self.activeUserInstance.username:
            self.edit_permissions = True

        # is project owner
        if self.projectInstance.owner.username == self.activeUserInstance.username:
            self.edit_permissions = True

        # is admin
        u = User()
        activeUser = u.get_user(self.session, self.activeUserInstance.username)
        for user in activeUser:
            for userRole in user.user_roles:
                if userRole.role_type == 'Admin':
                    self.edit_permissions = True
                    break

    # widget states
    def change_review_button_state(self):
        if self.taskInstance.status == 'Completed':
            self.sendReviewtButton.setEnabled(False)
        if self.taskInstance.status == 'Pending Review':
            self.sendReviewtButton.setText('Reject and send back')

    def task_progress_slider_value_changed(self):
        value = self.taskProgressHS.value()
        self.tpMinL.setText(str(value))

    def disable_view_task_fields(self):
        self.projectNameLE.setEnabled(False)
        self.taskNameLE.setEnabled(False)
        self.taskDescTE.setEnabled(False)
        self.taskStatusCB.setEnabled(False)
        self.taskStartDE.setEnabled(False)
        self.taskDueDE.setEnabled(False)
        self.taskEndLE.setEnabled(False)
        self.taskAssigneeCB.setEnabled(False)
        self.taskAssignerLE.setEnabled(False)
        self.saveChangesButton.setEnabled(False)
        self.closeTaskButton.setEnabled(False)
        self.deleteTaskButton.setEnabled(False)

    def disable_non_admin_features(self):
        self.taskNameLE.setReadOnly(False)
        self.taskDescTE.setReadOnly(False)
        self.taskStartDE.setReadOnly(False)
        self.taskDueDE.setReadOnly(False)
        self.taskAssigneeCB.setEnabled(True)


    #on button functions
    def on_delete_task(self):
        if self.admin_permissions is False:
            self.no_permission_to_perform_action()
        else:
            confirmation = QMessageBox.question(self, "Confirm Deletion",
                                                "Are you sure you want to delete this task?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                taskDelete = self.taskInstance.delete_task(self.session, self.task_pkey)
                if taskDelete == 'Task deleted successfully':
                    self.taskChangesLabel.setText(f'The Task, {self.taskInstance.name}! has now been removed.')
                    self.home_window_instance.populate_task_all_table(projectPKEY=self.project_pkey)

                    #disable fields after deletion
                    self.disable_view_task_fields()

                else:
                    return taskDelete

    def on_save_changes(self):
        if self.edit_permissions is False:
            self.no_permission_to_perform_action()
        else:
            currentProjectName = self.projectNameLE.text()
            currentTaskName = self.taskNameLE.text()
            currentDesc = self.taskDescTE.toPlainText()
            currentStatus = self.taskStatusCB.currentText()

            currentStartDate = self.taskStartDE.date()
            startDateDT = datetime.date(currentStartDate.year(), currentStartDate.month(), currentStartDate.day())
            Pstart = datetime.datetime.strptime(str(startDateDT), '%Y-%m-%d')

            currentDueDate = self.taskDueDE.date()
            dueDateDT = datetime.date(currentDueDate.year(), currentDueDate.month(), currentDueDate.day())
            Pdue = datetime.datetime.strptime(str(dueDateDT), '%Y-%m-%d')

            # get assignee fkey
            AssignToCBIndex = self.taskAssigneeCB.currentIndex()
            assignee_fkey = int(self.taskAssigneeCB.itemData(AssignToCBIndex))
            # check if assignee has changed
            if assignee_fkey != self.taskInstance.assignee_fkey:
                self.assignee_reassigned = True

            #task progress
            taskProgress = int(self.taskProgressHS.value())


            # pass variable to update
            updateTask = self.taskInstance.set_task(session=self.session, task_pkey=self.task_pkey,
                                                    setName=currentTaskName, setDesc=currentDesc,
                                                    taskProgress=taskProgress, setStatus=currentStatus,
                                                    setStartDate=Pstart, setDueDate=Pdue, assigneeFkey=assignee_fkey)

            if updateTask:
                self.taskChangesLabel.setText(f'The task, {currentTaskName}! has now been updated.')
                self.home_window_instance.populate_task_all_table(projectPKEY=self.project_pkey)
                self.exitWithoutSavingButton.setText('Exit')
                self.saveChangesButton.setEnabled(False)

                # send email if assignee as changed
                if self.assignee_reassigned:
                    emailSender = EmailSender()
                    emailSender.set_recipient(assignee_fkey)
                    emailSender.set_action_user(self.activeUserInstance.user_pkey)
                    emailSender.set_project(self.project_pkey)
                    emailSender.set_task_name(currentTaskName)

                    # Create thread for email
                    email_thread = threading.Thread(target=emailSender.on_task_assign)
                    email_thread.start()


            else:
                self.taskChangesLabel.setText(updateTask)

    def on_exit_without_save(self):
        if self.exitWithoutSavingButton.text() == 'Exit':
            self.close()
        else:
            confirmation = QMessageBox.question(self, "Confirm exit",
                                                "Are you sure you want to exit without saving the changes?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                self.close()

    def on_close_task(self):
        if self.admin_permissions is False:
            self.no_permission_to_perform_action()
        else:
            confirmation = QMessageBox.question(self, "Confirm Task Closure",
                                                "Are you sure you want to end and mark this task as complete?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                closeTask = self.taskInstance.close_task(self.session, self.task_pkey)
                if closeTask == 'Task Closed':
                    self.taskChangesLabel.setText(f'The task, {self.taskInstance.name}! has now been closed.')
                    self.taskProgressHS.setValue(100)
                    self.tpMinL.setText(str(100))
                    self.taskStatusCB.setCurrentText('Completed')
                    self.taskEndLE.setText(dt.utcnow().strftime('%d/%m/%Y %H:%M:%S'))
                    self.exitWithoutSavingButton.setText('Exit')
                    self.home_window_instance.populate_task_all_table(projectPKEY=self.project_pkey)

                    # disable fields after deletion
                    self.disable_view_task_fields()

                    # send email to assignee on closure
                    emailSender = EmailSender()
                    emailSender.set_recipient(self.taskInstance.assignee_fkey)
                    emailSender.set_action_user(self.activeUserInstance.user_pkey)
                    emailSender.set_project(self.project_pkey)
                    emailSender.set_task_name(self.taskInstance.name)
                    # Create thread for email
                    email_thread = threading.Thread(target=emailSender.on_task_close)
                    email_thread.start()

                else:
                    self.taskChangesLabel.setText(f'{closeTask}')
                    return closeTask

    def on_field_changed(self):
        self.field_changed = True
        self.saveChangesButton.setEnabled(True)
        self.exitWithoutSavingButton.setText('Exit (without saving')

    def on_send_for_review(self):
        if self.admin_permissions is True and self.taskInstance.status == 'Pending Review':
            confirmation = QMessageBox.question(self, "Confirm Fail Review",
                                                "Are you sure you want to fail the review?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                currentTaskName = self.taskNameLE.text()
                updateTask = self.taskInstance.set_task(self.session, self.task_pkey, setStatus='In-Progress')
                if updateTask:
                    self.taskStatusCB.setCurrentText('In-Progress')
                    self.taskChangesLabel.setText(f'The task, {currentTaskName}! has now been sent back.')
                    self.home_window_instance.populate_task_all_table(projectPKEY=self.project_pkey)
                    self.sendReviewtButton.setEnabled(False)
                    self.saveChangesButton.setEnabled(False)
                    self.exitWithoutSavingButton.setText('Exit')
                else:
                    self.taskChangesLabel.setText(updateTask)

        elif self.edit_permissions is True and self.taskInstance.status != 'Pending Review':
            confirmation = QMessageBox.question(self, "Confirm Task Review",
                                                "Are you sure you want to send this task for review?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                currentTaskName = self.taskNameLE.text()
                updateTask = self.taskInstance.set_task(self.session, self.task_pkey, setStatus='Pending Review')

                if updateTask:
                    self.taskStatusCB.setCurrentText('Pending Review')
                    self.taskChangesLabel.setText(f'The task, {currentTaskName}! has now been sent for review.')
                    self.home_window_instance.populate_task_all_table(projectPKEY=self.project_pkey)
                    self.sendReviewtButton.setEnabled(False)
                    self.saveChangesButton.setEnabled(False)
                    self.exitWithoutSavingButton.setText('Exit')
                else:
                    self.taskChangesLabel.setText(updateTask)

        else:
            self.no_permission_to_perform_action()






def main():
    # db connection
    dbCon = DatabaseConnection()
    session = dbCon.get_session()
    # Class user to query
    user = User()
    # authenticate user
    userAuthentication, userInstance = user.authenticate_user(session, 'tm1', '12345')

    app = QApplication(sys.argv)
    window = HomeWindow(activeUserInstance=userInstance)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()