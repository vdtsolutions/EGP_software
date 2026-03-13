import os
import time
from pathlib import Path
from egp_soft_based_on_mfl.Components.Configs import config_universal
from egp_soft_based_on_mfl.Tabs.TAB_5_Line_plot_abs_vs_ori.widgets.fetch_from_gcp import fetch_orientation_df_from_gcp
from egp_soft_based_on_mfl.Tabs.TAB_5_Line_plot_abs_vs_ori.widgets.helper_functions import fetch_weld_range, \
    safe_read_pickle, save_pickle_safely
from egp_soft_based_on_mfl.utils.loaderdialog.loader_dialog import BaseWorker



class LineChartWorker(BaseWorker):

    def __init__(self, tab):
        super().__init__()
        self.tab = tab

    def run(self):

        if self.isInterruptionRequested():
            return

        runid = self.tab.parent.runid
        weld_num = int(self.tab.combo_orientation.currentText())

        self.smooth_progress(0, 15, "Checking weld range...")

        if self.isInterruptionRequested():
            return

        with self.tab.config.connection.cursor() as cursor:

            result = fetch_weld_range(self.tab, cursor, runid, weld_num)

            if result is None or self.isInterruptionRequested():
                self.finished.emit(None)
                return

            path = Path(config_universal.roll_pkl_lc) / \
                   self.tab.parent.project_name.strip() / f"{weld_num}.pkl"

            os.makedirs(path.parent, exist_ok=True)

            self.smooth_progress(15, 35, "Checking cached data...")

            if self.isInterruptionRequested():
                return

            df_clock_holl = safe_read_pickle(self.tab, path)

            if df_clock_holl is not None:

                self.message.emit("Data already present")
                self.progress.emit(60)

                if self.isInterruptionRequested():
                    return

                time.sleep(0.4)

                self.message.emit("Loading cached data...")
                self.progress.emit(75)

                if self.isInterruptionRequested():
                    return

                time.sleep(0.4)

                self.message.emit("Preparing chart...")
                self.progress.emit(90)

                if self.isInterruptionRequested():
                    return

                self.finished.emit(df_clock_holl)
                return

            self.smooth_progress(35, 60, "Fetching data from GCP...")

            if self.isInterruptionRequested():
                return

            df_new = fetch_orientation_df_from_gcp(self.tab, result)

            if self.isInterruptionRequested():
                return

            self.smooth_progress(60, 80, "Saving cache...")

            save_pickle_safely(self.tab, path, df_new)

            if self.isInterruptionRequested():
                return

            self.smooth_progress(80, 95, "Preparing chart...")

            if self.isInterruptionRequested():
                return

            self.finished.emit(df_new)