from PyQt5.QtWidgets import QMessageBox

from egp_soft_based_on_mfl.Components import CreateProject, endcounter_to_startcounter_distance


def create_project(self):
    self.uploadData = CreateProject.AddProject()

def endcounter_to_startcounter(self):
    try:
        self.calculate_distance=endcounter_to_startcounter_distance.CalDistance(self.runid)
    except:
        QMessageBox.about(self, 'Info', 'Please select the runid')