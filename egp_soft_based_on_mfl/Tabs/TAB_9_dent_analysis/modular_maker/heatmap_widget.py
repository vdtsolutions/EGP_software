import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


num_of_sensors = 48
F_columns = int(num_of_sensors / 4)
minute = 720 / num_of_sensors
degree = minute / 2


class HeatmapWidget(QWidget):
    """
    Heatmap selector widget.
    Emits row_index on click.
    """

    def __init__(self, on_index_selected):
        super().__init__()

        self.pkl_path = None
        self.on_index_selected = on_index_selected

        self.MINUTE_STEP = int(minute)

        self._cid_click = None
        self._cid_hover = None
        self.ax = None

        from PyQt5.QtWidgets import QSizePolicy

        self.figure = Figure(figsize=(12, 4), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(450)

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def load_from_pkl(self, pkl_path):
        if not os.path.isfile(pkl_path):
            print("❌ Heatmap PKL not found:", pkl_path)
            return

        self.pkl_path = pkl_path
        self._load_and_plot()
        self.update()

    # ------------------------------------------------
    def _load_and_plot(self):
        if not os.path.isfile(self.pkl_path):
            return

        df = pd.read_pickle(self.pkl_path)
        df.columns = df.columns.astype(str).str.strip()

        clock_cols = [
            f"{h:02}:{m:02}"
            for h in range(12)
            for m in range(0, 60, self.MINUTE_STEP)
        ]

        val_ori = df[clock_cols]
        mean_vals = val_ori.mean()
        df_norm = ((val_ori - mean_vals) / mean_vals) * 100

        self.index_list = df["index"].tolist()
        self.oddo_list = df["ODDO1"].tolist()

        self.figure.clear()
        self.ax = self.figure.add_subplot(111)

        sns.heatmap(
            df_norm.transpose(),
            cmap="jet",
            vmin=-5,
            vmax=18,
            ax=self.ax,
            cbar_kws={"shrink": 0.8}
        )

        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Clock")

        self.canvas.draw_idle()

        if self._cid_click:
            self.canvas.mpl_disconnect(self._cid_click)
        if self._cid_hover:
            self.canvas.mpl_disconnect(self._cid_hover)

        self._cid_click = self.canvas.mpl_connect(
            "button_press_event", self._on_click
        )
        self._cid_hover = self.canvas.mpl_connect(
            "motion_notify_event", self._on_hover
        )

    # ------------------------------------------------
    def _on_hover(self, event):
        if event.xdata is None or event.ydata is None:
            return

        try:
            x = int(event.xdata)
            y = int(event.ydata)

            index_val = self.index_list[x]
            clock = y
            oddo = self.oddo_list[x]

            self.setToolTip(
                f"Index: {index_val}\n"
                f"Oddo: {oddo/1000:.3f} m\n"
                f"Clock row: {y}"
            )
        except Exception:
            pass

    # ------------------------------------------------
    def _on_click(self, event):
        if event.inaxes != self.ax:
            return
        if event.xdata is None:
            return

        x = int(round(event.xdata))
        if x < 0 or x >= len(self.index_list):
            return

        index_val = self.index_list[x]
        self.on_index_selected(index_val)

