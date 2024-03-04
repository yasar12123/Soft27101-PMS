from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassEmail import EmailSender
from src.ClassUser import User
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QDialog, QMessageBox, QSizePolicy, QLabel
from PyQt6.QtCore import QDate, Qt
from generated.AddProjectDialog import Ui_AddProjectDialog
from generated.HomeWindow import Ui_HomeWindow
from generated.ViewProjectDialog import Ui_ViewProjectDialog
from generated.ViewTaskDialog import Ui_ViewTaskDialog
from generated.AddTaskDialog import Ui_AddTaskDialog
from generated.ViewProjectAddTeamMemberDialog import Ui_ViewProjectAddTeamMemberDialog

import sys
import datetime
from datetime import datetime as dt
import threading


class HomeWindow(QMainWindow, Ui_HomeWindow):
    """
    Home window class
    defines the home window and its functions
    methods:
    - __init__(self, activeUserInstance)
    - on_load_defaults(self)
    - check_if_user_is_admin(self)
    - on_profile_load_defaults(self)
    - on_admin_profile_load_defaults(self)
    - populate_profile_details(self)
    - populate_admin_select_user_cb(self)
    - on_userSelectCB_changed(self)
    - populate_admin_select_user_cb_thread(self)
    - on_change_password_radio_button(self)
    - on_not_change_password_radio_button(self)
    - on_change_personal_details_button(self)
    - on_account_deletion_understand_button(self)
    - on_account_deletion_cancel_button(self)
    - on_update_details_button(self)
    - on_account_deletion_button(self)
    - on_grant_admin_access_to_user_button(self)
    - populate_user_timeline(self, userPkey=None)
    - on_profile_button(self)
    - on_dash_button(self)
    - display_project_stats(self)
    - display_task_stats(self)
    - populate_projects_ongoing_table(self)
    - populate_tasks_ongoing_table(self, projectPkey=None)
    - on_project_ongoing_table_item_clicked(self, item)
    - on_task_ongoing_table_item_clicked(self, item)
    - on_go_to_project_button(self)
    - on_go_to_task_button(self)
    - on_got_to_project_tasks_button(self)
    - go_to_all_project_task_table(self)
    - on_projects_button(self)
    - populate_projects_all_table(self)
    - populate_projects_all_table_thread(self)
    - populate_project_comments(self, projectPkey)
    - on_add_project_comment_button(self)
    - on_project_all_table_item_clicked(self, item)
    - on_add_project_button(self)
    - on_tasks_button(self)
    - populate_task_project_table(self)
    - populate_task_project_table_thread(self)
    - populate_task_all_table(self, project_pkey)
    - populate_task_all_table_thread(self, project_pkey)
    - on_task_project_all_table_item_clicked(self, item)
    """
    def __init__(self, activeUserInstance):
        super().__init__()
        self.setupUi(self)
        self.activeUserInstance = activeUserInstance
        self.activeUserIsAdmin = False
        self.projectNameItemSelected = None
        self.projectItemSelected = None
        self.taskItemSelected = None
        self.adminSelectedUserPkey = None

        # Database connection
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

        # load on start
        self.on_load_defaults()

        # menu buttons
        self.dashButton.clicked.connect(self.on_dash_button)
        self.projectsButton.clicked.connect(self.on_projects_button)
        self.tasksButton.clicked.connect(self.on_tasks_button)
        self.profileButton.clicked.connect(self.on_profile_button)
        self.logOutButton.clicked.connect(self.on_logOut_button)

        # dash functions
        self.dashViewProjectButton.clicked.connect(self.on_go_to_project_button)
        self.dashViewTaskButton.clicked.connect(self.on_go_to_task_button)
        self.ProjectsOngoingTable.itemClicked.connect(self.on_project_ongoing_table_item_clicked)
        self.TasksOngoingTable.itemClicked.connect(self.on_task_ongoing_table_item_clicked)

        # project function
        self.AddProjectButton.clicked.connect(self.on_add_project_button)
        self.ViewProjectButton.clicked.connect(self.on_view_project_button)
        self.projectViewTasksButton.clicked.connect(self.on_got_to_project_tasks_button)
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
        self.APgrantAdminPermissionButton.clicked.connect(self.on_grant_admin_access_to_user_button)

        # on field changed
        self.userSelectCB.currentIndexChanged.connect(self.on_userSelectCB_changed)

    def on_load_defaults(self):
        self.check_if_user_is_admin()
        self.on_dash_button()
        self.populate_projects_all_table_thread()

    """Profile Page Methods"""
    # profile page functions
    def on_profile_button(self):
        self.stackedWidget.setCurrentIndex(3)
        self.check_if_user_is_admin()
        self.populate_profile_details()

        # thread and populate user timeline
        user_timeline_thread = threading.Thread(target=self.populate_user_timeline)
        user_timeline_thread.start()

    # permissions and load defaults
    def check_if_user_is_admin(self):
        check = self.activeUserInstance.is_user_admin(self.session, self.activeUserInstance.user_pkey)
        if check:
            self.activeUserIsAdmin = True
            self.dashDescLabel.setText('This dashboard shows all ongoing projects and tasks associated with them')
            self.on_admin_profile_load_defaults()
        else:
            self.activeUserIsAdmin = False
            self.dashDescLabel.setText('This Dashboard Displays: '
                                       '\n1. All projects which you are a owner of along with the tasks that are associated with them.'
                                       '\n2. All project which you are a member of along with tasks that have been assigned to you.')
            self.on_profile_load_defaults()

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
        self.profileLabel.setText(f' Logged in as: \n {self.activeUserInstance.full_name}')
        # hide admin features
        self.adminSUGB.hide()
        self.APgrantAdminPermissionButton.hide()

    def on_admin_profile_load_defaults(self):
        self.on_profile_load_defaults()
        self.activeUserIsAdmin = True
        self.profileLabel.setText(f'Logged in as: \n {self.activeUserInstance.full_name}\n (Admin)')
        self.adminSUGB.show()
        self.APgrantAdminPermissionButton.show()
        self.populate_admin_select_user_cb_thread()

    def populate_profile_details(self):
        # refresh active user instance after changing details
        self.activeUserInstance = User.get_user_instance(self.session, self.activeUserInstance.user_pkey)
        self.pdNameLE.setText(self.activeUserInstance.full_name)
        self.pdEmailLE.setText(self.activeUserInstance.email_address)
        self.pdUsernameLE.setText(self.activeUserInstance.username)
        self.pdPasswordLE.setText('**********')

    def populate_admin_select_user_cb(self):
        # populate select user combo box
        users = User().get_users(self.session)
        self.userSelectCB.clear()
        for user in users:
            item_text = f'{user.full_name} ({user.username})'
            item_data = user.user_pkey
            self.userSelectCB.addItem(item_text, item_data)

        # set current user
        self.userSelectCB.setCurrentText(
            f'{self.activeUserInstance.full_name} ({self.activeUserInstance.username})')

    def on_userSelectCB_changed(self):
        # get user
        user_selected_index = self.userSelectCB.currentIndex()
        user_selected_fkey = int(self.userSelectCB.itemData(user_selected_index))
        user = User().get_user_instance(self.session, user_pkey=user_selected_fkey)
        self.adminSelectedUserPkey = user_selected_fkey
        # set fields from the user that is selected
        self.pdNameLE.setText(user.full_name)
        self.pdEmailLE.setText(user.email_address)
        self.pdUsernameLE.setText(user.username)
        self.pdPasswordLE.setText('**********')

        # # thread and populate user timeline
        user_timeline_thread = threading.Thread(target=self.populate_user_timeline(userPkey=user_selected_fkey))
        user_timeline_thread.start()

    def populate_admin_select_user_cb_thread(self):
        # thread populate combo box
        populate_admin_su_thread = threading.Thread(target=self.populate_admin_select_user_cb)
        populate_admin_su_thread.start()
        #populate_admin_su_thread.join()

    # profile page buttons
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
            self.updateDetailsButton.setEnabled(True)
            self.updateDetailsButton.show()
            self.changePasswordRB.show()
            self.changeDetailsButton.setText('Discard Changes')
        else:
            if self.activeUserIsAdmin:
                self.on_admin_profile_load_defaults()
            else:
                self.on_profile_load_defaults()
            self.populate_profile_details()

    def on_account_deletion_understand_button(self):
        self.accountDeleteButton.show()

    def on_account_deletion_cancel_button(self):
        self.accountDeleteButton.hide()
        self.accountDoNotDeleteRB.setChecked(True)

    def on_update_details_button(self):
        # input from window
        name = self.pdNameLE.text()
        emailAdd = self.pdEmailLE.text()
        password = self.pdPasswordLE.text()

        # if user is admin and they have selected a user from user combo box
        # then get the selected user pkey
        if self.activeUserIsAdmin and self.adminSelectedUserPkey:
            user_pkey = self.adminSelectedUserPkey

        # else use users own pkey
        else:
            user_pkey = self.activeUserInstance.user_pkey

        # if password not changed then update without password
        if self.request_password_change is False:
            set_user = self.activeUserInstance.set_user(self.session, user_to_set_pkey=user_pkey,
                                                        setFullname=name, setEmailAddress=emailAdd)

        # if password changed then update with password
        if self.request_password_change is True:
            set_user = self.activeUserInstance.set_user(self.session, user_to_set_pkey=user_pkey,
                                                        setFullname=name, setEmailAddress=emailAdd,
                                                        setPassword=password)
        # set label and reload profile
        self.updateStatusLabel.setText(set_user)
        self.on_profile_button()

    def on_account_deletion_button(self):

        # confirmation box
        confirmation = self.confirmation_box('Confirm deletion', 'Are you sure you want to delete the account?')
        if confirmation == QMessageBox.StandardButton.Yes:

            # if user is admin and they have selected a user from user combo box
            # then get the selected user pkey
            if self.activeUserIsAdmin is True and self.adminSelectedUserPkey:
                user_pkey = self.adminSelectedUserPkey

            # else use the users own pkey
            else:
                user_pkey = self.activeUserInstance.user_pkey

            # delete from user table
            delete_user = self.activeUserInstance.delete_user(self.session, user_pkey)
            self.deleteStatusLabel.setText(delete_user)

            # when user has been removed
            if delete_user == 'User has been deleted':

                #remove all roles
                remove_user_roles = UserRole().delete_user_role(self.session, user_pkey)
                self.deleteStatusLabel.setText(remove_user_roles)

                #un-assign all tasks
                remove_from_tasks = Task().unassign_tasks(self.session, user_pkey)
                self.deleteStatusLabel.setText(remove_from_tasks)

                # un-assign all projects
                remove_from_projects = Project().unassign_projects(self.session, user_pkey)
                self.deleteStatusLabel.setText(remove_from_projects)

                # remove from projects team
                delete_from_teams = ProjectTeam().delete_team_member_from_projects(self.session, user_pkey)
                self.deleteStatusLabel.setText(delete_from_teams)

                # label that the user has been deleted
                self.deleteStatusLabel.setText('user has now been deleted')
                self.on_profile_button()

                # finally close if user is not admin
                if self.activeUserIsAdmin is False:
                    self.close()

            # set label if error deleting user
            else:
                self.deleteStatusLabel.setText(delete_user)

    def on_grant_admin_access_to_user_button(self):
        # confirmation box
        confirmation = self.confirmation_box('Confirm Admin Access', 'Are you sure you want to grant '
                                                                     '\n Admin permissions to the account?')

        if confirmation == QMessageBox.StandardButton.Yes:

            # if user is admin and they have selected a user from user combo box
            # then get the selected user pkey
            if self.activeUserIsAdmin and self.adminSelectedUserPkey:
                user_pkey = self.adminSelectedUserPkey

            # else use users own pkey
            else:
                user_pkey = self.activeUserInstance.user_pkey

            if user_pkey:

                user_roles = self.activeUserInstance.get_roles(self.session)
                if user_roles:
                    for user_role in user_roles:
                        if user_role.role_type == 'Admin':
                            self.updateStatusLabel.setText('User already has Admin permissions')
                            return

            else:
                grantAccess = UserRole.add_user_role(self.session, user_pkey, 'Admin')
                self.updateStatusLabel.setText(grantAccess)
                self.on_profile_button()

    def populate_user_timeline(self, userPkey=None):
        # get project communication log
        comLog = CommunicationLog()
        if userPkey:
            userLog = comLog.get_user_communication_log(self.session, userPkey)
        else:
            userLog = comLog.get_user_communication_log(self.session, self.activeUserInstance.user_pkey)
        # Sort the projectLog list by timestamp
        userLog.sort(key=lambda log: log.timestamp, reverse=True)
        # clear comments list
        self.userTimeLineLW.clear()
        # load project comments
        for log in userLog:
            # add new line to space out comments
            timestamp = log.timestamp.strftime('%d/%m/%Y %H:%M:%S')
            self.userTimeLineLW.addItem('\n')
            if log.task_fkey == -1:
                log.task.name = 'N/A'
            self.userTimeLineLW.addItem(f'Datetime: {timestamp}, User: {log.user.full_name} '
                                        f'\nProject: {log.project.name}, Task:{log.task.name}'
                                        f'\n{log.comment} ')


    """ Dashboard page methods """
    def on_dash_button(self):

        # Switch to the dashboard page
        self.stackedWidget.setCurrentIndex(0)

        # disable buttons
        self.dashViewProjectButton.setEnabled(False)
        self.dashViewTaskButton.setEnabled(False)

        # run stats
        self.display_project_stats()
        self.display_task_stats()

        # run thread functions
        project_thread = threading.Thread(target=self.populate_projects_ongoing_table)
        project_thread.start()
        project_thread.join()
        task_thread = threading.Thread(target=self.populate_tasks_ongoing_table)
        task_thread.start()
        task_thread.join()



    def display_project_stats(self):
        # if user is admin then get all tasks
        if self.activeUserIsAdmin:
            projects = Project().get_projects(self.session)
        else:
            projects = Project().get_projects_user_member_of(self.session, user_pkey=self.activeUserInstance.user_pkey)

        # calc metrics
        total_projects = sum(1 for project in projects)
        completed_projects = sum(1 for project in projects if project.status == 'Completed')
        in_progress_projects = sum(1 for project in projects if project.status == 'In-Progress')
        not_started_projects = sum(1 for project in projects if project.status == 'Not Started')

        # set layout
        layout = QVBoxLayout(self.projectStatsFrame)

        # Add labels for counts
        project_label = QLabel(f'No of Projects: {total_projects}')
        layout.addWidget(project_label)
        project_completed_label = QLabel(f'No of Projects Completed: {completed_projects}')
        layout.addWidget(project_completed_label)
        completed_label = QLabel(f'No of Projects In-Progress: {in_progress_projects}')
        layout.addWidget(completed_label)
        in_progress_label = QLabel(f'No of Projects Not Started: {not_started_projects}')
        layout.addWidget(in_progress_label)

        # Set size policy to automatically adjust size
        self.projectStatsFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def display_task_stats(self):
        # if user is admin then get all tasks
        if self.activeUserIsAdmin:
            tasks = Task().get_tasks(self.session)
        else:
            tasks = Task().get_user_ongoing_project_tasks(self.session, self.activeUserInstance.user_pkey)

        # calc metrics
        total_tasks = sum(1 for task in tasks)
        completed_tasks = sum(1 for task in tasks if task.status == 'Completed')
        in_progress_tasks = sum(1 for task in tasks if task.status == 'In-Progress')
        not_started_tasks = sum(1 for task in tasks if task.status == 'Not Started')
        pending_review_tasks = sum(1 for task in tasks if task.status == 'Pending Review')
        review_failed_tasks = sum(1 for task in tasks if task.status == 'Review Failed')

        # set layout
        layout = QVBoxLayout(self.taskStatsFrame)
        layout.setAlignment(self.taskStatsFrame, Qt.AlignmentFlag.AlignRight)

        # Add labels for counts
        total_label = QLabel(f'{total_tasks} :No of Task')
        total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(total_label)
        completed_label = QLabel(f'{completed_tasks} :Tasks Completed')
        completed_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(completed_label)
        in_progress_label = QLabel(f'{in_progress_tasks} :Tasks In-Progress')
        in_progress_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(in_progress_label)
        not_started_label = QLabel(f'{not_started_tasks} :Tasks Not Started')
        not_started_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(not_started_label)
        pending_review_label = QLabel(f'{pending_review_tasks} :Tasks Pending Review')
        pending_review_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(pending_review_label)
        review_failed_label = QLabel(f'{review_failed_tasks} :Tasks Failed Review')
        review_failed_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(review_failed_label)

        # Set size policy to automatically adjust size
        self.taskStatsFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def populate_projects_ongoing_table(self):
        # clear table
        self.ProjectsOngoingTable.setRowCount(0)
        # if user is admin the get all ongoing projects
        if self.activeUserIsAdmin:
            projects = Project().get_projects(self.session, completed=False)

        # else display ongoing projects in which the user is a team member
        else:
            projects = Project().get_projects_user_member_of(self.session, self.activeUserInstance.user_pkey)

        # Populate the projects table
        if projects:
            for row, project in enumerate(projects):
                self.ProjectsOngoingTable.insertRow(row)
                self.ProjectsOngoingTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(project.project_pkey)))
                self.ProjectsOngoingTable.setItem(row, 1, QtWidgets.QTableWidgetItem(project.name))
                self.ProjectsOngoingTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(project.start_date.strftime('%d-%m-%Y'))))
                self.ProjectsOngoingTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(project.due_date.strftime('%d-%m-%Y'))))
                self.ProjectsOngoingTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(project.status)))
                self.ProjectsOngoingTable.setItem(row, 5, QtWidgets.QTableWidgetItem(str(project.owner.full_name)))

    def populate_tasks_ongoing_table(self, projectPkey=None):
        # clear table
        self.TasksOngoingTable.setRowCount(0)

        # if user is admin then get all tasks
        if self.activeUserIsAdmin:
            tasks = Task().get_tasks(self.session, project_completed=False)

        # if user is admin and project pkey has been specified
        elif self.activeUserIsAdmin and projectPkey:
            tasks = Task().get_tasks(self.session, project_pkey=projectPkey, project_completed=False)

        # if project pkey specified then all tasks for that project and user
        elif projectPkey:
            tasks = Task().get_user_ongoing_project_tasks(self.session, self.activeUserInstance.user_pkey, project_pkey=projectPkey)

        # else if user is not admin then all tasks assigned to that user
        else:
            tasks = Task().get_user_ongoing_project_tasks(self.session, self.activeUserInstance.user_pkey)

        # Populate the tasks table
        if tasks:
            for row, task in enumerate(tasks):
                self.TasksOngoingTable.insertRow(row)
                self.TasksOngoingTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(task.task_pkey)))
                self.TasksOngoingTable.setItem(row, 1, QtWidgets.QTableWidgetItem(task.name))
                self.TasksOngoingTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(task.start_date.strftime('%d-%m-%Y'))))
                self.TasksOngoingTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(task.due_date.strftime('%d-%m-%Y'))))
                self.TasksOngoingTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(task.status)))
                self.TasksOngoingTable.setItem(row, 5, QtWidgets.QTableWidgetItem(str(task.project_fkey)))

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

            # thread and populate tasks ongoing table with the specified project pkey
            task_thread = threading.Thread(target=self.populate_tasks_ongoing_table(projectPkey=int(projectPkey)))
            task_thread.start()


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

        # find and select the project in the project table
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

    def on_got_to_project_tasks_button(self):
        # Switch to the tasks page
        self.on_tasks_button()

        for row in range(self.taskProjectTable.rowCount()):
            # Get the value of the pkey in the table
            item = self.taskProjectTable.item(row, 0)
            if item is not None and item.text() == str(self.projectItemSelected):
                # Select the row if the value matches
                self.taskProjectTable.selectRow(row)
                self.taskProjectTable.itemClicked.emit(item)

    def go_to_all_project_task_table(self):
        # find and select row in the projects table
        for row in range(self.taskProjectTable.rowCount()):
            # Get the value of the pkey in the table
            item = self.taskProjectTable.item(row, 0)
            if item is not None and item.text() == str(self.projectItemSelected):
                # Select the row if the value matches
                self.taskProjectTable.selectRow(row)
                self.taskProjectTable.itemClicked.emit(item)

    """ Project page functions """

    def on_projects_button(self):
        # switch to project page
        self.stackedWidget.setCurrentIndex(1)
        # clear the comments
        self.commentListWidget.clear()
        # clear projects table
        self.ProjectsAllTable.setRowCount(0)
        # disable button
        self.ViewProjectButton.setEnabled(False)
        self.projectViewTasksButton.setEnabled(False)
        # load all projects using threading
        self.populate_projects_all_table_thread()

    def populate_projects_all_table(self):
        # clear projects table
        self.ProjectsAllTable.setRowCount(0)

        # project instance
        p = Project()
        projects = p.get_projects(self.session)

        # Populate the projects table
        if projects:
            # load data into table
            for row, project in enumerate(sorted(projects, key=lambda x: x.name.lower())):
                self.ProjectsAllTable.insertRow(row)
                self.ProjectsAllTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(project.project_pkey)))
                self.ProjectsAllTable.setItem(row, 1, QtWidgets.QTableWidgetItem(project.name))
                self.ProjectsAllTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(project.start_date.strftime('%d-%m-%Y'))))
                self.ProjectsAllTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(project.due_date.strftime('%d-%m-%Y'))))
                if project.end_date is not None:
                    self.ProjectsAllTable.setItem(row, 4, QtWidgets.QTableWidgetItem(project.end_date.strftime('%d-%m-%Y %H:%M:%S')))
                else:
                    self.ProjectsAllTable.setItem(row, 4, QtWidgets.QTableWidgetItem(''))
                self.ProjectsAllTable.setItem(row, 5, QtWidgets.QTableWidgetItem(str(project.status)))
                self.ProjectsAllTable.setItem(row, 6, QtWidgets.QTableWidgetItem(str(project.owner.full_name)))

    def populate_projects_all_table_thread(self):
        # Create threads for populating project all table
        populate_projects_all_thread = threading.Thread(target=self.populate_projects_all_table)
        populate_projects_all_thread.start()
        populate_projects_all_thread.join()

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
            self.projectViewTasksButton.setEnabled(True)

            # populate comments via threading
            project_comments_thread = threading.Thread(target=self.populate_project_comments(self.projectItemSelected))
            project_comments_thread.start()
            project_comments_thread.join()

    def on_add_project_button(self):
        # open add project class
        self.add_project_window = AddProject(self, activeUserInstance=self.activeUserInstance)
        self.add_project_window.show()



    """ Task page functions """

    def on_tasks_button(self):
        # switch Tasks page
        self.stackedWidget.setCurrentIndex(2)

        # disable buttons
        self.viewProjectButtonB.setEnabled(False)
        self.ViewTaskButton.setEnabled(False)
        self.AddTaskButton.setEnabled(False)
        self.addTaskCommentButton.setEnabled(False)

        # clear comments and project, task table
        self.taskCommentListWidget.clear()
        self.TaskAllTable.setRowCount(0)
        self.taskProjectTable.setRowCount(0)

        # run thread functions
        self.populate_task_project_table_thread()
        self.populate_task_all_table_thread(project_pkey=-1)

    def populate_task_project_table(self):
        # clear table
        self.taskProjectTable.setRowCount(0)
        # project instance
        p = Project()
        projects = p.get_projects(self.session)

        # Populate the projects table
        if projects:
            for row, project in enumerate(sorted(projects, key=lambda x: x.name.lower())):
                self.taskProjectTable.insertRow(row)
                self.taskProjectTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(project.project_pkey)))
                self.taskProjectTable.setItem(row, 1, QtWidgets.QTableWidgetItem(project.name))

    def populate_task_project_table_thread(self):
        # Create thread for populating task project table
        populate_task_project_thread = threading.Thread(target=self.populate_task_project_table)
        populate_task_project_thread.start()
        populate_task_project_thread.join()

    def populate_task_all_table(self, project_pkey):
        # clear table
        self.TaskAllTable.setRowCount(0)
        # get all tasks for project
        t = Task()
        tasks = t.get_tasks(self.session, project_pkey)

        # Populate the tasks table
        if tasks:
            for row, task in enumerate(sorted(tasks, key=lambda x: x.name.lower())):
                self.TaskAllTable.insertRow(row)
                self.TaskAllTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(task.project_fkey)))
                self.TaskAllTable.setItem(row, 1, QtWidgets.QTableWidgetItem(task.project.name))
                self.TaskAllTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(task.task_pkey)))
                self.TaskAllTable.setItem(row, 3, QtWidgets.QTableWidgetItem(task.name))
                self.TaskAllTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(task.start_date.strftime('%d-%m-%Y'))))
                self.TaskAllTable.setItem(row, 5, QtWidgets.QTableWidgetItem(task.status))
                self.TaskAllTable.setItem(row, 6, QtWidgets.QTableWidgetItem(str(task.due_date.strftime('%d-%m-%Y'))))
                if task.end_date is not None:
                    self.TaskAllTable.setItem(row, 7, QtWidgets.QTableWidgetItem(task.end_date.strftime('%d-%m-%Y %H:%M:%S')))
                else:
                    self.TaskAllTable.setItem(row, 7, QtWidgets.QTableWidgetItem(''))
                self.TaskAllTable.setItem(row, 8, QtWidgets.QTableWidgetItem(task.assignee.full_name))
                self.TaskAllTable.setItem(row, 9, QtWidgets.QTableWidgetItem(task.assigner.full_name))

    def populate_task_all_table_thread(self, project_pkey):
        # Create thread for populating task project table
        populate_task_thread = threading.Thread(target=self.populate_task_all_table(project_pkey=project_pkey))
        populate_task_thread.start()
        populate_task_thread.join()

    def on_task_project_all_table_item_clicked(self, item):
        if item:
            # clear task comments table
            self.taskCommentListWidget.clear()
            self.TaskAllTable.setRowCount(0)

            # set project pkey
            row = item.row()
            self.projectItemSelected = int(self.taskProjectTable.item(row, 0).text())
            self.projectNameItemSelected = self.taskProjectTable.item(row, 1).text()

            # populate tasks table via threading
            self.populate_task_all_table_thread(project_pkey=self.projectItemSelected)

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

    """ Buttons Connected to multiple pages"""
    def on_view_project_button(self):
        projectPk = self.projectItemSelected
        self.view_project_window = ViewProject(self, project_pkey=projectPk, activeUserInstance=self.activeUserInstance)
        self.view_project_window.show()

    def on_view_task_button(self):
        task_pkey = self.taskItemSelected
        self.view_task_window = ViewTask(self, project_pkey=self.projectItemSelected, task_pkey=task_pkey,
                                         activeUserInstance=self.activeUserInstance)
        self.view_task_window.show()


    """ Log out """
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
        ownerfkey = self.activeUserInstance.user_pkey

        # Create a new project instance
        new_project = Project(name=Pname, desc=Pdesc, start_date=Pstart, due_date=Pdue, status=Pstatus,
                              owner_fkey=ownerfkey, is_removed=0)

        # add project to database
        addProject = new_project.add_project(self.session)

        if addProject == 'successful':
            # update status label
            self.addProjectStatusLabel.setText(f'The project, {Pname}! has now been added.')

            # update project table in home window
            self.home_window_instance.populate_projects_all_table_thread()

            # disable fields
            self.projectNameLE.setEnabled(False)
            self.projectDescTE.setEnabled(False)
            self.projectStatusCB.setEnabled(False)
            self.projectStartDE.setEnabled(False)
            self.projectDueDE.setEnabled(False)
            self.addProjectButton.setEnabled(False)
            self.exitProjectButton.setText('Exit')

            # prompt to add team members
            confirmation = QMessageBox.question(self, "Add Team Members",
                                                "Do you want to add team members to the project now?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                project_pkey = new_project.project_pkey
                self.view_project_window = ViewProject(self.home_window_instance, project_pkey=project_pkey,
                                                       activeUserInstance=self.activeUserInstance)
                self.view_project_window.show()
                self.close()

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

        # load on start
        self.on_load_defaults()

        # buttons
        self.addTaskButton.clicked.connect(self.on_add_task_button)
        self.exitTaskButton.clicked.connect(self.on_exit_without_save)

        # check if fields have changed
        self.taskNameLE.textChanged.connect(self.on_field_changed)
        self.taskDescTE.textChanged.connect(self.on_field_changed)
        self.taskStatusCB.currentTextChanged.connect(self.on_field_changed)
        self.taskStartDE.dateChanged.connect(self.on_field_changed)
        self.taskDueDE.dateChanged.connect(self.on_field_changed)


    def on_load_defaults(self):
        # set date defaults
        self.taskStartDE.setDate(QDate.currentDate())
        self.taskDueDE.setDate(QDate.currentDate())
        # set project name
        self.projectNameLE.setText(self.projectName)
        # disable button
        self.addTaskButton.setEnabled(False)
        # run thread on start
        self.populate_assign_to_thread()

    def populate_assign_to(self):
        project = Project().get_project_team(self.session, self.projectPkey)
        for user in project:
            item_text = f'{user.user.full_name} ({user.user.username})'
            item_data = user.user.user_pkey
            self.AssignToCB.addItem(item_text, item_data)

    def populate_assign_to_thread(self):
        #thread assign to field populate
        populate_assign_to_thread = threading.Thread(target=self.populate_assign_to)
        populate_assign_to_thread.start()
        populate_assign_to_thread.join()

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
        addTask = new_task.add_task(self.session, self.activeUserInstance, self.projectPkey)

        if addTask == 'successful':
            self.addTaskStatusLabel.setText(f'The task, {Tname}! has now been added in to project: {self.projectName}.')
            self.home_window_instance.populate_task_all_table(project_pkey=self.projectPkey)

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
        self.exitTaskButton.setText('Exit (without saving)')




class ViewProject(QDialog, Ui_ViewProjectDialog):
    def __init__(self, home_window_instance, project_pkey, activeUserInstance):
        super().__init__()
        self.setupUi(self)
        self.home_window_instance = home_window_instance
        self.project_pkey = project_pkey
        self.activeUserInstance = activeUserInstance
        self.projectInstance = None
        self.field_changed = False
        self.is_admin = False
        self.is_owner = False
        self.selected_team_user_pkey = None

        # database connection
        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()

        # disable fields
        self.projectNameLE.setReadOnly(True)
        self.projectDescTE.setReadOnly(True)
        self.projectStatusCB.model().item(2).setEnabled(False)
        self.projectStatusCB.setEnabled(False)
        self.projectStartDE.setReadOnly(True)
        self.projectDueDE.setReadOnly(True)
        self.projectEndLE.setReadOnly(True)
        self.projectOwnerLE.setReadOnly(True)
        self.projectProgressHS.setEnabled(False)


        # hide table columns
        self.TeamMembersTable.setColumnHidden(3, True)

        # run functions
        self.get_project_instance()
        self.check_project_status()
        self.check_permissions()
        self.populate_project()
        self.populate_team_members_table_thread()

        # on buttons click
        self.deleteProjectButton.clicked.connect(self.on_delete_project)
        self.saveChangesButton.clicked.connect(self.on_save_changes)
        self.exitWithoutSavingButton.clicked.connect(self.on_exit_without_save)
        self.closeProjectButton.clicked.connect(self.on_close_project)
        self.addMemberButton.clicked.connect(self.on_add_member_button)
        self.removeMemberButton.clicked.connect(self.on_remove_member_button)
        self.TeamMembersTable.itemClicked.connect(self.on_team_members_table_item_clicked)

        # check if fields have changed
        self.projectNameLE.textChanged.connect(self.on_field_changed)
        self.projectDescTE.textChanged.connect(self.on_field_changed)
        self.projectStatusCB.currentTextChanged.connect(self.on_field_changed)
        self.projectStartDE.dateChanged.connect(self.on_field_changed)
        self.projectDueDE.dateChanged.connect(self.on_field_changed)
        self.projectProgressHS.valueChanged.connect(self.on_field_changed)
        self.projectProgressHS.valueChanged.connect(self.project_progress_slider_value_changed)

        # disable buttons
        self.saveChangesButton.setEnabled(False)

    # project population
    def get_project_instance(self):
        p = Project()
        self.projectInstance = p.get_project(self.session, self.project_pkey)

    def populate_project(self):
        self.projectNameLE.setText(self.projectInstance.name)
        self.projectDescTE.setText(self.projectInstance.desc)
        self.projectStatusCB.setCurrentText(self.projectInstance.status)
        self.projectStartDE.setDate(self.projectInstance.start_date)
        self.projectDueDE.setDate(self.projectInstance.due_date)
        self.ppMinL.setText(str(self.projectInstance.project_progress))
        self.projectProgressHS.setValue(self.projectInstance.project_progress)
        if self.projectInstance.end_date:
            self.projectEndLE.setText(self.projectInstance.end_date.strftime("%d/%m/%Y"))

        self.projectOwnerLE.setText(self.projectInstance.owner.full_name)

    def populate_team_members_table(self):
        # project team instance
        pt = Project()
        teamMembers = pt.get_project_team(self.session, self.projectInstance.project_pkey)

        # Populate the projects table
        row = 0
        if teamMembers:
            self.TeamMembersTable.setRowCount(0)
            for teamMember in teamMembers:
                self.TeamMembersTable.insertRow(row)
                self.TeamMembersTable.setItem(row, 0, QtWidgets.QTableWidgetItem(teamMember.user.username))
                self.TeamMembersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(teamMember.user.full_name))
                self.TeamMembersTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(teamMember.start_date)))
                self.TeamMembersTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(teamMember.user.user_pkey)))
                row += 1

    def populate_team_members_table_thread(self):
        populate_team_members_thread = threading.Thread(target=self.populate_team_members_table)
        populate_team_members_thread.start()
        populate_team_members_thread.join()

    def check_project_status(self):
        # if the project has ended then disable fields
        if self.projectInstance.end_date:
            self.disable_view_project_fields()
            self.projectProgressHS.setEnabled(False)
            self.projectStatusCB.setEnabled(False)


    # permissions
    def no_permission_to_perform_action(self):
        if not self.is_admin or not self.is_owner:
            QMessageBox.critical(self, "Permission denied",
                                 "You do not have permissions to perform this action because you are not the owner",
                                 QMessageBox.StandardButton.Close)

    def check_permissions(self):
        # check if active user is owner of project
        if self.projectInstance.owner.username == self.activeUserInstance.username:
            self.is_owner = True
            self.enable_view_project_fields()

        # check if active user is admin
        if self.home_window_instance.activeUserIsAdmin is True:
            self.is_admin = True
            self.enable_view_project_fields()


    # field states
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
        self.projectProgressHS.setEnabled(False)

    def enable_view_project_fields(self):
        self.projectNameLE.setReadOnly(False)
        self.projectDescTE.setReadOnly(False)
        self.projectStartDE.setReadOnly(False)
        self.projectDueDE.setReadOnly(False)
        self.projectEndLE.setReadOnly(False)
        self.projectOwnerLE.setReadOnly(False)
        self.projectStatusCB.setEnabled(True)
        self.projectProgressHS.setEnabled(True)

    def on_field_changed(self):
        self.field_changed = True
        self.saveChangesButton.setEnabled(True)
        self.exitWithoutSavingButton.setText('Exit (without saving')

    def on_exit_without_save(self):
        if self.exitWithoutSavingButton.text() == 'Exit':
            self.close()
        else:
            confirmation = self.confirmation_box("Confirm exit",
                                                 "Are you sure you want to exit without saving the changes?")
            if confirmation == QMessageBox.StandardButton.Yes:
                self.close()

    def project_progress_slider_value_changed(self):
        value = self.projectProgressHS.value()
        self.ppMinL.setText(str(value))


    # on buttons click
    def confirmation_box(self, title, display_text):
        if title and display_text:
            confirmation = QMessageBox.question(self, title, display_text,
                                                QMessageBox.StandardButton.Yes |
                                                QMessageBox.StandardButton.No)
            return confirmation

    def on_delete_project(self):

        # check if user is admin or owner of the project to delete
        if self.is_admin is True or self.is_owner is True:

            # confirmation box to delete project
            confirmation = self.confirmation_box("Confirm Deletion", "Are you sure you want to delete this project?")
            if confirmation == QMessageBox.StandardButton.Yes:

                # delete project
                projectDelete = self.projectInstance.delete_project(self.session, self.activeUserInstance, self.projectInstance.project_pkey)
                if projectDelete == 'Project deleted successfully':

                    Task().delete_tasks_for_project(self.session, self.activeUserInstance, self.project_pkey)
                    # update label
                    self.projectChangesLabel.setText(f'The project, {self.projectInstance.name}! has now been removed.')

                    # refresh projects table to include the new project on dash tab/projects tab
                    if self.home_window_instance.stackedWidget.currentIndex() == 0: # dash tab
                        self.home_window_instance.populate_projects_ongoing_table()

                    if self.home_window_instance.stackedWidget.currentIndex() == 1: # projects tab
                        self.home_window_instance.populate_projects_all_table()

                    # disable fields after deletion
                    self.disable_view_project_fields()

                    # thread send email on project deletion
                    emailSender = EmailSender()
                    emailSender.set_action_user(self.activeUserInstance.user_pkey)
                    emailSender.set_project(self.project_pkey)
                    email_thread = threading.Thread(target=emailSender.on_project_delete)
                    email_thread.start()

                else:
                    return projectDelete
        else:
            self.no_permission_to_perform_action()

    def on_save_changes(self):
        if self.is_admin is True or self.is_owner is True:
            # input from window
            currentName = self.projectNameLE.text()
            currentDesc = self.projectDescTE.toPlainText()
            currentStatus = self.projectStatusCB.currentText()
            currentStartDate = self.projectStartDE.date()
            startDateDT = datetime.date(currentStartDate.year(), currentStartDate.month(), currentStartDate.day())
            Pstart = datetime.datetime.strptime(str(startDateDT), '%Y-%m-%d')
            currentDueDate = self.projectDueDE.date()
            dueDateDT = datetime.date(currentDueDate.year(), currentDueDate.month(), currentDueDate.day())
            Pdue = datetime.datetime.strptime(str(dueDateDT), '%Y-%m-%d')
            projectProgress = int(self.projectProgressHS.value())

            # update project
            updateProject = self.projectInstance.set_project(self.session, self.activeUserInstance, self.projectInstance.project_pkey,
                                                             currentName, currentDesc, currentStatus, Pstart, Pdue,
                                                             projectProgress)
            if updateProject:
                self.projectChangesLabel.setText(f'The project, {currentName}! has now been updated.')
                self.home_window_instance.populate_projects_all_table_thread()
                self.exitWithoutSavingButton.setText('Exit')
                self.saveChangesButton.setEnabled(False)
            else:
                self.projectChangesLabel.setText(updateProject)
        else:
            self.no_permission_to_perform_action()

    def on_close_project(self):
        if self.is_admin is True or self.is_owner is True:
            confirmation = self.confirmation_box("Confirm Project Closure", "Are you sure you want to close this project?")
            if confirmation == QMessageBox.StandardButton.Yes:

                closeProject = self.projectInstance.close_project(self.session, self.activeUserInstance, self.projectInstance.project_pkey)
                if closeProject == 'Project Closed':
                    closeTasks = Task().close_tasks_for_project(self.session, self.activeUserInstance, self.projectInstance.project_pkey)
                    self.projectChangesLabel.setText(f'The project, {self.projectInstance.name}! has now been closed.')
                    self.home_window_instance.populate_projects_all_table_thread()
                    # disable fields after deletion
                    self.disable_view_project_fields()

                    # start email thread to all team members
                    emailSender = EmailSender()
                    emailSender.set_action_user(self.activeUserInstance.user_pkey)
                    emailSender.set_project(self.project_pkey)
                    # Create thread for email
                    email_thread = threading.Thread(target=emailSender.on_project_delete)
                    email_thread.start()
                else:
                    return closeProject
        else:
            self.no_permission_to_perform_action()

    def on_add_member_button(self):
        if self.is_admin is True or self.is_owner is True:
            self.add_member_window = AddTeamMemberDialog(self, projectInstance=self.projectInstance,
                                                         activeUserInstance=self.activeUserInstance)
            self.add_member_window.show()
        else:
            self.no_permission_to_perform_action()

    def on_remove_member_button(self):
        if self.is_admin is True or self.is_owner is True:
            confirmation = self.confirmation_box("Confirm Team Member Removal",
                                                 "Are you sure you want to remove this user from the project?")
            if confirmation == QMessageBox.StandardButton.Yes:
                # delete project team instance
                deleteMember = ProjectTeam().delete_team_member_from_projects(self.session, self.selected_team_user_pkey,
                                                                              self.projectInstance.project_pkey)

                if deleteMember == 'Deleted successfully from teams':
                    self.populate_team_members_table_thread()
                    self.projectChangesLabel.setText(deleteMember)
                    self.removeMemberButton.setEnabled(False)

                    # thread unassign tasks from project
                    unassign_tasks_thread = threading.Thread(target=Task().unassign_tasks_from_project(self.session,
                                                                                                       self.selected_team_user_pkey,
                                                                                                       self.projectInstance.project_pkey))
                    unassign_tasks_thread.start()
                    unassign_tasks_thread.join()

                    # refresh task table on home window
                    self.home_window_instance.populate_task_all_table_thread(project_pkey=self.projectInstance.project_pkey)

                    # start email thread to user who has been removed
                    emailSender = EmailSender()
                    emailSender.set_action_user(self.activeUserInstance.user_pkey)
                    emailSender.set_project(self.projectInstance.project_pkey)
                    emailSender.set_recipient(self.selected_team_user_pkey)
                    # Create thread for email
                    email_thread = threading.Thread(target=emailSender.on_remove_from_project)
                    email_thread.start()

                else:
                    self.projectChangesLabel.setText(deleteMember)
        else:
            self.no_permission_to_perform_action()

    def on_team_members_table_item_clicked(self, item):
        if item:
            self.selected_team_user_pkey = int(self.TeamMembersTable.item(item.row(), 3).text())
            self.removeMemberButton.setEnabled(True)




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
        populate_user_name_thread.join()

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
        projectUser = ProjectTeam(user_fkey=user_pkey, project_fkey=self.projectInstance.project_pkey)
        addToPT = projectUser.add_team_member_to_project(self.session)

        if addToPT == 'successful':
            self.addUserConfirmLE.setText(f'{self.userCB.itemText(index)}! has now been added to {self.projectInstance.name}.')
            self.view_project_instance.populate_team_members_table()

            # thread send email to user who has been added
            emailSender = EmailSender()
            emailSender.set_action_user(self.activeUserInstance.user_pkey)
            emailSender.set_project(self.projectInstance.project_pkey)
            emailSender.set_recipient(user_pkey)
            # Create thread for email
            email_thread = threading.Thread(target=emailSender.on_add_to_project)
            email_thread.start()
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

        self.admin_permissions = False
        self.project_owner_permissions = False
        self.edit_permissions = False
        self.project_owner_fkey = False
        self.assignee_fkey = None
        self.assignee_reassigned = False
        self.field_changed = False
        # disable items in task status drop down
        self.taskStatusCB.model().item(2).setEnabled(False)
        self.taskStatusCB.model().item(3).setEnabled(False)
        self.taskStatusCB.model().item(4).setEnabled(False)

        # database connection
        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()

        # on start
        self.load_defaults()

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
        self.taskAssigneeCB.currentTextChanged.connect(self.on_field_changed) # bug with this field, activating exit without saving
        self.taskProgressHS.valueChanged.connect(self.on_field_changed)
        self.taskProgressHS.valueChanged.connect(self.task_progress_slider_value_changed)

        # disable buttons
        self.saveChangesButton.setEnabled(False)

    def load_defaults(self):
        # disable fields
        self.taskNameLE.setReadOnly(True)
        self.taskDescTE.setReadOnly(True)
        self.taskStartDE.setReadOnly(True)
        self.taskDueDE.setReadOnly(True)
        self.taskAssigneeCB.setEnabled(False)

        # run functions
        self.get_project_instance()
        self.get_task_instance()
        self.check_permissions()
        self.populate_task()
        self.check_task_status()
        self.populate_task_assignee_thread()

    def check_task_status(self):
        if self.taskInstance.status == 'Completed':
            self.disable_view_task_fields()
        if self.taskInstance.status == 'Pending Review':
            self.sendReviewtButton.setText('Reject and send back')

    def get_project_instance(self):
        p = Project()
        self.projectInstance = p.get_project(self.session, self.project_pkey)

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

        self.taskAssignerLE.setText(f'{self.taskInstance.assigner.full_name} ({self.taskInstance.assigner.username})')
        self.taskAssigneeCB.setCurrentText(f'{self.taskInstance.assignee.full_name} ({self.taskInstance.assignee.username})')
        self.project_owner_fkey = self.taskInstance.project.owner_fkey

    def populate_task_assignee(self):
        pt = Project()
        project = pt.get_project_team(self.session, self.project_pkey)

        for user in project:
            item_text = f'{user.user.full_name} ({user.user.username})'
            item_data = user.user.user_pkey
            self.taskAssigneeCB.addItem(item_text, item_data)

    def populate_task_assignee_thread(self):
        #thread assign to field populate
        populate_assign_to_thread = threading.Thread(target=self.populate_task_assignee)
        populate_assign_to_thread.start()
        populate_assign_to_thread.join()

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
        self.taskProgressHS.setEnabled(False)
        self.sendReviewtButton.setEnabled(False)

    def enable_edit_features(self):
        self.taskNameLE.setReadOnly(False)
        self.taskDescTE.setReadOnly(False)
        self.taskStartDE.setReadOnly(False)
        self.taskDueDE.setReadOnly(False)
        self.taskAssigneeCB.setEnabled(True)
        self.taskStatusCB.setEnabled(True)

    def check_permissions(self):
        # if active user is project owner
        if self.projectInstance.owner.username == self.activeUserInstance.username:
            self.project_owner_permissions = True
            self.edit_permissions = True
            self.enable_edit_features()

        # if active user is admin
        if self.home_window_instance.activeUserIsAdmin is True:
            self.admin_permissions = True
            self.edit_permissions = True
            self.enable_edit_features()

        # check if task is assigned to active  user
        if self.taskInstance.assignee.username == self.activeUserInstance.username:
            self.edit_permissions = True

    def no_permission_to_perform_action(self):
        if self.taskInstance.assignee_fkey != self.activeUserInstance.user_pkey:
            QMessageBox.critical(self, "Permission denied", "You do not have permissions to perform this action"
                                                            "\n because you are not the assigned user.",
                                 QMessageBox.StandardButton.Close)
        else:
            QMessageBox.critical(self, "Permission denied", "You do not have permissions to perform this action"
                                                            "\n because you are not the project owner.",
                                 QMessageBox.StandardButton.Close)

    def on_field_changed(self):
        self.field_changed = True
        self.saveChangesButton.setEnabled(True)
        self.exitWithoutSavingButton.setText('Exit (without saving')

    def task_progress_slider_value_changed(self):
        value = self.taskProgressHS.value()
        self.tpMinL.setText(str(value))

    # on button functions
    def confirmation_box(self, title, message):
        return QMessageBox.question(self, title, message, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    def on_delete_task(self):
        # check if user has permissions
        if self.admin_permissions is True or self.project_owner_permissions is True:
            confirmation = self.confirmation_box('Confirm Deletion', 'Are you sure you want to delete this task?')

            if confirmation == QMessageBox.StandardButton.Yes:
                delete_task = self.taskInstance.delete_task(self.session, self.activeUserInstance, self.project_pkey, self.task_pkey)

                if delete_task == 'Task deleted successfully':
                    # update table
                    self.taskChangesLabel.setText(f'The Task, {self.taskInstance.name}! has now been removed.')
                    self.home_window_instance.populate_task_all_table_thread(project_pkey=self.project_pkey)
                    # disable fields after deletion
                    self.disable_view_task_fields()
                else:
                    return delete_task
        else:
            self.no_permission_to_perform_action()

    def on_save_changes(self):
        # check if user has permissions
        if self.edit_permissions is False:
            self.no_permission_to_perform_action()
        else:
            # input from window
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
            taskProgress = int(self.taskProgressHS.value())

            # # check if assignee has been reassigned
            AssignToCBIndex = self.taskAssigneeCB.currentIndex()
            if self.taskAssigneeCB.itemData(AssignToCBIndex) is None or (str(self.taskAssigneeCB.itemData(AssignToCBIndex)) == str(self.taskInstance.assignee_fkey)):
                self.assignee_fkey = self.taskInstance.assignee_fkey
            else:
                self.assignee_fkey = int(self.taskAssigneeCB.itemData(AssignToCBIndex))
                self.assignee_reassigned = True

            #pass variables to update
            update_task = self.taskInstance.set_task(session=self.session, userInstance=self.activeUserInstance,
                                                     project_pkey=self.project_pkey, task_pkey=self.task_pkey,
                                                     setName=currentTaskName, setDesc=currentDesc,
                                                     setStatus=currentStatus, setTaskProgress=taskProgress,
                                                     setStartDate=Pstart, setDueDate=Pdue, setAssigneeFkey=self.assignee_fkey)

            # if task has been updated
            if update_task == 'Task updated':
                self.taskChangesLabel.setText(f'The task, {currentTaskName}! has now been updated.')
                self.home_window_instance.populate_task_all_table_thread(project_pkey=self.project_pkey)
                self.exitWithoutSavingButton.setText('Exit')
                self.saveChangesButton.setEnabled(False)

                # send email if assignee as changed
                if self.assignee_reassigned:
                    emailSender = EmailSender()
                    emailSender.set_recipient(self.assignee_fkey)
                    emailSender.set_action_user(self.activeUserInstance.user_pkey)
                    emailSender.set_project(self.project_pkey)
                    emailSender.set_task_name(currentTaskName)

                    # Create thread for email
                    email_thread = threading.Thread(target=emailSender.on_task_assign)
                    email_thread.start()
            else:
                self.taskChangesLabel.setText(update_task)

    def on_exit_without_save(self):
        if self.exitWithoutSavingButton.text() == 'Exit':
            self.close()
        else:
            confirmation = self.confirmation_box('Confirm exit', 'Are you sure you want to exit without saving the changes?')
            if confirmation == QMessageBox.StandardButton.Yes:
                self.close()

    def on_close_task(self):
        # check if user has permissions
        if self.admin_permissions is True or self.project_owner_permissions is True:
            confirmation = self.confirmation_box('Confirm Task Closure', 'Are you sure you want to end and mark this task as complete?')
            if confirmation == QMessageBox.StandardButton.Yes:
                # close task
                close_task = self.taskInstance.close_task(self.session, self.activeUserInstance, self.project_pkey, self.task_pkey)

                # if task has been closed
                if close_task == 'Task Closed':
                    self.taskChangesLabel.setText(f'The task, {self.taskInstance.name}! has now been closed.')
                    self.taskProgressHS.setValue(100)
                    self.tpMinL.setText(str(100))
                    self.taskStatusCB.setCurrentText('Completed')
                    self.taskEndLE.setText(dt.utcnow().strftime('%d/%m/%Y %H:%M:%S'))
                    self.exitWithoutSavingButton.setText('Exit')
                    self.home_window_instance.populate_task_all_table_thread(project_pkey=self.project_pkey)

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
                    self.taskChangesLabel.setText(f'{close_task}')
                    return close_task
        else:
            self.no_permission_to_perform_action()

    def fail_review_confirmation(self):
        """Fail review of task"""
        confirmation = self.confirmation_box('Confirm Fail Review', 'Are you sure you want to fail the review?')
        if confirmation == QMessageBox.StandardButton.Yes:
            currentTaskName = self.taskNameLE.text()
            updateTask = self.taskInstance.set_task(self.session, self.activeUserInstance, self.project_pkey, self.task_pkey, setStatus='In-Progress')
            if updateTask == 'Task updated':
                self.taskStatusCB.setCurrentText('In-Progress')
                self.taskChangesLabel.setText(f'The task, {currentTaskName}! has now been sent back.')
                self.home_window_instance.populate_task_all_table_thread(project_pkey=self.project_pkey)
                self.sendReviewtButton.setEnabled(False)
                self.saveChangesButton.setEnabled(False)
                self.exitWithoutSavingButton.setText('Exit')
            else:
                self.taskChangesLabel.setText(updateTask)

    def send_for_review(self):
        confirmation = self.confirmation_box('Confirm Task Review', 'Are you sure you want to send this task for review?')
        if confirmation == QMessageBox.StandardButton.Yes:
            currentTaskName = self.taskNameLE.text()
            updateTask = self.taskInstance.set_task(self.session, self.activeUserInstance, self.project_pkey, self.task_pkey, setStatus='Pending Review')
            if updateTask == 'Task updated':
                self.taskStatusCB.setCurrentText('Pending Review')
                self.taskChangesLabel.setText(f'The task, {currentTaskName}! has now been sent for review.')
                self.home_window_instance.populate_task_all_table_thread(project_pkey=self.project_pkey)
                self.sendReviewtButton.setEnabled(False)
                self.saveChangesButton.setEnabled(False)
                self.exitWithoutSavingButton.setText('Exit')
            else:
                self.taskChangesLabel.setText(updateTask)

    def on_send_for_review(self):
        # check if user has permissions and task is in pending review
        if (self.admin_permissions is True or self.project_owner_permissions is True) and self.taskInstance.status == 'Pending Review':
            self.fail_review_confirmation()

        # check if user has permissions and task is not in pending review
        elif self.edit_permissions is True and self.taskInstance.status != 'Pending Review':
            self.send_for_review()

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