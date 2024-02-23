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
from generated.ViewTaskDialog import Ui_ViewTaskDialog
from generated.AddTaskDialog import Ui_AddTaskDialog
from generated.ViewProjectAddTeamMemberDialog import Ui_ViewProjectAddTeamMemberDialog

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



import sys
import datetime



class HomeWindow(QMainWindow, Ui_HomeWindow):
    def __init__(self, activeUser):
        super().__init__()
        self.setupUi(self)
        self.activeUser = activeUser
        self.projectNameItemSelected = None
        self.projectItemSelected = None
        self.taskItemSelected = None

        # Hide pkey for tables
        self.ProjectsOngoingTable.setColumnHidden(0, True)
        self.ProjectsAllTable.setColumnHidden(0, True)
        self.TasksOngoingTable.setColumnHidden(0, True)
        self.TaskAllTable.setColumnHidden(0, True)
        self.TaskAllTable.setColumnHidden(2, True)
        self.taskProjectTable.setColumnHidden(0, True)

        # Run functions on start
        self.populate_projects_ongoing_table()
        self.populate_tasks_ongoing_table()
        self.plot_project_gantt_chart()

        # On button click
        self.dashButton.clicked.connect(self.on_dash_button)
        self.projectsButton.clicked.connect(self.on_projects_button)
        self.AddProjectButton.clicked.connect(self.on_add_project_button)
        self.addCommentButton.clicked.connect(self.on_add_project_comment_button)
        self.ViewProjectButton.clicked.connect(self.on_view_project_button)
        self.tasksButton.clicked.connect(self.on_tasks_button)
        self.addTaskCommentButton.clicked.connect(self.on_add_task_comment_button)
        self.ViewTaskButton.clicked.connect(self.on_view_task_button)
        self.AddTaskButton.clicked.connect(self.on_add_task_button)

        # on table click
        self.ProjectsAllTable.itemClicked.connect(self.on_project_all_table_item_clicked)
        self.ProjectsOngoingTable.itemClicked.connect(self.on_project_ongoing_table_item_clicked)
        self.taskProjectTable.itemClicked.connect(self.on_task_project_all_table_item_clicked)
        self.TaskAllTable.itemClicked.connect(self.on_task_table_item_clicked)



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


    def populate_tasks_ongoing_table(self, projectPkey=None):
        #clear table
        self.TasksOngoingTable.setRowCount(0)

        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        # project instance
        t = Task()
        if projectPkey:
            tasks = t.get_tasks_for_team_member(session, self.activeUser, projectPkey=projectPkey)
        else:
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
            self.populate_tasks_ongoing_table(projectPkey=int(projectPkey))


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


    def on_add_project_comment_button(self):
        # get comment
        commentToAdd = self.newCommentTE.toPlainText()

        # Create a session
        db = DatabaseConnection()
        session = db.get_session()
        # get user fkey
        user = User()
        userFkey = user.get_user_fkey(session, self.activeUser)
        # get project fkey
        projectFkey = self.projectItemSelected

        # add comment
        new_comment = CommunicationLog(user_fkey=userFkey, project_fkey=projectFkey, task_fkey=-1, comment=commentToAdd,
                                       timestamp=datetime.datetime.now())
        addComment = new_comment.add_comment(session)

        if addComment == 'successful':
            self.populate_project_comments(projectPkey=projectFkey)
            self.newCommentTE.clear()
        else:
            print(addComment)

    def on_project_all_table_item_clicked(self, item):
        # get project name
        row = item.row()
        project = self.ProjectsAllTable.item(row, 0).text()
        self.projectItemSelected = int(project)
        self.projectNameItemSelected = self.ProjectsAllTable.item(row, 1).text()
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

    ####tasks dashboard
    def on_tasks_button(self):
        self.stackedWidget.setCurrentIndex(2)
        self.TaskAllTable.setRowCount(0)
        self.populate_task_project_table()

    def populate_task_project_table(self):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        # project instance
        p = Project()
        projects = p.get_projects(session)

        # Populate the projects table
        row = 0
        if projects:
            self.taskProjectTable.setRowCount(0)
            for project in projects:
                self.taskProjectTable.insertRow(row)
                self.taskProjectTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(project.project_pkey)))
                self.taskProjectTable.setItem(row, 1, QtWidgets.QTableWidgetItem(project.name))


    def populate_task_all_table(self, projectPKEY = None):
        #clear table
        self.TaskAllTable.setRowCount(0)

        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        # task instance
        t = Task()
        if projectPKEY:
            tasks = t.get_tasks(session, projectPKEY)
        else:
            tasks = t.get_tasks(session)

        # Populate the tasks table
        row = 0
        if tasks:
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
        if item is None:
            self.populate_task_all_table()

        else:
            self.taskCommentListWidget.clear()
            row = item.row()
            project = self.taskProjectTable.item(row, 0).text()
            self.populate_task_all_table(projectPKEY=int(project))
            self.projectItemSelected = int(project)
            self.projectNameItemSelected = self.taskProjectTable.item(row, 1).text()


    def populate_task_comments(self, taskPkey):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        comLog = CommunicationLog()
        taskLog = comLog.get_task_communication_log(session, taskPkey)
        self.taskCommentListWidget.clear()
        for log in taskLog:
            self.taskCommentListWidget.addItem('')
            self.taskCommentListWidget.addItem(f'Posted: {log.timestamp}, User: {log.user.full_name} \n {log.comment} ')


    def on_task_table_item_clicked(self, item):
        if item is None:
            self.populate_task_all_table()
        else:
            # get project name
            row = item.row()
            project = self.TaskAllTable.item(row, 0).text()
            task = self.TaskAllTable.item(row, 2).text()
            self.projectItemSelected = int(project)
            self.projectNameItemSelected = self.TaskAllTable.item(row, 1).text()
            self.taskItemSelected = int(task)
            self.populate_task_comments(taskPkey=int(task))

    def on_add_task_comment_button(self):
        # get comment
        commentToAdd = self.newTaskCommentTE.toPlainText()

        # Create a session
        db = DatabaseConnection()
        session = db.get_session()
        # get user fkey
        user = User()
        userFkey = user.get_user_fkey(session, self.activeUser)
        # get project fkey
        projectFkey = self.projectItemSelected
        # get task fkey
        taskFkey = self.taskItemSelected

        # add comment
        new_comment = CommunicationLog(user_fkey=userFkey, project_fkey=projectFkey, task_fkey=taskFkey, comment=commentToAdd,
                                       timestamp=datetime.datetime.now())
        addComment = new_comment.add_comment(session)

        if addComment == 'successful':
            self.populate_task_comments(taskPkey=taskFkey)
            self.newTaskCommentTE.clear()
        else:
            print(addComment)



    def on_add_project_button(self):
        self.add_project_window = AddProject(self, activeUser=self.activeUser)
        self.add_project_window.show()

    def on_view_project_button(self):
        projectPk = self.projectItemSelected
        self.view_project_window = ViewProject(self, projectPkey=projectPk, activeUser=self.activeUser)
        self.view_project_window.show()

    def on_view_task_button(self):
        taskPk = self.taskItemSelected
        self.view_task_window = ViewTask(self, projectPkey=self.projectItemSelected, taskPkey=taskPk, activeUser=self.activeUser)
        self.view_task_window.show()

    def on_add_task_button(self):
        self.add_task_window = AddTask(self, projectName=self.projectNameItemSelected, projectPkey=self.projectItemSelected, activeUser=self.activeUser)
        self.add_task_window.show()


