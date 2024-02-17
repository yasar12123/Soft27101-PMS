# Form implementation generated from reading ui file 'ui\addProjectDialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AddProjectDialog(object):
    def setupUi(self, AddProjectDialog):
        AddProjectDialog.setObjectName("AddProjectDialog")
        AddProjectDialog.resize(473, 372)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddProjectDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtWidgets.QLabel(parent=AddProjectDialog)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.projectDueDE = QtWidgets.QDateEdit(parent=AddProjectDialog)
        self.projectDueDE.setCalendarPopup(True)
        self.projectDueDE.setObjectName("projectDueDE")
        self.gridLayout.addWidget(self.projectDueDE, 4, 2, 1, 1)
        self.projectStatusCB = QtWidgets.QComboBox(parent=AddProjectDialog)
        self.projectStatusCB.setAcceptDrops(False)
        self.projectStatusCB.setObjectName("projectStatusCB")
        self.projectStatusCB.addItem("")
        self.projectStatusCB.addItem("")
        self.gridLayout.addWidget(self.projectStatusCB, 2, 2, 1, 1)
        self.projectStartDE = QtWidgets.QDateEdit(parent=AddProjectDialog)
        self.projectStartDE.setCalendarPopup(True)
        self.projectStartDE.setObjectName("projectStartDE")
        self.gridLayout.addWidget(self.projectStartDE, 3, 2, 1, 1)
        self.projectNameLE = QtWidgets.QLineEdit(parent=AddProjectDialog)
        self.projectNameLE.setObjectName("projectNameLE")
        self.gridLayout.addWidget(self.projectNameLE, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=AddProjectDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.projectDescTE = QtWidgets.QTextEdit(parent=AddProjectDialog)
        self.projectDescTE.setObjectName("projectDescTE")
        self.gridLayout.addWidget(self.projectDescTE, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=AddProjectDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=AddProjectDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=AddProjectDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=AddProjectDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.addProjectStatusLabel = QtWidgets.QLabel(parent=AddProjectDialog)
        self.addProjectStatusLabel.setText("")
        self.addProjectStatusLabel.setObjectName("addProjectStatusLabel")
        self.verticalLayout.addWidget(self.addProjectStatusLabel)
        self.frame_3 = QtWidgets.QFrame(parent=AddProjectDialog)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addProjectButton = QtWidgets.QPushButton(parent=self.frame_3)
        self.addProjectButton.setObjectName("addProjectButton")
        self.horizontalLayout.addWidget(self.addProjectButton)
        self.exitProjectButton = QtWidgets.QPushButton(parent=self.frame_3)
        self.exitProjectButton.setObjectName("exitProjectButton")
        self.horizontalLayout.addWidget(self.exitProjectButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.frame_3)

        self.retranslateUi(AddProjectDialog)
        QtCore.QMetaObject.connectSlotsByName(AddProjectDialog)

    def retranslateUi(self, AddProjectDialog):
        _translate = QtCore.QCoreApplication.translate
        AddProjectDialog.setWindowTitle(_translate("AddProjectDialog", "Add new project"))
        self.label_6.setText(_translate("AddProjectDialog", "Add a new project"))
        self.projectStatusCB.setItemText(0, _translate("AddProjectDialog", "Open"))
        self.projectStatusCB.setItemText(1, _translate("AddProjectDialog", "Not Started"))
        self.label_3.setText(_translate("AddProjectDialog", "Project Status: "))
        self.label_5.setText(_translate("AddProjectDialog", "Project Due Date: "))
        self.label_4.setText(_translate("AddProjectDialog", "Project Start Date: "))
        self.label_2.setText(_translate("AddProjectDialog", "Project Description: "))
        self.label.setText(_translate("AddProjectDialog", "Project Name: "))
        self.addProjectButton.setText(_translate("AddProjectDialog", "Add Project"))
        self.exitProjectButton.setText(_translate("AddProjectDialog", "Exit (without saving)"))