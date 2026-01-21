# workers.py
import os
import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
# from circular_dent_maker.modular_maker.gcp import gcp_fetch_clock
from egp_soft_based_on_mfl.Tabs.TAB_9_dent_analysis.modular_maker.gcp import gcp_fetch_clock


class FetchDataWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(object, str)   # raw_df, clock_pkl_path
    error = pyqtSignal(str)

    def __init__(self, start_index, end_index, weld_id, raw_folder, clock_folder):
        super().__init__()
        self.start_index = start_index
        self.end_index = end_index
        self.weld_id = weld_id
        self.raw_folder = raw_folder
        self.clock_folder = clock_folder

    def run(self):
        try:
            self.progress.emit("Fetching data…")

            gcp_fetch_clock(
                self.start_index,
                self.end_index,
                self.weld_id
            )

            self.progress.emit("Loading raw data…")
            raw_pkl = os.path.join(self.raw_folder, f"{self.weld_id}.pkl")
            raw_df = pd.read_pickle(raw_pkl)
            raw_df.columns = raw_df.columns.str.strip()

            clock_pkl = os.path.join(self.clock_folder, f"{self.weld_id}.pkl")

            self.finished.emit(raw_df, clock_pkl)

        except Exception as e:
            self.error.emit(str(e))