class AddProject(QDialog, Ui_AddProjectDialog):
    def __init__(self, home_window_instance, activeUser):
        super().__init__()
        self.setupUi(self)
        self.activeUser = activeUser
        self.field_changed = False
        self.home_window_instance = home_window_instance

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
            self.exitProjectButton.setText('Exit')
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
    def __init__(self, home_window_instance, projectName, projectPkey, activeUser):
        super().__init__()
        self.setupUi(self)
        self.activeUser = activeUser
        self.projectName = projectName
        self.projectPkey = projectPkey
        self.field_changed = False
        self.home_window_instance = home_window_instance

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



    def on_add_task_button(self):
        # Create a session
        db = DatabaseConnection()
        session = db.get_session()

        # get assigner fkey
        assigner = User()
        assignerfkey = assigner.get_user_fkey(session, self.activeUser)

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

        # db session
        dbCon = DatabaseConnection()
        session = dbCon.get_session()

        # Create a new task instance
        new_task = Task(project_fkey=self.projectPkey, name=Tname, desc=Tdesc, start_date=Tstart, due_date=Tdue, status=Tstatus,
                        assigner_fkey=assignerfkey, assignee_fkey=-1, is_removed=0)
        # add project to db
        addTask = new_task.add_task(session)

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
    def __init__(self, home_window_instance, projectPkey, activeUser):
        super().__init__()
        self.setupUi(self)
        self.home_window_instance = home_window_instance
        self.projectPkey = projectPkey
        self.projectName = None
        self.activeUser = activeUser
        self.field_changed = False
        self.is_admin_or_owner = False

        # run functions
        self.populate_project()
        self.populate_team_members_table()
        self.check_if_user_is_admin_or_owner()
        self.set_projectName()

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

    def set_projectName(self):
        self.projectName = self.projectNameLE.text()
    def no_permission_to_perform_action(self):
        QMessageBox.critical(self, "Permission denied", "You do not have permissions to perform this action",
                             QMessageBox.StandardButton.Close)

    def check_if_user_is_admin_or_owner(self):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()

        # is project owner
        p = Project()
        projectSelected = p.get_project(session, self.projectPkey)
        for project in projectSelected:
            if project.owner.username == self.activeUser:
                self.is_admin_or_owner = True
                break

        # is admin
        u = User()
        activeUser = u.get_user(session, self.activeUser)
        for user in activeUser:
            for userRole in user.user_roles:
                if userRole.role_type == 'Admin':
                    self.is_admin_or_owner = True
                    break

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
                self.projectEndLE.setText(project.end_date.strftime("%d/%m/%Y"))

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
        if self.is_admin_or_owner is False:
            self.no_permission_to_perform_action()
        else:
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
                    self.disable_view_project_fields()

                else:
                    return projectDelete
            else:
                # Cancelled by the user
                return

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

            # Create a database connection
            db = DatabaseConnection()
            session = db.get_session()
            p = Project()
            updateProject = p.set_project(session, self.projectPkey, currentName, currentDesc,
                                          currentStatus, Pstart, Pdue)

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
                # Create a database connection
                db = DatabaseConnection()
                session = db.get_session()
                # project instance
                p = Project()
                projects = p.get_project(session, self.projectPkey)
                for project in projects:
                    projectName = project.name
                closeProject = p.close_project(session, self.projectPkey)
                if closeProject == 'Project Closed':
                    self.projectChangesLabel.setText(f'The project, {projectName}! has now been closed.')
                    self.home_window_instance.populate_projects_all_table()

                    # disable fields after deletion
                    self.disable_view_project_fields()
                else:
                    return closeProject
            else:
                return

    def disable_view_project_fields(self):
        self.projectNameLE.setEnabled(False)
        self.projectDescTE.setEnabled(False)
        self.projectStatusCB.setEnabled(False)
        self.projectStartDE.setEnabled(False)
        self.projectDueDE.setEnabled(False)
        self.projectEndLE.setEnabled(False)
        self.projectOwnerLE.setEnabled(False)
        self.saveChangesButton.setEnabled(False)
        #self.exitWithoutSavingButton.setEnabled(False)
        self.closeProjectButton.setEnabled(False)
        self.deleteProjectButton.setEnabled(False)
        self.TeamMembersTable.setEnabled(False)
        self.addMemberButton.setEnabled(False)
        self.removeMemberButton.setEnabled(False)

    def on_field_changed(self):
        self.field_changed = True
        self.saveChangesButton.setEnabled(True)
        self.exitWithoutSavingButton.setText('Exit (without saving')

    def on_add_member_button(self):
        self.add_member_window = AddTeamMemberDialog(self, projectName=self.projectName,
                                                     projectPkey=self.projectPkey,
                                                     activeUser=self.activeUser)
        self.add_member_window.show()




