from PyQt5.QtWidgets import QMessageBox, QApplication

def exit_app(self):

    reply = QMessageBox.question(
        self,
        "Exit Application",
        "Are you sure you want to exit?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        QApplication.instance().quit()