from PyQt5.QtWidgets import QMessageBox

from egp_soft_based_on_mfl.Components import endcounter_to_startcounter_distance
from egp_soft_based_on_mfl.main_window.widgets.menubar.file_menu.create_project import AddProject


def create_project(self):
    self.uploadData = AddProject()

def endcounter_to_startcounter(self):
    try:
        self.calculate_distance=endcounter_to_startcounter_distance.CalDistance(self.runid)
    except:
        QMessageBox.about(self, 'Info', 'Please select the runid')