# Form implementation generated from reading ui file 'ui\homeWindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HomeWindow(object):
    def setupUi(self, HomeWindow):
        HomeWindow.setObjectName("HomeWindow")
        HomeWindow.resize(1134, 550)
        self.centralwidget = QtWidgets.QWidget(parent=HomeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(parent=self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.frame_3 = QtWidgets.QFrame(parent=self.splitter)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.layoutWidget = QtWidgets.QWidget(parent=self.frame_3)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 70, 77, 211))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.dashButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.dashButton.setObjectName("dashButton")
        self.verticalLayout_4.addWidget(self.dashButton)
        self.projectsButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.projectsButton.setObjectName("projectsButton")
        self.verticalLayout_4.addWidget(self.projectsButton)
        self.tasksButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.tasksButton.setObjectName("tasksButton")
        self.verticalLayout_4.addWidget(self.tasksButton)
        self.profileButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.profileButton.setObjectName("profileButton")
        self.verticalLayout_4.addWidget(self.profileButton)
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.splitter)
        self.stackedWidget.setObjectName("stackedWidget")
        self.dashboardPage = QtWidgets.QWidget()
        self.dashboardPage.setObjectName("dashboardPage")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.dashboardPage)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame = QtWidgets.QFrame(parent=self.dashboardPage)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_5.addWidget(self.frame)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(parent=self.dashboardPage)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ProjectsOngoingTable = QtWidgets.QTableWidget(parent=self.groupBox)
        self.ProjectsOngoingTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.ProjectsOngoingTable.setObjectName("ProjectsOngoingTable")
        self.ProjectsOngoingTable.setColumnCount(5)
        self.ProjectsOngoingTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.ProjectsOngoingTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ProjectsOngoingTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ProjectsOngoingTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.ProjectsOngoingTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.ProjectsOngoingTable.setHorizontalHeaderItem(4, item)
        self.verticalLayout_2.addWidget(self.ProjectsOngoingTable)
        self.projectPlotFrame = QtWidgets.QFrame(parent=self.groupBox)
        self.projectPlotFrame.setBaseSize(QtCore.QSize(0, 0))
        self.projectPlotFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.projectPlotFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.projectPlotFrame.setObjectName("projectPlotFrame")
        self.verticalLayout_2.addWidget(self.projectPlotFrame)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.dashboardPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.TasksOngoingTable = QtWidgets.QTableWidget(parent=self.groupBox_2)
        self.TasksOngoingTable.setObjectName("TasksOngoingTable")
        self.TasksOngoingTable.setColumnCount(4)
        self.TasksOngoingTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.TasksOngoingTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TasksOngoingTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TasksOngoingTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.TasksOngoingTable.setHorizontalHeaderItem(3, item)
        self.verticalLayout_3.addWidget(self.TasksOngoingTable)
        self.taskPlotFrame = QtWidgets.QFrame(parent=self.groupBox_2)
        self.taskPlotFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.taskPlotFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.taskPlotFrame.setObjectName("taskPlotFrame")
        self.verticalLayout_3.addWidget(self.taskPlotFrame)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.stackedWidget.addWidget(self.dashboardPage)
        self.projectsPage = QtWidgets.QWidget()
        self.projectsPage.setObjectName("projectsPage")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.projectsPage)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_2 = QtWidgets.QFrame(parent=self.projectsPage)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_2 = QtWidgets.QLabel(parent=self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_9.addWidget(self.label_2)
        self.verticalLayout_6.addWidget(self.frame_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.projectsPage)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.ProjectsAllTable = QtWidgets.QTableWidget(parent=self.groupBox_3)
        self.ProjectsAllTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.ProjectsAllTable.setObjectName("ProjectsAllTable")
        self.ProjectsAllTable.setColumnCount(6)
        self.ProjectsAllTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.ProjectsAllTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ProjectsAllTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ProjectsAllTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.ProjectsAllTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.ProjectsAllTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.ProjectsAllTable.setHorizontalHeaderItem(5, item)
        self.verticalLayout_7.addWidget(self.ProjectsAllTable)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ViewProjectButton = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.ViewProjectButton.setObjectName("ViewProjectButton")
        self.horizontalLayout_4.addWidget(self.ViewProjectButton)
        self.AddProjectButton = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.AddProjectButton.setObjectName("AddProjectButton")
        self.horizontalLayout_4.addWidget(self.AddProjectButton)
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self.projectsPage)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.TeamMembersTable = QtWidgets.QTableWidget(parent=self.groupBox_4)
        self.TeamMembersTable.setObjectName("TeamMembersTable")
        self.TeamMembersTable.setColumnCount(3)
        self.TeamMembersTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.TeamMembersTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TeamMembersTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TeamMembersTable.setHorizontalHeaderItem(2, item)
        self.verticalLayout_8.addWidget(self.TeamMembersTable)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.ViewMemberButton = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.ViewMemberButton.setObjectName("ViewMemberButton")
        self.horizontalLayout_6.addWidget(self.ViewMemberButton)
        self.AddMemberButton = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.AddMemberButton.setObjectName("AddMemberButton")
        self.horizontalLayout_6.addWidget(self.AddMemberButton)
        self.verticalLayout_8.addLayout(self.horizontalLayout_6)
        self.verticalLayout_10.addLayout(self.verticalLayout_8)
        self.horizontalLayout_3.addWidget(self.groupBox_4)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.verticalLayout_11.addLayout(self.verticalLayout_6)
        self.stackedWidget.addWidget(self.projectsPage)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.frame_4 = QtWidgets.QFrame(parent=self.page)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_3 = QtWidgets.QLabel(parent=self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_15.addWidget(self.label_3)
        self.verticalLayout_16.addWidget(self.frame_4)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.groupBox_6 = QtWidgets.QGroupBox(parent=self.page)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.TaskAllTable = QtWidgets.QTableWidget(parent=self.groupBox_6)
        self.TaskAllTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.TaskAllTable.setObjectName("TaskAllTable")
        self.TaskAllTable.setColumnCount(5)
        self.TaskAllTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.TaskAllTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TaskAllTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TaskAllTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.TaskAllTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.TaskAllTable.setHorizontalHeaderItem(4, item)
        self.verticalLayout_14.addWidget(self.TaskAllTable)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.ViewProjectButton_2 = QtWidgets.QPushButton(parent=self.groupBox_6)
        self.ViewProjectButton_2.setObjectName("ViewProjectButton_2")
        self.horizontalLayout_5.addWidget(self.ViewProjectButton_2)
        self.AddProjectButton_2 = QtWidgets.QPushButton(parent=self.groupBox_6)
        self.AddProjectButton_2.setObjectName("AddProjectButton_2")
        self.horizontalLayout_5.addWidget(self.AddProjectButton_2)
        self.verticalLayout_14.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_8.addWidget(self.groupBox_6)
        self.groupBox_5 = QtWidgets.QGroupBox(parent=self.page)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.TeamMemberTable1 = QtWidgets.QTableWidget(parent=self.groupBox_5)
        self.TeamMemberTable1.setObjectName("TeamMemberTable1")
        self.TeamMemberTable1.setColumnCount(3)
        self.TeamMemberTable1.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.TeamMemberTable1.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TeamMemberTable1.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TeamMemberTable1.setHorizontalHeaderItem(2, item)
        self.verticalLayout_13.addWidget(self.TeamMemberTable1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.ViewMemberButton_2 = QtWidgets.QPushButton(parent=self.groupBox_5)
        self.ViewMemberButton_2.setObjectName("ViewMemberButton_2")
        self.horizontalLayout_7.addWidget(self.ViewMemberButton_2)
        self.AddMemberButton_2 = QtWidgets.QPushButton(parent=self.groupBox_5)
        self.AddMemberButton_2.setObjectName("AddMemberButton_2")
        self.horizontalLayout_7.addWidget(self.AddMemberButton_2)
        self.verticalLayout_13.addLayout(self.horizontalLayout_7)
        self.verticalLayout_12.addLayout(self.verticalLayout_13)
        self.horizontalLayout_8.addWidget(self.groupBox_5)
        self.verticalLayout_16.addLayout(self.horizontalLayout_8)
        self.stackedWidget.addWidget(self.page)
        self.horizontalLayout.addWidget(self.splitter)
        HomeWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=HomeWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1134, 22))
        self.menubar.setObjectName("menubar")
        HomeWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=HomeWindow)
        self.statusbar.setObjectName("statusbar")
        HomeWindow.setStatusBar(self.statusbar)

        self.retranslateUi(HomeWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(HomeWindow)

    def retranslateUi(self, HomeWindow):
        _translate = QtCore.QCoreApplication.translate
        HomeWindow.setWindowTitle(_translate("HomeWindow", "MainWindow"))
        self.dashButton.setText(_translate("HomeWindow", "Dashboard"))
        self.projectsButton.setText(_translate("HomeWindow", "Projects"))
        self.tasksButton.setText(_translate("HomeWindow", "Tasks"))
        self.profileButton.setText(_translate("HomeWindow", "Profile"))
        self.label.setText(_translate("HomeWindow", "Dashboard"))
        self.groupBox.setTitle(_translate("HomeWindow", "Ongoing Projects"))
        item = self.ProjectsOngoingTable.horizontalHeaderItem(0)
        item.setText(_translate("HomeWindow", "Project"))
        item = self.ProjectsOngoingTable.horizontalHeaderItem(1)
        item.setText(_translate("HomeWindow", "Start Date"))
        item = self.ProjectsOngoingTable.horizontalHeaderItem(2)
        item.setText(_translate("HomeWindow", "Due Date"))
        item = self.ProjectsOngoingTable.horizontalHeaderItem(3)
        item.setText(_translate("HomeWindow", "Status"))
        item = self.ProjectsOngoingTable.horizontalHeaderItem(4)
        item.setText(_translate("HomeWindow", "Owner"))
        self.groupBox_2.setTitle(_translate("HomeWindow", "Assigned Tasks"))
        item = self.TasksOngoingTable.horizontalHeaderItem(0)
        item.setText(_translate("HomeWindow", "Task"))
        item = self.TasksOngoingTable.horizontalHeaderItem(1)
        item.setText(_translate("HomeWindow", "Start Date"))
        item = self.TasksOngoingTable.horizontalHeaderItem(2)
        item.setText(_translate("HomeWindow", "Due Date"))
        item = self.TasksOngoingTable.horizontalHeaderItem(3)
        item.setText(_translate("HomeWindow", "Status"))
        self.label_2.setText(_translate("HomeWindow", "Projects"))
        self.groupBox_3.setTitle(_translate("HomeWindow", "Projects "))
        item = self.ProjectsAllTable.horizontalHeaderItem(0)
        item.setText(_translate("HomeWindow", "Project"))
        item = self.ProjectsAllTable.horizontalHeaderItem(1)
        item.setText(_translate("HomeWindow", "Start Date"))
        item = self.ProjectsAllTable.horizontalHeaderItem(2)
        item.setText(_translate("HomeWindow", "Due Date"))
        item = self.ProjectsAllTable.horizontalHeaderItem(3)
        item.setText(_translate("HomeWindow", "End Date"))
        item = self.ProjectsAllTable.horizontalHeaderItem(4)
        item.setText(_translate("HomeWindow", "Status"))
        item = self.ProjectsAllTable.horizontalHeaderItem(5)
        item.setText(_translate("HomeWindow", "Owner"))
        self.ViewProjectButton.setText(_translate("HomeWindow", "View Project"))
        self.AddProjectButton.setText(_translate("HomeWindow", "Add Project"))
        self.groupBox_4.setTitle(_translate("HomeWindow", "Team Members"))
        item = self.TeamMembersTable.horizontalHeaderItem(0)
        item.setText(_translate("HomeWindow", "Username"))
        item = self.TeamMembersTable.horizontalHeaderItem(1)
        item.setText(_translate("HomeWindow", "Name"))
        item = self.TeamMembersTable.horizontalHeaderItem(2)
        item.setText(_translate("HomeWindow", "Start Date"))
        self.ViewMemberButton.setText(_translate("HomeWindow", "View Member"))
        self.AddMemberButton.setText(_translate("HomeWindow", "Add Member"))
        self.label_3.setText(_translate("HomeWindow", "Tasks"))
        self.groupBox_6.setTitle(_translate("HomeWindow", "Tasks"))
        item = self.TaskAllTable.horizontalHeaderItem(0)
        item.setText(_translate("HomeWindow", "Project"))
        item = self.TaskAllTable.horizontalHeaderItem(1)
        item.setText(_translate("HomeWindow", "Start Date"))
        item = self.TaskAllTable.horizontalHeaderItem(2)
        item.setText(_translate("HomeWindow", "Due Date"))
        item = self.TaskAllTable.horizontalHeaderItem(3)
        item.setText(_translate("HomeWindow", "End Date"))
        item = self.TaskAllTable.horizontalHeaderItem(4)
        item.setText(_translate("HomeWindow", "Status"))
        self.ViewProjectButton_2.setText(_translate("HomeWindow", "View Project"))
        self.AddProjectButton_2.setText(_translate("HomeWindow", "Add Project"))
        self.groupBox_5.setTitle(_translate("HomeWindow", "Team Members"))
        item = self.TeamMemberTable1.horizontalHeaderItem(0)
        item.setText(_translate("HomeWindow", "Username"))
        item = self.TeamMemberTable1.horizontalHeaderItem(1)
        item.setText(_translate("HomeWindow", "Name"))
        item = self.TeamMemberTable1.horizontalHeaderItem(2)
        item.setText(_translate("HomeWindow", "Start Date"))
        self.ViewMemberButton_2.setText(_translate("HomeWindow", "View Member"))
        self.AddMemberButton_2.setText(_translate("HomeWindow", "Add Member"))
