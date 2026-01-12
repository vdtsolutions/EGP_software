from PyQt5 import QtCore, QtGui, QtWidgets
from main import Ui_MainWindow
import Components.config as Config
import Components.logger as logger

connection = Config.connection


class Ui_Dialog2(object):
    def login_check(self):
        uname = self.U_name_text.text()
        passw = self.pass_text.text()
        with connection.cursor() as cursor:
            # result = connection.execute("SELECT * FROM users WHERE USERNAME = ? AND PASSWORD = ?", (uname, passw))
            cursor.execute(
                "SELECT * FROM users WHERE UserName='" + str(uname) + "' AND Password='" + str(passw) + "'")
            allSQLRows = cursor.fetchall()
            if (len(allSQLRows) > 0):
                logger.user_name = uname
                logger.log_info("Login Success")
                self.welcomeWindow = QtWidgets.QMainWindow()
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self.welcomeWindow)
                Dialog.hide()
                self.welcomeWindow.show()
                # print("Login success")
                # MainWindow = QtWidgets.QMainWindow()
                # ui = Ui_MainWindow()
                # ui.setupUi(MainWindow)
                # Dialog.hide()
                #  MainWindow.show()
            else:
                logger.log_warning("login failed")
                print("invalid login")

    def setupUi2(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 500)
        Dialog.setStyleSheet("QDialog{\n"
                             "background-color: rgb(167, 210, 255);\n"
                             "}\n"
                             "QPushButton{\n"
                             "background-color: rgb(255, 255, 255);\n"
                             "border:none;\n"
                             "}\n"
                             "QLabel{\n"
                             "color:rgb(255, 23, 54);\n"
                             "font-size:20px;\n"
                             "}")
        self.U_name_Lable = QtWidgets.QLabel(Dialog)
        self.U_name_Lable.setGeometry(QtCore.QRect(150, 200, 111, 21))
        self.U_name_Lable.setObjectName("U_name_Lable")
        self.Pass_Lable = QtWidgets.QLabel(Dialog)
        self.Pass_Lable.setGeometry(QtCore.QRect(150, 250, 111, 21))
        self.Pass_Lable.setObjectName("Pass_Lable")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(190, 120, 201, 31))
        font = QtGui.QFont()
        # font.setPointSize(-1)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel#label{\n"
                                 "font-size:30px;\n"
                                 "}")
        self.label.setObjectName("label")
        self.pass_text = QtWidgets.QLineEdit(Dialog)
        self.pass_text.setGeometry(QtCore.QRect(280, 250, 131, 20))
        self.pass_text.setObjectName("pass_text")
        self.login_button = QtWidgets.QPushButton(Dialog)
        self.login_button.setGeometry(QtCore.QRect(280, 300, 61, 23))
        self.login_button.setObjectName("login_button")
        ##############button event################
        self.login_button.clicked.connect(self.login_check)
        ##########################################
        # self.sighup_button = QtWidgets.QPushButton(Dialog)
        # self.sighup_button.setGeometry(QtCore.QRect(210, 190, 61, 23))
        # self.sighup_button.setObjectName("sighup_button")
        self.U_name_text = QtWidgets.QLineEdit(Dialog)
        self.U_name_text.setGeometry(QtCore.QRect(280, 200, 131, 20))
        self.U_name_text.setStyleSheet("")
        self.U_name_text.setObjectName("U_name_text")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Login"))
        self.U_name_Lable.setText(_translate("Dialog", "USER NAME"))
        self.Pass_Lable.setText(_translate("Dialog", "PASSWORD"))
        self.label.setText(_translate("Dialog", "LOGIN FORM"))
        self.login_button.setText(_translate("Dialog", "Login"))
        # self.sighup_button.setText(_translate("Dialog", "Sign-up"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog2()
    ui.setupUi2(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
