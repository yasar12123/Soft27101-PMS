# Form implementation generated from reading ui file 'ui\viewTaskDialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ViewTaskDialog(object):
    def setupUi(self, ViewTaskDialog):
        ViewTaskDialog.setObjectName("ViewTaskDialog")
        ViewTaskDialog.resize(816, 559)
        self.gridLayout_3 = QtWidgets.QGridLayout(ViewTaskDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_3 = QtWidgets.QGroupBox(parent=ViewTaskDialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.TaskCommentsLW = QtWidgets.QListWidget(parent=self.groupBox_3)
        self.TaskCommentsLW.setObjectName("TaskCommentsLW")
        self.verticalLayout_8.addWidget(self.TaskCommentsLW)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.addTaskCommentButton = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.addTaskCommentButton.setObjectName("addTaskCommentButton")
        self.horizontalLayout_6.addWidget(self.addTaskCommentButton)
        self.verticalLayout_8.addLayout(self.horizontalLayout_6)
        self.verticalLayout.addLayout(self.verticalLayout_8)
        self.gridLayout_3.addWidget(self.groupBox_3, 1, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(parent=ViewTaskDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 8, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)
        self.taskStartDE = QtWidgets.QDateEdit(parent=self.groupBox)
        self.taskStartDE.setCalendarPopup(True)
        self.taskStartDE.setObjectName("taskStartDE")
        self.gridLayout.addWidget(self.taskStartDE, 4, 2, 1, 1)
        self.taskEndLE = QtWidgets.QLineEdit(parent=self.groupBox)
        self.taskEndLE.setReadOnly(True)
        self.taskEndLE.setClearButtonEnabled(False)
        self.taskEndLE.setObjectName("taskEndLE")
        self.gridLayout.addWidget(self.taskEndLE, 6, 2, 1, 1)
        self.taskStatusCB = QtWidgets.QComboBox(parent=self.groupBox)
        self.taskStatusCB.setAcceptDrops(False)
        self.taskStatusCB.setObjectName("taskStatusCB")
        self.taskStatusCB.addItem("")
        self.taskStatusCB.addItem("")
        self.gridLayout.addWidget(self.taskStatusCB, 3, 2, 1, 1)
        self.taskDueDE = QtWidgets.QDateEdit(parent=self.groupBox)
        self.taskDueDE.setCalendarPopup(True)
        self.taskDueDE.setObjectName("taskDueDE")
        self.gridLayout.addWidget(self.taskDueDE, 5, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.taskNameLE = QtWidgets.QLineEdit(parent=self.groupBox)
        self.taskNameLE.setObjectName("taskNameLE")
        self.gridLayout.addWidget(self.taskNameLE, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.taskDescTE = QtWidgets.QTextEdit(parent=self.groupBox)
        self.taskDescTE.setObjectName("taskDescTE")
        self.gridLayout.addWidget(self.taskDescTE, 2, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.taskAssigneeCB = QtWidgets.QComboBox(parent=self.groupBox)
        self.taskAssigneeCB.setObjectName("taskAssigneeCB")
        self.gridLayout.addWidget(self.taskAssigneeCB, 7, 2, 1, 1)
        self.taskAssignerLE = QtWidgets.QLineEdit(parent=self.groupBox)
        self.taskAssignerLE.setReadOnly(True)
        self.taskAssignerLE.setPlaceholderText("")
        self.taskAssignerLE.setClearButtonEnabled(False)
        self.taskAssignerLE.setObjectName("taskAssignerLE")
        self.gridLayout.addWidget(self.taskAssignerLE, 8, 2, 1, 1)
        self.projectNameLE = QtWidgets.QLineEdit(parent=self.groupBox)
        self.projectNameLE.setObjectName("projectNameLE")
        self.gridLayout.addWidget(self.projectNameLE, 0, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.taskChangesLabel = QtWidgets.QLabel(parent=self.groupBox)
        self.taskChangesLabel.setText("")
        self.taskChangesLabel.setObjectName("taskChangesLabel")
        self.verticalLayout_3.addWidget(self.taskChangesLabel)
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
        self.closeTaskButton = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.closeTaskButton.setObjectName("closeTaskButton")
        self.horizontalLayout.addWidget(self.closeTaskButton)
        self.deleteTaskButton = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.deleteTaskButton.setObjectName("deleteTaskButton")
        self.horizontalLayout.addWidget(self.deleteTaskButton)
        self.verticalLayout_4.addWidget(self.groupBox_4)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.gridLayout_3.addWidget(self.groupBox, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(parent=ViewTaskDialog)
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

        self.retranslateUi(ViewTaskDialog)
        QtCore.QMetaObject.connectSlotsByName(ViewTaskDialog)

    def retranslateUi(self, ViewTaskDialog):
        _translate = QtCore.QCoreApplication.translate
        ViewTaskDialog.setWindowTitle(_translate("ViewTaskDialog", "View Task"))
        self.groupBox_3.setTitle(_translate("ViewTaskDialog", "Task Comments: "))
        self.addTaskCommentButton.setText(_translate("ViewTaskDialog", "Add Comment"))
        self.groupBox.setTitle(_translate("ViewTaskDialog", "Task Details: "))
        self.label_2.setText(_translate("ViewTaskDialog", "Task Description: "))
        self.label_9.setText(_translate("ViewTaskDialog", "Assigned By: "))
        self.label_8.setText(_translate("ViewTaskDialog", "Assigned To: "))
        self.taskEndLE.setPlaceholderText(_translate("ViewTaskDialog", "Task is currently open"))
        self.taskStatusCB.setItemText(0, _translate("ViewTaskDialog", "Not Started"))
        self.taskStatusCB.setItemText(1, _translate("ViewTaskDialog", "In-Progress"))
        self.label_5.setText(_translate("ViewTaskDialog", "Task Due Date: "))
        self.label_3.setText(_translate("ViewTaskDialog", "Task Status: "))
        self.label.setText(_translate("ViewTaskDialog", "Task Name: "))
        self.label_4.setText(_translate("ViewTaskDialog", "Task Start Date: "))
        self.label_7.setText(_translate("ViewTaskDialog", "Task End Date"))
        self.label_10.setText(_translate("ViewTaskDialog", "Project Name: "))
        self.saveChangesButton.setText(_translate("ViewTaskDialog", "Save Changes"))
        self.exitWithoutSavingButton.setText(_translate("ViewTaskDialog", "Exit"))
        self.closeTaskButton.setText(_translate("ViewTaskDialog", "Close Task"))
        self.deleteTaskButton.setText(_translate("ViewTaskDialog", "Delete Task"))
        self.label_6.setText(_translate("ViewTaskDialog", "View Task"))
