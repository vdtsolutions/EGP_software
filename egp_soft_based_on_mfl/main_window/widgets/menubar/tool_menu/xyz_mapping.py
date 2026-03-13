import os
import subprocess
from PyQt5.QtWidgets import QMessageBox

from egp_soft_based_on_mfl.Components.Configs import config_universal

def open_google_earth(self):

    path = rf"{config_universal.google_earth_pro}"

    # confirmation popup
    reply = QMessageBox.question(
        None,
        "Open Google Earth Pro",
        "This will open Google Earth Pro.\nDo you want to proceed?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:

        if os.path.exists(path):
            subprocess.Popen(path)

        else:
            QMessageBox.warning(
                None,
                "Google Earth Pro Not Found",
                "Google Earth Pro executable was not found.\n\n"
                "If Google Earth Pro is already installed, please check the path configuration inside config_unversal.py.\n"
                "Otherwise, install Google Earth Pro before proceeding."
            )