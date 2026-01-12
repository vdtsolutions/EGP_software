
from PyQt5 import QtWidgets, QtCore
import egp_soft_based_on_mfl.Components.style1 as Style
# from egp_soft_based_on_mfl.Components.Configs import config as config


# connection = config.connection
class FetchDefectList(QtWidgets.QTableWidget):
    """
    Reusable table widget for displaying defect list information.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """
        Initialize the defect list table structure, headers, and properties.
        """
        self.setGeometry(QtCore.QRect(30, 600, 1300, 235))
        self.setRowCount(7)
        self.setColumnCount(11)

        # --- Column widths ---
        for i in range(11):
            self.setColumnWidth(i, 160)

        self.horizontalHeader().setStretchLastSection(True)

        # --- Column headers ---
        headers = [
            'defect_id',
            'runid',
            'start_observation',
            'end_observation',
            'start_sensor',
            'end_sensor',
            'angle',
            'length',
            'breadth',
            'depth',
            'type'
        ]
        self.setHorizontalHeaderLabels(headers)

        # --- Behavior ---
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    # Optional helper to clear or populate
    def clear_table(self):
        """Clear all rows."""
        self.setRowCount(0)

    def populate(self, rows):
        """
        Populate table with data rows (list of tuples or lists).
        """
        self.setRowCount(0)
        for r, row_data in enumerate(rows):
            self.insertRow(r)
            for c, data in enumerate(row_data):
                self.setItem(r, c, QtWidgets.QTableWidgetItem(str(data)))






class FetchDefectListButton(QtWidgets.QWidget):
    """
    Reusable button widget for fetching the Defect List table.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent   # parent = TabShowData
        self._setup_ui()
        self.config = self.parent.config

    def _setup_ui(self):
        """
        Initialize button UI and connect to the parent's DefectList function.
        """
        layout = QtWidgets.QVBoxLayout(self)

        # Button setup
        self.Show_Defect_list = QtWidgets.QPushButton()
        self.Show_Defect_list.setGeometry(QtCore.QRect(800, 840, 160, 43))
        self.Show_Defect_list.setObjectName("Fetch Data")
        self.Show_Defect_list.setText("Fetch Defect List")
        self.Show_Defect_list.setStyleSheet(Style.btn_type_primary)

        # ✅ Connect to parent's method
        self.Show_Defect_list.clicked.connect(self.DefectList)

        layout.addWidget(self.Show_Defect_list)
        self.setLayout(layout)

    def DefectList(self):
        runid = self.parent.parent.runid
        with self.config.connection.cursor() as cursor:
            try:
                Fetch_weld_detail = "select id,runid,start_observation,end_observation,start_sensor,end_sensor,angle_hr_m,length,breadth,depth,type from defect_sensor_hm where runid='%s'"
                # Execute query.
                cursor.execute(Fetch_weld_detail, (int(runid)))
                self.parent.myTableWidget2.setRowCount(0)
                allSQLRows = cursor.fetchall()
                if allSQLRows:
                    for row_number, row_data in enumerate(allSQLRows):
                        self.parent.myTableWidget2.insertRow(row_number)
                        for column_num, data in enumerate(row_data):
                            self.parent.myTableWidget2.setItem(row_number, column_num, QtWidgets.QTableWidgetItem(str(data)))
                    self.parent.myTableWidget2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                else:
                    self.config.warning_msg("No record found", "")
            except:
                # logger.log_error("Fetch DefectList has some error")
                pass

