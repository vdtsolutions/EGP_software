# frontend/widgets/WeldTable.py
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableView


class WeldTable(QtWidgets.QTableWidget):
    """Reusable Weld data table widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.setGeometry(QtCore.QRect(30, 30, 1000, 170))
        self.setRowCount(7)
        self.setColumnCount(11)

        # --- Column widths ---
        for i in range(11):
            self.setColumnWidth(i, 140)

        self.horizontalHeader().setStretchLastSection(True)

        # --- Column headers ---
        headers = [
            'weld_number', 'runid', 'analytic_id', 'sensitivity', 'length',
            'start_index', 'end_index', 'start_oddo1', 'end_oddo1',
            'start_oddo2', 'end_oddo2'
        ]
        self.setHorizontalHeaderLabels(headers)

        # --- Selection & interaction ---
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def bind_double_click(self, slot_func):
        """Attach a function to run when a row is double-clicked."""
        self.doubleClicked.connect(slot_func)
