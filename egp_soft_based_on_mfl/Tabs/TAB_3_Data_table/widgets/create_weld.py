from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QInputDialog

import egp_soft_based_on_mfl.Components.style1 as Style
from egp_soft_based_on_mfl.extras import weld_update


class CreateWeldButton(QtWidgets.QWidget):
    """Reusable 'Create Weld and Pipe' button."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent   # this will be TabShowData
        self._setup_ui()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # --- Button setup ---
        self.create_weld = QtWidgets.QPushButton()
        self.create_weld.setGeometry(QtCore.QRect(480, 265, 180, 43))
        self.create_weld.setObjectName("Create Weld Data")
        self.create_weld.setText("Create Weld and Pipe")
        self.create_weld.setStyleSheet(Style.btn_type_primary)

        # --- Connect to parent tab's CreateWeld method ---
        self.create_weld.clicked.connect(self.CreateWeld)

        layout.addWidget(self.create_weld)
        self.setLayout(layout)

    def CreateWeld(self):
        try:
            self.sensitivity, okPressed = QInputDialog.getText(self, "Get integer", "sensitivity")
            if okPressed:
                pass
                # self.sensitivifty = self.sensitivity
            self.weldupdate = weld_update.Query_flow(self.parent.parent.runid, self.sensitivity)
        except:
            # logger.log_error("sensitivity is not found")
            pass