# table_widget.py
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class DataTable(QTableWidget):
    def __init__(self, dataframe, start_index, end_index, all_halls, on_row_selected):
        super().__init__()

        self.df = dataframe
        self.start_index = start_index
        self.end_index = end_index
        self.all_halls = all_halls
        self.on_row_selected = on_row_selected

        self.cellClicked.connect(self._row_clicked)
        self._populate()

    def _populate(self):
        subset = self.df.iloc[self.start_index:self.end_index]

        self.setRowCount(len(subset))
        self.setColumnCount(len(subset.columns))
        self.setHorizontalHeaderLabels(subset.columns)

        for r, (_, row) in enumerate(subset.iterrows()):
            for c, val in enumerate(row):
                self.setItem(r, c, QTableWidgetItem(str(val)))

    def _row_clicked(self, row, col):
        actual_idx = self.start_index + row
        self.on_row_selected(actual_idx)

