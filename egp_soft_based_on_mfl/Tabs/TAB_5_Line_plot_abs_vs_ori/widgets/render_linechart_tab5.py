import numpy as np
import plotly.io as pio
import plotly.graph_objs as go
from PyQt5.QtCore import Qt, QUrl
from scipy.signal import savgol_filter, lfilter
from pathlib import Path
import os

# Dynamically locate the GMFL root (2 levels above this file)
GMFL_ROOT = Path(__file__).resolve().parents[3]


def gmfl_path(relative):
    """Return absolute path inside GMFL backend_data/temp folder."""
    temp_dir = GMFL_ROOT / "backend_data" / "data_generated" / "temp"
    os.makedirs(temp_dir, exist_ok=True)  # make sure folder exists
    return str(temp_dir / relative)


def render_linechart_tab5(self, df_new, html_name="linechart_tab5.html"):
    """
    Renders the Tab-5 line chart from a dataframe shaped like df_new.
    Keeps identical logic: 15-point moving-average (lfilter), dtick=300,
    HH:MM columns (00:00..11:55), writes HTML, loads into QWebEngineView.
    Returns the written file path.
    """
    print("generating linechart for tab 5")
    # --- unchanged computations ---
    df_clock_holl_oddo1 = (df_new['ODDO1'] / 1000).round(3)  # kept for parity even if unused
    df_clock_index = df_new['index']
    df_new_1 = df_new[[f"{h:02}:{int(m):02}" for h in range(12) for m in np.arange(0, 60, self.config.minute)]]

    n = 15
    b = [1.0 / n] * n
    a = 1

    fig = go.Figure()
    for column1 in df_new_1.columns:
        filtered_data = lfilter(b, a, df_new_1[column1])
        fig.add_trace(go.Scatter(x=df_clock_index, y=filtered_data, name=column1))

    fig.update_xaxes(dtick=300, title_text="Absolute Distance(m)", tickangle=0)

    file_path = gmfl_path(html_name)
    pio.write_html(fig, file=file_path, auto_open=False)
    self.m_output_orientation.load(QUrl.fromLocalFile(file_path))
    return file_path
