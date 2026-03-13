import pandas as pd

from egp_soft_based_on_mfl.Components.Configs import config_universal
from egp_soft_based_on_mfl.utils.loaderdialog.loader_dialog import BaseWorker
from .helper_func import func, select_weld
from concurrent.futures import ThreadPoolExecutor


class WeldSelectionWorker(BaseWorker):

    def __init__(self, tab):
        super().__init__()
        self.tab = tab

    def run(self):

        tab = self.tab

        runid = tab.parent.runid
        start15 = int(tab.start15.text())
        end15 = int(tab.end15.text())

        self.message.emit("Preparing weld selection...")
        self.progress.emit(5)

        future = []
        config_universal.print_with_time("Start_time")

        executor = ThreadPoolExecutor(max_workers=10)

        x = 20000

        while start15 < end15:

            if self.isInterruptionRequested():
                return

            future.append(
                executor.submit(func, tab, [start15 + 1, start15 + x])
            )

            start15 = start15 + x

        self.message.emit("Fetching sensor data...")
        self.progress.emit(40)

        d1 = []

        for f in future:

            if self.isInterruptionRequested():
                return

            df = f.result()
            d1.append(df)

        self.message.emit("Combining data...")
        self.progress.emit(70)

        df_plot_data1 = pd.concat(d1)

        self.message.emit("Finalizing...")
        self.progress.emit(90)

        config_universal.print_with_time("End_time")

        self.progress.emit(100)
        self.message.emit("Completed")

        self.finished.emit(df_plot_data1)