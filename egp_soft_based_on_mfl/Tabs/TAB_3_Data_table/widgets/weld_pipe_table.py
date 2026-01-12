# frontend/widgets/FetchWeldToPipe.py
from PyQt5 import QtWidgets, QtCore
import egp_soft_based_on_mfl.Components.style1 as Style



class FetchWeldToPipe(QtWidgets.QTableWidget):
    """Reusable table widget for displaying Weld → Pipe mapping data."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.setGeometry(QtCore.QRect(30, 310, 1300, 235))
        self.setRowCount(7)
        self.setColumnCount(8)

        # --- Column widths ---
        for i in range(8):
            self.setColumnWidth(i, 160)

        self.horizontalHeader().setStretchLastSection(True)

        # --- Headers ---
        headers = [
            'pipe_id',
            'runid',
            'analytic_id',
            'lower_sensitivity',
            'upper_sensitivity',
            'length',
            'start_index',
            'end_index',
        ]
        self.setHorizontalHeaderLabels(headers)

        # --- Basic behavior ---
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def clear_table(self):
        """Utility to reset/clear the table contents."""
        self.setRowCount(0)

    def populate(self, rows):
        """Optional helper: populate the table with data tuples."""
        self.setRowCount(0)
        for r, row_data in enumerate(rows):
            self.insertRow(r)
            for c, data in enumerate(row_data):
                self.setItem(r, c, QtWidgets.QTableWidgetItem(str(data)))


class FetchWeldToPipeButton(QtWidgets.QWidget):
    """
    Reusable button widget for 'Fetch Weld To Pipe' functionality
    inside the third tab.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # parent = TabShowData
        self._setup_ui()

    def _setup_ui(self):
        """
        Create and style the 'Fetch Weld To Pipe' button,
        and connect it to the tab's ShowWeldToPipe function.
        """
        layout = QtWidgets.QVBoxLayout(self)

        # Original naming preserved
        self.Show_Weld_to_Pipe = QtWidgets.QPushButton()
        self.Show_Weld_to_Pipe.setGeometry(QtCore.QRect(600, 550, 160, 43))
        self.Show_Weld_to_Pipe.setObjectName("Fetch Data")
        self.Show_Weld_to_Pipe.setText("Fetch Weld To Pipe")
        self.Show_Weld_to_Pipe.setStyleSheet(Style.btn_type_primary)

        # ✅ Connect button click to tab method
        self.Show_Weld_to_Pipe.clicked.connect(self.parent.ShowWeldToPipe)

        layout.addWidget(self.Show_Weld_to_Pipe)
        self.setLayout(layout)
