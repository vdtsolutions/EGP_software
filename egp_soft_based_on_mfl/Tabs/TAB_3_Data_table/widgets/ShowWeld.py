from PyQt5 import QtWidgets, QtCore
import egp_soft_based_on_mfl.Components.style1 as Style

class ShowWeldSelection(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()


    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        """
        Weld button located inside the third tab
        """
        self.ShowWeld = QtWidgets.QPushButton()
        self.ShowWeld.setGeometry(QtCore.QRect(690, 265, 160, 43))
        self.ShowWeld.setObjectName("Fetch Data")
        self.ShowWeld.setText("Fetch Weld Details")
        """
        Call the function show_weld
        """
        self.ShowWeld.clicked.connect(self.parent.Show_Weld)
        self.ShowWeld.setStyleSheet(Style.btn_type_primary)

        layout.addWidget(self.ShowWeld)
        self.setLayout(layout)