class AddTeamMemberDialog(QDialog, Ui_ViewProjectAddTeamMemberDialog):
    def __init__(self, view_project_instance, projectName, projectPkey, activeUser):
        super().__init__()
        self.setupUi(self)
        self.view_project_instance = view_project_instance
        self.projectPkey = projectPkey
        self.projectName = projectName
        self.activeUser = activeUser
        self.field_changed = False
        #self.edit_permissions = False

        #run func
        self.populate_project_name()
        self.populate_user_name()

        #on button
        self.addUserButton.clicked.connect(self.on_add_user_button)

    def populate_project_name(self):
        self.projectNameLE.setText(self.projectName)

    def populate_user_name(self):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        u = User()
        users = u.get_users(session)
        row = 0
        for user in users:
            self.userCB.addItem(str(user.user_pkey))
            self.userCB.setItemText(row, f'{user.full_name} ({user.username})')
            row += 1

    def on_add_user_button(self):
        # input from window
        user = self.userCB.itemData()
        print(user)


        # # db session
        # dbCon = DatabaseConnection()
        # session = dbCon.get_session()
        #
        # # Create a new task instance
        # new_task = Task(project_fkey=self.projectPkey, name=Tname, desc=Tdesc, start_date=Tstart, due_date=Tdue, status=Tstatus,
        #                 assigner_fkey=assignerfkey, assignee_fkey=-1, is_removed=0)
        # # add project to db
        # addTask = new_task.add_task(session)
        #
        # if addTask == 'successful':
        #     self.addTaskStatusLabel.setText(f'The task, {Tname}! has now been added in to project: {self.projectName}.')
        #     self.home_window_instance.populate_task_all_table(projectPKEY=self.projectPkey)
        #
        #     # disable fields
        #     self.projectNameLE.setEnabled(False)
        #     self.taskNameLE.setEnabled(False)
        #     self.taskDescTE.setEnabled(False)
        #     self.taskStatusCB.setEnabled(False)
        #     self.taskStartDE.setEnabled(False)
        #     self.taskDueDE.setEnabled(False)
        #     self.addTaskButton.setEnabled(False)
        #     self.exitTaskButton.setText('Exit')
        # else:
        #     self.addTaskStatusLabel.setText(addTask)




