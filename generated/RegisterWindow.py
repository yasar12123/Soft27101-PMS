# Form implementation generated from reading ui file 'ui\registerWindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        RegisterWindow.setObjectName("RegisterWindow")
        RegisterWindow.resize(533, 635)
        self.centralwidget = QtWidgets.QWidget(parent=RegisterWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_5 = QtWidgets.QLabel(parent=self.frame)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.groupBox = QtWidgets.QGroupBox(parent=self.frame)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.FullnameLE = QtWidgets.QLineEdit(parent=self.groupBox)
        self.FullnameLE.setObjectName("FullnameLE")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.FullnameLE)
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.EmailLE = QtWidgets.QLineEdit(parent=self.groupBox)
        self.EmailLE.setObjectName("EmailLE")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.EmailLE)
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.UsernameLE = QtWidgets.QLineEdit(parent=self.groupBox)
        self.UsernameLE.setObjectName("UsernameLE")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.UsernameLE)
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.PasswordLE = QtWidgets.QLineEdit(parent=self.groupBox)
        self.PasswordLE.setObjectName("PasswordLE")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.PasswordLE)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.TermsAndCondTE = QtWidgets.QTextEdit(parent=self.frame)
        self.TermsAndCondTE.setObjectName("TermsAndCondTE")
        self.verticalLayout_3.addWidget(self.TermsAndCondTE)
        self.AcceptRadioButton = QtWidgets.QRadioButton(parent=self.frame)
        self.AcceptRadioButton.setEnabled(True)
        self.AcceptRadioButton.setObjectName("AcceptRadioButton")
        self.verticalLayout_3.addWidget(self.AcceptRadioButton)
        self.NotAcceptRadioButton = QtWidgets.QRadioButton(parent=self.frame)
        self.NotAcceptRadioButton.setObjectName("NotAcceptRadioButton")
        self.verticalLayout_3.addWidget(self.NotAcceptRadioButton)
        self.scrollArea = QtWidgets.QScrollArea(parent=self.frame)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 495, 78))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.RegistrationLabel = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.RegistrationLabel.setGeometry(QtCore.QRect(10, 10, 511, 51))
        self.RegistrationLabel.setText("")
        self.RegistrationLabel.setObjectName("RegistrationLabel")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.RegisterButton = QtWidgets.QPushButton(parent=self.frame)
        self.RegisterButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RegisterButton.sizePolicy().hasHeightForWidth())
        self.RegisterButton.setSizePolicy(sizePolicy)
        self.RegisterButton.setMinimumSize(QtCore.QSize(0, 0))
        self.RegisterButton.setBaseSize(QtCore.QSize(0, 0))
        self.RegisterButton.setIconSize(QtCore.QSize(16, 16))
        self.RegisterButton.setObjectName("RegisterButton")
        self.verticalLayout_3.addWidget(self.RegisterButton)
        self.verticalLayout.addWidget(self.frame)
        RegisterWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=RegisterWindow)
        self.statusbar.setObjectName("statusbar")
        RegisterWindow.setStatusBar(self.statusbar)

        self.retranslateUi(RegisterWindow)
        QtCore.QMetaObject.connectSlotsByName(RegisterWindow)

    def retranslateUi(self, RegisterWindow):
        _translate = QtCore.QCoreApplication.translate
        RegisterWindow.setWindowTitle(_translate("RegisterWindow", "Registration Window"))
        self.label_5.setText(_translate("RegisterWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:700;\">Registeration</span></p><p align=\"center\"><br/></p></body></html>"))
        self.label.setText(_translate("RegisterWindow", "Full Name:  "))
        self.label_3.setText(_translate("RegisterWindow", "Email Address:        "))
        self.label_2.setText(_translate("RegisterWindow", "Username "))
        self.label_4.setText(_translate("RegisterWindow", "Password: "))
        self.TermsAndCondTE.setHtml(_translate("RegisterWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Terms and Conditions</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">These Terms and Conditions (&quot;Terms&quot;) govern your access to and use of [Project Management App] (&quot;Project Managment App&quot;), provided by [TT Corp] (&quot;TT Corp&quot;). By accessing or using the App, you agree to be bound by these Terms. If you do not agree to these Terms, you may not access or use the App.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">1. Account Registration</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1.1 You must create an account to use certain features of the App. When creating an account, you agree to provide accurate, current, and complete information about yourself.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1.2 You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">2. Use of the App</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2.1 You may use the App only for lawful purposes and in accordance with these Terms. You agree not to use the App in any way that violates any applicable laws or regulations.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2.2 You may not:</p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Use the App in any manner that could disable, overburden, damage, or impair the App or interfere with any other party\'s use of the App.</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Attempt to gain unauthorized access to any part of the App.</li>\n"
"<li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Use any robot, spider, or other automatic device, process, or means to access the App for any purpose.</li></ul>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">3. Intellectual Property</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3.1 The App and its original content, features, and functionality are owned by the Company and are protected by international copyright, trademark, patent, trade secret, and other intellectual property or proprietary rights laws.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3.2 You may not modify, reproduce, distribute, create derivative works of, publicly display, publicly perform, republish, download, store, or transmit any of the material on the App, except as necessary for your own personal, non-commercial use.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">4. Privacy</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4.1 Your privacy is important to us. Please refer to our Privacy Policy for information on how we collect, use, and disclose your personal information.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">5. Limitation of Liability</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5.1 In no event shall the Company, its officers, directors, employees, or agents be liable to you for any indirect, incidental, special, consequential, or punitive damages, including without limitation, lost profits, data, use, goodwill, or other intangible losses, arising out of or in connection with your use of the App.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">6. Changes to Terms</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">6.1 The Company reserves the right to modify or revise these Terms at any time. Your continued use of the App following the posting of any changes to these Terms constitutes acceptance of those changes.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">7. Governing Law</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">7.1 These Terms shall be governed by and construed in accordance with the laws of [United Kingdom], without regard to its conflict of law provisions.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">8. Contact Us</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">8.1 If you have any questions about these Terms, please contact us.</p></body></html>"))
        self.AcceptRadioButton.setText(_translate("RegisterWindow", "Accept terms and conditions"))
        self.NotAcceptRadioButton.setText(_translate("RegisterWindow", "Do not accept terms and conditions"))
        self.RegisterButton.setText(_translate("RegisterWindow", "Register"))
