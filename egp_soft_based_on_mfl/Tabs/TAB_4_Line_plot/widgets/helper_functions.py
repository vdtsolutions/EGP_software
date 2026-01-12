import pandas as pd
import numpy as np
from scipy.signal import savgol_filter, lfilter
from matplotlib.widgets import RectangleSelector
from matplotlib.transforms import Bbox
from sklearn.preprocessing import MinMaxScaler
from PyQt5.QtCore import QUrl
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt
from pathlib import Path
import os

# Dynamically locate the GMFL root (2 levels above this file)
GMFL_ROOT = Path(__file__).resolve().parents[3]


def gmfl_path(relative):
    """Return absolute path inside GMFL backend_data/temp folder."""
    temp_dir = GMFL_ROOT / "backend_data" / "data_generated" / "temp"
    os.makedirs(temp_dir, exist_ok=True)  # make sure folder exists
    return str(temp_dir / relative)



#this function is to plot hall sensor and prox sensor line chart for tab4 aka linechart (counter v sensor)
def plot_linechart_sensor(self, df_pipe):
    print("hi sensor linechart")
    self.index = df_pipe['index']
    oddo1 = (df_pipe['ODDO1'] - self.config.oddo1) / 1000

    self.figure_x5.clear()
    self.ax5 = self.figure_x5.add_subplot(111)
    self.ax5.figure.subplots_adjust(bottom=0.085, left=0.055, top=0.930, right=0.920)
    self.ax5.clear()

    res = [f'F{i}H{j}' for i in range(1, self.config.F_columns + 1) for j in range(1, 5)]
    df1 = df_pipe[res].apply(pd.to_numeric, errors='coerce')

    # ------------------- Denoising -------------------
    window_length = 15
    polyorder = 2
    for col in res:
        data = df1[col].values
        time_index = np.arange(len(df1))
        coefficients = np.polyfit(time_index, data, polyorder)
        trend = np.polyval(coefficients, time_index)
        data_dettrended = data - trend
        data_denoised = savgol_filter(data_dettrended, window_length, polyorder)
        df1.loc[:len(df1), col] = data_denoised

    for i, data in enumerate(res):
        df1[data] = df1[data] + i * 1400

    n = 15
    b = [1.0 / n] * n
    a = 1

    for i, data in enumerate(res):
        filtered_data = lfilter(b, a, df1[data])
        self.ax5.plot(self.index, filtered_data, label=i)

    self.ax5.margins(x=0, y=0)
    oddo_val = list(oddo1)
    num_ticks1 = len(self.ax5.get_xticks())
    tick_positions1 = [int(i) for i in np.linspace(0, len(oddo_val) - 1, num_ticks1)]

    ax4 = self.ax5.twiny()
    ax4.set_xticks(tick_positions1)
    ax4.set_xticklabels([f'{oddo_val[i]:.2f}' for i in tick_positions1], size=8)
    ax4.set_xlabel("Absolute Distance (m)", size=8)

    def on_hover(event):
        if event.inaxes:
            try:
                x, y = event.xdata, event.ydata
                if x is not None:
                    x = int(event.xdata)
                    y = int(event.ydata)
                    z = (df_pipe.loc[df_pipe.index == x, 'ODDO1']) - self.config.oddo1
                    Abs_distance = int(z.values[0])
                    index_value = df_pipe.loc[df_pipe.index == x, 'index']
                    index_value_1 = int(index_value.values[0])
                    self.toolbar_x5.set_message(
                        f"Index_Value={index_value_1}, Abs.Distance(mm)={Abs_distance / 1000:.2f},\nSensor_offset_Values={y}"
                    )
            except (IndexError, ValueError):
                print("Hovering outside valid data range.")

    self.canvas_x5.mpl_connect('motion_notify_event', on_hover)

    legend = self.ax5.legend(res, loc="upper left", bbox_to_anchor=(1.02, 0, 0.07, 1))
    d = {"down": 30, "up": -30}

    def func_scroll(evt):
        if legend.contains(evt):
            bbox = legend.get_bbox_to_anchor()
            bbox = Bbox.from_bounds(bbox.x0, bbox.y0 + d[evt.button], bbox.width, bbox.height)
            tr = legend.axes.transAxes.inverted()
            legend.set_bbox_to_anchor(bbox.transformed(tr))
            self.canvas_x5.draw_idle()

    self.canvas_x5.mpl_connect("scroll_event", func_scroll)

    # ------------------- Proximity Plot -------------------
    # df_proxi_data = [
    #     'F1P1', 'F2P2', 'F3P3', 'F4P4', 'F5P1', 'F6P2', 'F7P3', 'F8P4', 'F9P1', 'F10P2',
    #     'F11P3', 'F12P4', 'F13P1', 'F14P2', 'F15P3', 'F16P4', 'F17P1', 'F18P2', 'F19P3',
    #     'F20P4', 'F21P1', 'F22P2', 'F23P3', 'F24P4', 'F25P1', 'F26P2', 'F27P3', 'F28P4',
    #     'F29P1', 'F30P2', 'F31P3', 'F32P4', 'F33P1', 'F34P2', 'F35P3', 'F36P4'
    # ]
    df_proxi_data = self.config.sensor_columns_prox

    scaler = MinMaxScaler()
    scaled_values = scaler.fit_transform(df_pipe[df_proxi_data])
    for i, col in enumerate(df_proxi_data):
        df_pipe[col] = scaled_values[:, i]

    n = 15
    b = [1.0 / n] * n
    a = 1
    ls = [round(i * 0.3, 1) for i in range(1, 37)]

    for j1, column2 in enumerate(df_proxi_data):
        df_pipe[column2] = df_pipe[column2] + ls[j1]

    fig = go.Figure()
    for i1, column1 in enumerate(df_proxi_data):
        yy = lfilter(b, a, df_pipe[column1])
        fig.add_trace(go.Scatter(x=df_pipe.index, y=yy, name=column1))

    fig.update_layout(
        width=1800,
        height=400,
        title={'x': 0.5},
        font={"family": "courier"},
    )
    fig.update_xaxes(
        title_text="ODDO1(Absolute Distance(m))",
        tickfont=dict(size=11),
        dtick=1000,
        tickangle=0,
        showticklabels=True,
        ticklen=0,
    )


    #saving proximity line chart
    file_path = gmfl_path("h_line_chart_proxi.html")
    print(f"file path: ----- {file_path}")
    pio.write_html(fig, file=file_path, auto_open=False)
    self.m_output_proxi.load(QUrl.fromLocalFile(file_path))

    self.canvas_x5.draw()
    self.config.print_with_time("End plotting at : ")

    # --- Rectangle Selector (same as original logic) ---self.figure_x5.gca()
    self.rs1 = RectangleSelector(self.figure_x5.gca(),
                                 lambda eclick, erelease: line_selection5(self, eclick, erelease),
                                 useblit=True)
    plt.connect('key_press_event', self.rs1)






