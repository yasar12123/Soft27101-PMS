# Form implementation generated from reading ui file 'ui/viewProjectAddTeamMemberDialog.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ViewProjectAddTeamMemberDialog(object):
    def setupUi(self, ViewProjectAddTeamMemberDialog):
        ViewProjectAddTeamMemberDialog.setObjectName("ViewProjectAddTeamMemberDialog")
        ViewProjectAddTeamMemberDialog.resize(312, 294)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ViewProjectAddTeamMemberDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(parent=ViewProjectAddTeamMemberDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.verticalLayout_2.addWidget(self.frame)
        self.groupBox = QtWidgets.QGroupBox(parent=ViewProjectAddTeamMemberDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.projectNameLE = QtWidgets.QLineEdit(parent=self.groupBox)
        self.projectNameLE.setObjectName("projectNameLE")
        self.verticalLayout_3.addWidget(self.projectNameLE)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=ViewProjectAddTeamMemberDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.userCB = QtWidgets.QComboBox(parent=self.groupBox_2)
        self.userCB.setEditable(True)
        self.userCB.setObjectName("userCB")
        self.verticalLayout.addWidget(self.userCB)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(parent=ViewProjectAddTeamMemberDialog)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.addUserConfirmLE = QtWidgets.QLabel(parent=self.groupBox_3)
        self.addUserConfirmLE.setText("")
        self.addUserConfirmLE.setObjectName("addUserConfirmLE")
        self.verticalLayout_4.addWidget(self.addUserConfirmLE)
        self.addUserButton = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.addUserButton.setObjectName("addUserButton")
        self.verticalLayout_4.addWidget(self.addUserButton)
        self.exitButton = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.exitButton.setObjectName("exitButton")
        self.verticalLayout_4.addWidget(self.exitButton)
        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.retranslateUi(ViewProjectAddTeamMemberDialog)
        QtCore.QMetaObject.connectSlotsByName(ViewProjectAddTeamMemberDialog)

    def retranslateUi(self, ViewProjectAddTeamMemberDialog):
        _translate = QtCore.QCoreApplication.translate
        ViewProjectAddTeamMemberDialog.setWindowTitle(_translate("ViewProjectAddTeamMemberDialog", "Add Team Member"))
        self.label_6.setText(_translate("ViewProjectAddTeamMemberDialog", "Search and Add Team Member"))
        self.groupBox.setTitle(_translate("ViewProjectAddTeamMemberDialog", "Project Name: "))
        self.groupBox_2.setTitle(_translate("ViewProjectAddTeamMemberDialog", "Serach for User: "))
        self.userCB.setPlaceholderText(_translate("ViewProjectAddTeamMemberDialog", "Select a User"))
        self.addUserButton.setText(_translate("ViewProjectAddTeamMemberDialog", "Add User"))
        self.exitButton.setText(_translate("ViewProjectAddTeamMemberDialog", "Exit"))