class ViewTask(QDialog, Ui_ViewTaskDialog):
    def __init__(self, home_window_instance, projectPkey, taskPkey, activeUser):
        super().__init__()
        self.setupUi(self)
        self.home_window_instance = home_window_instance
        self.projectPkey = projectPkey
        self.taskPkey = taskPkey
        self.activeUser = activeUser
        self.field_changed = False
        self.edit_permissions = False

        # run functions
        self.populate_task()
        self.check_edit_permissions()
        #self.populate_team_members_table()

        # on buttons click
        self.deleteTaskButton.clicked.connect(self.on_delete_task)
        self.saveChangesButton.clicked.connect(self.on_save_changes)
        self.exitWithoutSavingButton.clicked.connect(self.on_exit_without_save)
        self.closeTaskButton.clicked.connect(self.on_close_task)

        # check if fields have changed
        self.taskNameLE.textChanged.connect(self.on_field_changed)
        self.taskDescTE.textChanged.connect(self.on_field_changed)
        self.taskStatusCB.currentTextChanged.connect(self.on_field_changed)
        self.taskStartDE.dateChanged.connect(self.on_field_changed)
        self.taskDueDE.dateChanged.connect(self.on_field_changed)

        # disable buttons
        self.saveChangesButton.setEnabled(False)


    def no_permission_to_perform_action(self):
        QMessageBox.critical(self, "Permission denied", "You do not have permissions to perform this action",
                             QMessageBox.StandardButton.Close)

    def check_edit_permissions(self):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()

        # is task assignee
        t = Task()
        taskSelected = t.get_task(session, self.taskPkey)
        for task in taskSelected:
            if task.assignee.username == self.activeUser:
                self.edit_permissions = True
                break

        # is project owner
        p = Project()
        projectSelected = p.get_project(session, self.projectPkey)
        for project in projectSelected:
            if project.owner.username == self.activeUser:
                self.edit_permissions = True
                break

        # is admin
        u = User()
        activeUser = u.get_user(session, self.activeUser)
        for user in activeUser:
            for userRole in user.user_roles:
                if userRole.role_type == 'Admin':
                    self.edit_permissions = True
                    break

    def populate_task(self):
        # Create a database connection
        db = DatabaseConnection()
        session = db.get_session()
        # task instance
        t = Task()
        taskSelected = t.get_task(session, self.taskPkey)
        for task in taskSelected:
            self.projectNameLE.setText(task.project.name)
            self.taskNameLE.setText(task.name)
            self.taskDescTE.setText(task.desc)
            self.taskStatusCB.setCurrentText(task.status)
            self.taskStartDE.setDate(task.start_date)
            self.taskDueDE.setDate(task.due_date)
            if task.end_date:
                self.taskEndLE.setText(task.end_date.strftime("%d/%m/%Y"))

            self.taskAssignerLE.setText(task.assigner.full_name)
            self.taskAssigneeCB.setCurrentText(task.assignee.full_name)


    def on_delete_task(self):
        if self.edit_permissions is False:
            self.no_permission_to_perform_action()
        else:
            confirmation = QMessageBox.question(self, "Confirm Deletion",
                                                "Are you sure you want to delete this task?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                # Proceed with deletion
                # Create a database connection
                db = DatabaseConnection()
                session = db.get_session()
                # task instance
                t = Task()
                tasks = t.get_task(session, self.taskPkey)
                for task in tasks:
                    taskName = task.name
                taskDelete = t.delete_task(session, self.taskPkey)
                if taskDelete == 'Task deleted successfully':
                    self.taskChangesLabel.setText(f'The Task, {taskName}! has now been removed.')
                    self.home_window_instance.populate_task_all_table(projectPKEY=self.projectPkey)

                    #disable fields after deletion
                    self.disable_view_task_fields()

                else:
                    return taskDelete
            else:
                # Cancelled by the user
                return

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

            # Create a database connection
            db = DatabaseConnection()
            session = db.get_session()
            t = Task()
            updateTask = t.set_task(session, self.taskPkey, currentTaskName, currentDesc,
                                          currentStatus, Pstart, Pdue)

            if updateTask:
                print('updated')
                self.taskChangesLabel.setText(f'The task, {currentTaskName}! has now been updated.')
                self.home_window_instance.populate_task_all_table(projectPKEY=self.projectPkey)
                self.exitWithoutSavingButton.setText('Exit')
                self.saveChangesButton.setEnabled(False)
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
        if self.edit_permissions is False:
            self.no_permission_to_perform_action()
        else:
            confirmation = QMessageBox.question(self, "Confirm Task Closure",
                                                "Are you sure you want to close this task?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmation == QMessageBox.StandardButton.Yes:
                # Create a database connection
                db = DatabaseConnection()
                session = db.get_session()
                # task instance
                t = Task()
                tasks = t.get_task(session, self.taskPkey)
                for task in tasks:
                    taskName = task.name
                closeTask = t.close_task(session, self.taskPkey)
                if closeTask == 'Task Closed':
                    self.taskChangesLabel.setText(f'The task, {taskName}! has now been closed.')
                    self.home_window_instance.populate_task_all_table(projectPKEY=self.projectPkey)

                    # disable fields after deletion
                    self.disable_view_task_fields()
                else:
                    return closeTask
            else:
                return


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
        #self.exitWithoutSavingButton.setEnabled(False)
        self.closeTaskButton.setEnabled(False)
        self.deleteTaskButton.setEnabled(False)
        #self.TeamMembersTable.setEnabled(False)
        #self.addMemberButton.setEnabled(False)
        #self.removeMemberButton.setEnabled(False)

    def on_field_changed(self):
        self.field_changed = True
        self.saveChangesButton.setEnabled(True)
        self.exitWithoutSavingButton.setText('Exit (without saving')





def main():
    app = QApplication(sys.argv)
    window = HomeWindow(activeUser='tm1')
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()