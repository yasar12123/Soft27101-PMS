# Form implementation generated from reading ui file 'ui\viewProjectDialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ViewProjectDialog(object):
    def setupUi(self, ViewProjectDialog):
        ViewProjectDialog.setObjectName("ViewProjectDialog")
        ViewProjectDialog.resize(853, 598)
        self.gridLayout_3 = QtWidgets.QGridLayout(ViewProjectDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_3 = QtWidgets.QGroupBox(parent=ViewProjectDialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.TeamMembersTable = QtWidgets.QTableWidget(parent=self.groupBox_3)
        self.TeamMembersTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.TeamMembersTable.setObjectName("TeamMembersTable")
        self.TeamMembersTable.setColumnCount(4)
        self.TeamMembersTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.TeamMembersTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TeamMembersTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TeamMembersTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.TeamMembersTable.setHorizontalHeaderItem(3, item)
        self.verticalLayout_8.addWidget(self.TeamMembersTable)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.removeMemberButton = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.removeMemberButton.setEnabled(False)
        self.removeMemberButton.setObjectName("removeMemberButton")
        self.horizontalLayout_6.addWidget(self.removeMemberButton)
        self.addMemberButton = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.addMemberButton.setObjectName("addMemberButton")
        self.horizontalLayout_6.addWidget(self.addMemberButton)
        self.verticalLayout_8.addLayout(self.horizontalLayout_6)
        self.verticalLayout.addLayout(self.verticalLayout_8)
        self.gridLayout_3.addWidget(self.groupBox_3, 1, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(parent=ViewProjectDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.projectEndLE = QtWidgets.QLineEdit(parent=self.groupBox)
        self.projectEndLE.setReadOnly(True)
        self.projectEndLE.setClearButtonEnabled(False)
        self.projectEndLE.setObjectName("projectEndLE")
        self.gridLayout.addWidget(self.projectEndLE, 5, 2, 1, 1)
        self.projectStartDE = QtWidgets.QDateEdit(parent=self.groupBox)
        self.projectStartDE.setCalendarPopup(True)
        self.projectStartDE.setObjectName("projectStartDE")
        self.gridLayout.addWidget(self.projectStartDE, 3, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 6, 0, 1, 1)
        self.projectOwnerLE = QtWidgets.QLineEdit(parent=self.groupBox)
        self.projectOwnerLE.setReadOnly(True)
        self.projectOwnerLE.setObjectName("projectOwnerLE")
        self.gridLayout.addWidget(self.projectOwnerLE, 6, 2, 1, 1)
        self.projectDescTE = QtWidgets.QTextEdit(parent=self.groupBox)
        self.projectDescTE.setObjectName("projectDescTE")
        self.gridLayout.addWidget(self.projectDescTE, 1, 2, 1, 1)
        self.projectNameLE = QtWidgets.QLineEdit(parent=self.groupBox)
        self.projectNameLE.setObjectName("projectNameLE")
        self.gridLayout.addWidget(self.projectNameLE, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)
        self.projectStatusCB = QtWidgets.QComboBox(parent=self.groupBox)
        self.projectStatusCB.setAcceptDrops(False)
        self.projectStatusCB.setObjectName("projectStatusCB")
        self.projectStatusCB.addItem("")
        self.projectStatusCB.addItem("")
        self.projectStatusCB.addItem("")
        self.gridLayout.addWidget(self.projectStatusCB, 2, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.projectDueDE = QtWidgets.QDateEdit(parent=self.groupBox)
        self.projectDueDE.setCalendarPopup(True)
        self.projectDueDE.setObjectName("projectDueDE")
        self.gridLayout.addWidget(self.projectDueDE, 4, 2, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(parent=self.groupBox)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ppMinL = QtWidgets.QLabel(parent=self.groupBox_5)
        self.ppMinL.setObjectName("ppMinL")
        self.horizontalLayout_3.addWidget(self.ppMinL)
        self.projectProgressHS = QtWidgets.QSlider(parent=self.groupBox_5)
        self.projectProgressHS.setMaximum(100)
        self.projectProgressHS.setSingleStep(10)
        self.projectProgressHS.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.projectProgressHS.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.projectProgressHS.setTickInterval(20)
        self.projectProgressHS.setObjectName("projectProgressHS")
        self.horizontalLayout_3.addWidget(self.projectProgressHS)
        self.ppmax = QtWidgets.QLabel(parent=self.groupBox_5)
        self.ppmax.setObjectName("ppmax")
        self.horizontalLayout_3.addWidget(self.ppmax)
        self.gridLayout.addWidget(self.groupBox_5, 7, 2, 1, 1)
        self.label_13 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 7, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.projectChangesLabel = QtWidgets.QLabel(parent=self.groupBox)
        self.projectChangesLabel.setText("")
        self.projectChangesLabel.setObjectName("projectChangesLabel")
        self.verticalLayout_3.addWidget(self.projectChangesLabel)
        self.frame_3 = QtWidgets.QFrame(parent=self.groupBox)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.frame_3)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.saveChangesButton = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.saveChangesButton.setObjectName("saveChangesButton")
        self.verticalLayout_2.addWidget(self.saveChangesButton)
        self.exitWithoutSavingButton = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.exitWithoutSavingButton.setObjectName("exitWithoutSavingButton")
        self.verticalLayout_2.addWidget(self.exitWithoutSavingButton)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self.frame_3)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.closeProjectButton = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.closeProjectButton.setObjectName("closeProjectButton")
        self.horizontalLayout.addWidget(self.closeProjectButton)
        self.deleteProjectButton = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.deleteProjectButton.setObjectName("deleteProjectButton")
        self.horizontalLayout.addWidget(self.deleteProjectButton)
        self.verticalLayout_4.addWidget(self.groupBox_4)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.gridLayout_3.addWidget(self.groupBox, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(parent=ViewProjectDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 2)

        self.retranslateUi(ViewProjectDialog)
        QtCore.QMetaObject.connectSlotsByName(ViewProjectDialog)

    def retranslateUi(self, ViewProjectDialog):
        _translate = QtCore.QCoreApplication.translate
        ViewProjectDialog.setWindowTitle(_translate("ViewProjectDialog", "View project"))
        self.groupBox_3.setTitle(_translate("ViewProjectDialog", "Team Members: "))
        item = self.TeamMembersTable.horizontalHeaderItem(0)
        item.setText(_translate("ViewProjectDialog", "Username"))
        item = self.TeamMembersTable.horizontalHeaderItem(1)
        item.setText(_translate("ViewProjectDialog", "Name"))
        item = self.TeamMembersTable.horizontalHeaderItem(2)
        item.setText(_translate("ViewProjectDialog", "Start Date"))
        item = self.TeamMembersTable.horizontalHeaderItem(3)
        item.setText(_translate("ViewProjectDialog", "UserPkey"))
        self.removeMemberButton.setText(_translate("ViewProjectDialog", "Remove Member"))
        self.addMemberButton.setText(_translate("ViewProjectDialog", "Add Member"))
        self.groupBox.setTitle(_translate("ViewProjectDialog", "Project Details: "))
        self.label_3.setText(_translate("ViewProjectDialog", "Project Status: "))
        self.projectEndLE.setPlaceholderText(_translate("ViewProjectDialog", "Project is currently open"))
        self.label_8.setText(_translate("ViewProjectDialog", "Owner"))
        self.label_2.setText(_translate("ViewProjectDialog", "Project Description: "))
        self.label_4.setText(_translate("ViewProjectDialog", "Project Start Date: "))
        self.label.setText(_translate("ViewProjectDialog", "Project Name: "))
        self.label_7.setText(_translate("ViewProjectDialog", "Project End Date"))
        self.projectStatusCB.setItemText(0, _translate("ViewProjectDialog", "Not Started"))
        self.projectStatusCB.setItemText(1, _translate("ViewProjectDialog", "In-Progress"))
        self.projectStatusCB.setItemText(2, _translate("ViewProjectDialog", "Completed"))
        self.label_5.setText(_translate("ViewProjectDialog", "Project Due Date: "))
        self.ppMinL.setText(_translate("ViewProjectDialog", "0"))
        self.projectProgressHS.setToolTip(_translate("ViewProjectDialog", "Adjust to set the task progress "))
        self.ppmax.setText(_translate("ViewProjectDialog", "100"))
        self.label_13.setText(_translate("ViewProjectDialog", "Project Progress: "))
        self.saveChangesButton.setText(_translate("ViewProjectDialog", "Save Changes"))
        self.exitWithoutSavingButton.setText(_translate("ViewProjectDialog", "Exit"))
        self.closeProjectButton.setText(_translate("ViewProjectDialog", "Close Project"))
        self.deleteProjectButton.setText(_translate("ViewProjectDialog", "Delete Project"))
        self.label_6.setText(_translate("ViewProjectDialog", "View Project"))