#this function is to select the region on hall sensor linechart it makes a rec/sq shape selection
def line_selection5(self, eclick, erelease):
    """Handles rectangular selection and saves start/end coords."""
    try:
        if abs(eclick.x - erelease.x) >= 3 and abs(eclick.y - erelease.y) >= 3:
            self.rect_start_1 = (eclick.xdata, eclick.ydata)
            self.rect_end_1 = (erelease.xdata, erelease.ydata)

            ax = self.figure_x5.gca()
            for patch in list(ax.patches):  # clear existing rectangles
                patch.remove()

            rect = plt.Rectangle(
                (min(self.rect_start_1[0], self.rect_end_1[0]),
                 min(self.rect_start_1[1], self.rect_end_1[1])),
                abs(self.rect_end_1[0] - self.rect_start_1[0]),
                abs(self.rect_end_1[1] - self.rect_start_1[1]),
                edgecolor='black',
                linewidth=1,
                fill=False
            )
            ax.add_patch(rect)
            self.canvas_x5.draw()

            print(f"[DEBUG] Rectangle selected: {self.rect_start_1} → {self.rect_end_1}")
        else:
            print("[DEBUG] Too small to select.")
    except Exception as e:
        import traceback
        print(f"[ERROR] line_selection5 failed: {e}")
        traceback.print_exc()