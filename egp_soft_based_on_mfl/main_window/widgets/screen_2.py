from PyQt5 import QtCore, QtWidgets, QtGui
import egp_soft_based_on_mfl.Components.style1 as Style

def build_screen2(self):
    self.screen2 = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(self.screen2)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(10)

    # -------- TAB BAR HOLDER --------
    self.tabbar_container = QtWidgets.QVBoxLayout()
    self.tabbar_container.setContentsMargins(0, 0, 0, 0)
    self.tabbar_container.setSpacing(0)
    layout.addLayout(self.tabbar_container)

    # -------- TAB CONTENT AREA --------
    self.main_container = QtWidgets.QVBoxLayout()
    self.main_container.setContentsMargins(0, 0, 0, 0)
    layout.addLayout(self.main_container)

    # -------- Home button AT BOTTOM --------
    self.back_btn = QtWidgets.QPushButton("Home")
    self.back_btn.setStyleSheet(Style.btn_back)
    self.back_btn.setFixedHeight(40)
    self.back_btn.clicked.connect(lambda: confirm_go_home(self))

    bottom_box = QtWidgets.QHBoxLayout()
    bottom_box.addStretch()
    bottom_box.addWidget(self.back_btn)
    bottom_box.addStretch()

    layout.addLayout(bottom_box)



# ----------------------------------------------------------------------
# GO HOME -> Return to Landing Screen
# ----------------------------------------------------------------------

def confirm_go_home(self):
    msg = QtWidgets.QMessageBox(self)
    msg.setWindowTitle("Confirm Action")
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText("Are you sure you want to go to home?\n\nThe current project session will be closed.")
    msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
    msg.button(QtWidgets.QMessageBox.Yes).setText("Yes, Go to Home")
    msg.button(QtWidgets.QMessageBox.Cancel).setText("Cancel")

    result = msg.exec_()

    if result == QtWidgets.QMessageBox.Yes:
        reset_default_screen(self)  # Perform your go-back action
    else:
        pass  # Do nothing, stay on screen2

def reset_default_screen(self):
    self.stack.setCurrentIndex(0)
    self.menubar.setVisible(False)
    self.project_name = ""